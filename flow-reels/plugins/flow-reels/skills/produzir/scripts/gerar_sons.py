#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_sons.py  ·  sintetiza a biblioteca de efeitos sonoros do pacote

Os efeitos que o audio.py põe nos tempos do vídeo (o whoosh da transição, o pop
de um elemento que entra, o tique do contador) não vêm de banco de sons. Eles são
calculados aqui, amostra por amostra, com numpy: ruído filtrado, senoides que
decaem, envelopes. O arquivo existe por três motivos:

  licença   som baixado da internet quase sempre tem dono, e "livre" costuma
            querer dizer "livre para uso pessoal". Som calculado por este
            arquivo é obra do próprio pacote e pode ir em qualquer corte, pago,
            patrocinado ou não, e dentro do pacote distribuído.

  estilo    a marca é de tecnologia. O som certo é discreto, curto e limpo,
            quase uma textura de interface: nada de mola, buzina ou desenho
            animado. Com a receita no código, o estilo se ajusta por número.

  repetir   a mesma --semente gera os mesmos arquivos, então a biblioteca pode
            ser apagada e refeita sem mudar o som dos cortes.

São 15 famílias. Cada uma tem o arquivo base com o nome da família (whoosh.wav,
o que os cortes antigos sempre usaram, bit a bit igual ao da 3.0) e as
variações numeradas (whoosh-1.wav ... whoosh-4.wav): o mesmo desenho com outro
timbre, outra duração ou outra altura. O mesmo arquivo 15 vezes no reel é a
assinatura número um da edição automática; o audio.py sorteia, sem repetir em
seguida, entre o base e as variações (MOTOR.md, docs-4/variedade-e-som.md).

As seis da 3.0 (base + 4 variações cada):

  whoosh    0,45 s  ruído numa banda que sobe e desce, passando de um lado para
                    o outro. O ponto mais forte fica a 0,20 s do começo, para
                    cair em cima da transição.
  pop       0,08 s  uma bolha: um tom curto que sobe de altura enquanto some.
  tick      0,02 s  o tique do contador: um estalo seco, de madeira clara.
  clique    0,04 s  clique de interface, com o estalo de apertar e o de soltar.
  subida    0,50 s  riser curto: ruído abrindo para o agudo e um acorde baixo que
                    sobe uma quarta. Mais forte no fim, para terminar no evento.
  clarao    0,35 s  impacto suave para o clarão: um corpo grave curto, um sopro
                    médio que fecha e um brilho de ar que se abre no estéreo.

As nove da 4.0 (base + 3 variações cada):

  glitch    0,24 s  estalos digitais: grãos de bits esmagados, tom quadrado que
                    salta e um pedaço repetido (gagueira), cada um num lado.
  rebobina  0,60 s  fita acelerando: "fala" de fita que sobe de velocidade com
                    wow e flutter, chiado que abre, e a trava seca no fim.
  impacto   0,55 s  hit grave curto com corpo: senoide que cai, saturada para o
                    celular tocar, soco abafado e uma sala pequena.
  estatica  0,50 s  chiado de TV que liga e desliga: o tum da rede ao ligar, o
                    chiado tremulando e o zíper que desce ao desligar.
  energia   0,90 s  zumbido que cresce, como carga: tom que sobe com o filtro
                    abrindo e o tremolo acelerando. Mais forte no fim.
  carimbo   0,14 s  batida seca de borracha e madeira: baque, modos de madeira e
                    o tapa do papel, com o segundo toque do carimbo assentando.
  bip       0,08 s  bip digital de chip antigo: onda quadrada em 16 degraus.
  obturador 0,20 s  clique de câmera: o estalo que abre, a mola e o que fecha.
  raio      0,65 s  estalo elétrico: o craque, o arco que zumbe e a crepitação
                    cada vez mais rara.

Antes de ir para o disco, todo som passa pela mesma conferência: pico
verdadeiro (medido com sobreamostragem de 4x) no máximo -1 dBTP, nenhuma
componente contínua (DC), a primeira e a última amostra em zero (fade nas duas
pontas), a duração certa, nada de NaN, e cada variação diferente do base (a
distância entre os espectros, em bandas de terço de oitava, de pelo menos
0,5 dB em média, ou outra duração). Todos saem com o mesmo volume de curto prazo
(janela de 100 ms, ponderação K da ITU-R BS.1770), para soarem parelhos quando
você os ouve soltos. O volume dentro do corte quem decide é o audio.py, que mede
a voz antes.

A tabela impressa no fim é a "escuta técnica": duração, pico, pico verdadeiro,
RMS, nível de 100 ms, ponto forte, centroide e a distância de cada variação para
o base da família.

Uso:

    flow-reels produzir/gerar_sons
    flow-reels produzir/gerar_sons --saida componentes/sons --semente 7
    flow-reels produzir/gerar_sons --so glitch,raio

--saida    a pasta da biblioteca (padrão: componentes/sons/ na raiz do pacote).
--semente  o número que fixa o ruído (padrão 7). Outra semente dá outra
           variação do mesmo desenho de som.
--so       só estas famílias (base e variações), separadas por vírgula. O
           LEIA.md é reescrito com a medida de todos os arquivos da pasta.

Junto com os .wav sai o LEIA.md da pasta, com a origem, a licença, as medidas e
o comando para refazer.

Saída 0 = gerou e todos passaram na conferência. Saída 1 = algum som reprovou,
e nesse caso nada é gravado. Saída 2 = erro de uso.
"""

import argparse
import sys
import wave
from datetime import date
from pathlib import Path
sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / ".claude-plugin").is_dir()) / "lib"))
import fabrica  # noqa: E402  (onde mora cada coisa: a pasta de trabalho e o plugin)

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


SR = 48000            # taxa de amostragem de toda a cadeia de áudio do pacote
TETO_DBTP = -1.0      # pico verdadeiro máximo de cada som
NIVEL_CURTO = -18.0   # volume de curto prazo (janela de 100 ms) de cada som solto, em LUFS
SEMENTE = 7

# Ponderação K da ITU-R BS.1770 em 48 kHz: o filtro de prateleira e o passa-alta RLB.
K_PRATELEIRA = ((1.53512485958697, -2.69169618940638, 1.19839281085285),
                (1.0, -1.69065929318241, 0.73248077421585))
K_PASSA_ALTA = ((1.0, -2.0, 1.0),
                (1.0, -1.99004745483398, 0.99007225036621))

np = None  # carregado em main(), para o erro de numpy ausente sair em português


def erro(msg):
    sys.stdout.flush()
    print("  erro: " + msg, file=sys.stderr)


def carregar_numpy():
    try:
        import numpy
    except ImportError:
        erro("o numpy não está instalado neste Python.\n"
             "        Rode com o Python do pacote: .venv/bin/python, ou instale com: pip install numpy")
        sys.exit(2)
    return numpy


def achar_raiz():
    """O plugin: a biblioteca de sons é do pacote, e só quem mantém o pacote a refaz."""
    return fabrica.plugin()


# ---------------------------------------------------------------------------
# Ferramentas de síntese
# ---------------------------------------------------------------------------

def eixo(dur):
    """O eixo do tempo de um som de `dur` segundos."""
    return np.arange(int(round(dur * SR))) / SR


def suave(u):
    """Rampa de 0 a 1 sem quina nas pontas (smoothstep)."""
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)


def ataque(t, dur):
    """Subida em cosseno de 0 a 1 em `dur` segundos: tira o degrau do começo sem amolecer o som."""
    if dur <= 0:
        return (t >= 0).astype(float)
    return np.where(t < 0, 0.0, np.where(t < dur, 0.5 - 0.5 * np.cos(np.pi * t / dur), 1.0))


def fase(freq):
    """Fase acumulada de uma frequência que muda a cada amostra (sem salto entre amostras)."""
    return 2.0 * np.pi * np.cumsum(freq) / SR


def svf(x, fc, q):
    """Filtro de variáveis de estado (topologia TPT, de Zavalishin).

    Devolve passa-baixa, passa-faixa (com ganho 1 no centro) e passa-alta. O corte
    e o Q podem mudar a cada amostra sem estalar, que é o que faz o whoosh e a
    subida soarem como ar e não como degraus.
    """
    n = len(x)
    fc = np.broadcast_to(np.asarray(fc, dtype=float), (n,))
    q = np.broadcast_to(np.asarray(q, dtype=float), (n,))
    g = np.tan(np.pi * np.clip(fc, 10.0, 0.45 * SR) / SR)
    k = 1.0 / q
    a1 = 1.0 / (1.0 + g * (g + k))
    a2 = g * a1
    a3 = g * a2
    xs, A1, A2, A3 = x.tolist(), a1.tolist(), a2.tolist(), a3.tolist()
    baixa, faixa = [0.0] * n, [0.0] * n
    ic1 = ic2 = 0.0
    for i in range(n):
        v3 = xs[i] - ic2
        v1 = A1[i] * ic1 + A2[i] * v3
        v2 = ic2 + A2[i] * ic1 + A3[i] * v3
        ic1 = 2.0 * v1 - ic1
        ic2 = 2.0 * v2 - ic2
        baixa[i] = v2
        faixa[i] = v1
    baixa = np.array(baixa)
    faixa = np.array(faixa)
    alta = x - k * faixa - baixa
    return baixa, faixa * k, alta


def rms(x):
    return float(np.sqrt(np.mean(np.square(x)))) or 1e-12


def ruido_rosa(rng, n):
    """Ruído rosa (-3 dB por oitava): o sopro do ruído branco sem o chiado agudo que cansa."""
    m = 1 << int(np.ceil(np.log2(n)))
    espectro = np.fft.rfft(rng.standard_normal(m))
    f = np.fft.rfftfreq(m, 1.0 / SR)
    espectro /= np.sqrt(np.maximum(f, 40.0))
    espectro[f < 30.0] = 0.0          # sem deriva lenta: ela viraria grave embolado depois do envelope
    y = np.fft.irfft(espectro, m)[:n]
    return y / rms(y)


def estereo(mono):
    return np.stack([mono, mono], axis=1)


def fades(x, entrada, saida):
    """Fade em cosseno nas duas pontas: a primeira e a última amostra ficam em zero exato."""
    n = len(x)
    w = np.ones(n)
    ni = max(1, int(round(entrada * SR)))
    no = max(1, int(round(saida * SR)))
    w[:ni] = 0.5 - 0.5 * np.cos(np.pi * np.arange(ni) / ni)
    w[n - no:] = 0.5 + 0.5 * np.cos(np.pi * (np.arange(no) + 1) / no)
    return x * w[:, None]


def tirar_grave_inutil(x, corte=20.0):
    """Passa-alta de fase zero em 20 Hz, aplicado no espectro: nada abaixo do que se ouve."""
    n = len(x)
    m = 1 << int(np.ceil(np.log2(n + SR // 2)))
    espectro = np.fft.rfft(x, m, axis=0)
    f = np.fft.rfftfreq(m, 1.0 / SR)
    h = (f / corte) ** 2 / np.sqrt(1.0 + (f / corte) ** 4)
    return np.fft.irfft(espectro * h[:, None], m, axis=0)[:n]


def zerar_media(x):
    """Tira a componente contínua sem mexer nas pontas.

    Num som de 20 ms o passa-alta não alcança a média: uma senoide que decai tem
    soma líquida diferente de zero. Aqui a média sai subtraindo uma janela de Hann
    do mesmo comprimento (zero nas pontas, conteúdo abaixo de 50 Hz), na medida
    exata para a soma de cada canal dar zero.
    """
    janela = np.hanning(len(x))
    return x - np.outer(janela / janela.mean(), x.mean(axis=0))


def reverb_curto(x, rng, cauda=0.07, comprimento=0.30, mistura=0.22):
    """Um espaço pequeno e claro: convolução com ruído que decai, diferente em cada lado."""
    m_ir = int(comprimento * SR)
    t = np.arange(m_ir) / SR
    saida = x.copy()
    n = len(x)
    tamanho = 1 << int(np.ceil(np.log2(n + m_ir)))
    for c in range(x.shape[1]):
        ir = rng.standard_normal(m_ir) * np.exp(-t / cauda) * ataque(t, 0.004)
        _, ir, _ = svf(ir, 3200.0, 0.6)          # cauda sem chiado nem grave embolado
        ir /= np.sqrt(np.sum(ir ** 2))
        molhado = np.fft.irfft(np.fft.rfft(x[:, c], tamanho) * np.fft.rfft(ir, tamanho), tamanho)[:n]
        saida[:, c] = x[:, c] + mistura * molhado
    return saida
# ---------------------------------------------------------------------------
# Ferramentas dos sons da 4.0
# ---------------------------------------------------------------------------

def pico_de(x):
    return float(np.max(np.abs(x))) or 1e-12


def descida(t, inicio, dur):
    """O contrário do ataque: 1 até `inicio`, cai em cosseno até 0 em `dur` segundos."""
    return 1.0 - ataque(t - inicio, dur)


def pan(mono, posicao):
    """Põe um som mono numa posição de -1 (esquerda) a 1 (direita), com potência constante."""
    angulo = (np.asarray(posicao) + 1.0) * np.pi / 4.0
    return np.stack([mono * np.cos(angulo) * np.sqrt(2.0), mono * np.sin(angulo) * np.sqrt(2.0)], axis=1)


def harmonicos(ph, f, ganho_k, teto=10000.0, k_max=64, cosseno=False):
    """Soma de harmônicos de uma fase acumulada `ph` (frequência `f` por amostra).

    Com senos e ganho 1/k sai o dente de serra; com cossenos e ganho sen(pi k D)/k, a onda
    de pulso de largura D (a quadrada do 8-bit com D = 0,5). Cada harmônico some em rampa
    quando passa do teto, em vez de cortar seco: harmônico que liga e desliga no meio do
    som estala, e o que passa de 24 kHz volta rebatido como chiado.
    """
    onda = np.cos if cosseno else np.sin
    y = np.zeros(len(ph))
    for k in range(1, k_max + 1):
        g = ganho_k(k)
        if g == 0.0:
            continue
        peso = np.clip((teto - k * f) / (0.15 * teto), 0.0, 1.0)
        if not np.any(peso):
            break
        y += g * peso * onda(k * ph)
    return y


def ruido_lento(rng, n, taxa, minimo, maximo):
    """Um valor sorteado `taxa` vezes por segundo, ligado em linha reta: tremor, sílaba, oscilação."""
    pontos = rng.uniform(minimo, maximo, int(n / SR * taxa) + 3)
    return np.interp(np.arange(n) / SR * taxa, np.arange(len(pontos)), pontos)


# ---------------------------------------------------------------------------
# As seis da 3.0. Com p = {} cada função calcula exatamente o som de antes.
# ---------------------------------------------------------------------------

def som_whoosh(rng, p):
    dur, pico = p.get("dur", 0.45), p.get("pico", 0.20)
    t = eixo(dur)
    n = len(t)
    # a frequência central sobe até o pico e desce depois, em escala logarítmica
    f_ini, f_pico, f_fim = p.get("f", (380.0, 2000.0, 650.0))
    lf = np.where(t < pico,
                  np.log(f_ini) + (np.log(f_pico) - np.log(f_ini)) * suave(t / pico),
                  np.log(f_pico) + (np.log(f_fim) - np.log(f_pico)) * suave((t - pico) / (dur - pico)))
    fc = np.exp(lf)
    q = p.get("q", 1.15) + p.get("q_pico", 0.45) * np.exp(-((t - pico) / 0.06) ** 2)   # um fio de ar mais definido no pico
    # envelope de passagem: chega, passa e vai embora um pouco mais devagar do que chegou
    largura = np.where(t < pico, p.get("chega", 0.072), p.get("vai", 0.095))
    envelope = (1.0 + ((t - pico) / largura) ** 2) ** -1.5
    # corpo: ruído grave abafado, só em volta do pico, para o ar não ficar magro
    corpo_env = np.exp(-((t - pico) / 0.07) ** 2)
    comum = ruido_rosa(rng, n)
    canais = []
    for _ in range(2):
        ruido = 0.8 * comum + 0.6 * ruido_rosa(rng, n)   # os dois lados parecidos, não iguais
        _, ar, _ = svf(ruido, fc, q)
        ar, _, _ = svf(ar, p.get("teto", 5500.0), 0.7)  # sem o chiado acima de 5,5 kHz
        _, grave, _ = svf(ruido, p.get("f_corpo", 300.0), 0.9)   # o corpo mora entre 150 e 600 Hz
        canais.append(ar / rms(ar) * envelope + p.get("corpo", 0.30) * grave / rms(grave) * corpo_env)
    x = np.stack(canais, axis=1)
    # passa de um lado para o outro, com potência constante e sem chegar nas pontas
    pan_ini, pan_larg = p.get("pan", (-0.35, 0.70))
    posicao = pan_ini + pan_larg * suave(t / dur)
    angulo = (posicao + 1.0) * np.pi / 4.0
    x[:, 0] *= np.cos(angulo) * np.sqrt(2.0)
    x[:, 1] *= np.sin(angulo) * np.sqrt(2.0)
    return x, (0.004, 0.030)


def som_pop(rng, p):
    dur = p.get("dur", 0.08)
    t = eixo(dur)
    n = len(t)
    # a bolha: o tom sobe de ~470 Hz para ~1 kHz enquanto some
    f = p.get("f0", 470.0) * (1.0 + p.get("sobe", 1.2) * (1.0 - np.exp(-t / p.get("sobe_tau", 0.014))))
    ph = fase(f)
    tom = (np.sin(ph) + p.get("h2", 0.07) * np.sin(2.0 * ph)) * np.exp(-t / p.get("tau", 0.017)) * ataque(t, 0.0015)
    # o estouro: 2 ms de ar agudo, bem baixo, só para dar contorno ao começo
    _, sopro, _ = svf(rng.standard_normal(n), p.get("f_sopro", 3600.0), 0.9)
    sopro = sopro / rms(sopro) * np.exp(-t / 0.0015) * ataque(t, 0.0003)
    return estereo(tom + p.get("sopro", 0.06) * sopro), (0.0005, 0.010)


def som_tick(rng, p):
    dur = p.get("dur", 0.02)
    t = eixo(dur)
    n = len(t)
    esc, tau = p.get("esc", 1.0), p.get("tau", 1.0)
    parciais = [(2350.0 * esc, 0.0022 * tau, 1.00),                    # o estalo
                (4700.0 * esc, 0.0010 * tau, p.get("brilho", 0.25)),   # o brilho, que some primeiro
                (1180.0 * esc, 0.0035 * tau, p.get("corpo", 0.35))]    # o corpo
    x = sum(a * np.sin(2.0 * np.pi * f * t) * np.exp(-t / tau_k) for f, tau_k, a in parciais)
    _, ar, _ = svf(rng.standard_normal(n), 5000.0, 0.8)
    x = x + 0.08 * ar / rms(ar) * np.exp(-t / 0.0006)
    return estereo(x * ataque(t, 0.0003)), (0.0002, 0.004)


def som_clique(rng, p):
    dur = p.get("dur", 0.04)
    t = eixo(dur)
    n = len(t)
    esc = p.get("esc", 1.0)
    _, ar, _ = svf(rng.standard_normal(n), 4200.0, 0.8)
    ar = ar / rms(ar)

    def estalo(inicio, escala, ganho):
        tt = t - inicio
        y = np.zeros(n)
        vivo = tt >= 0
        for f, tau, a in [(1750.0, 0.0040, 1.00), (3500.0, 0.0018, 0.40), (720.0, 0.0060, 0.30)]:
            y[vivo] += a * np.sin(2.0 * np.pi * (f * esc) * escala * tt[vivo]) * np.exp(-tt[vivo] / tau)
        y[vivo] += 0.22 * ar[vivo] * np.exp(-tt[vivo] / 0.0008)
        return ganho * y * ataque(tt, 0.0003)

    # apertar e, 11 ms depois, soltar: mais fraco e um pouco mais agudo
    x = estalo(0.0, 1.0, 1.0) + estalo(p.get("vao", 0.011), p.get("solta_esc", 1.12), p.get("solta", 0.32))
    return estereo(x), (0.0002, 0.006)


def som_subida(rng, p):
    dur, pico = p.get("dur", 0.50), p.get("pico", 0.47)
    t = eixo(dur)
    n = len(t)
    u = np.clip(t / pico, 0.0, 1.0)
    envelope = u ** 2.4
    # o ar: uma banda de ruído que abre de 450 Hz até 4 kHz
    fc_ini, fc_fim = p.get("fc", (450.0, 4000.0))
    fc = fc_ini * (fc_fim / fc_ini) ** (u ** 1.3)
    comum = ruido_rosa(rng, n)
    canais = []
    for lado, desafino in ((0, -1.0), (1, 1.0)):
        ruido = 0.8 * comum + 0.6 * ruido_rosa(rng, n)
        _, ar, _ = svf(ruido, fc, 1.0)
        ar, _, _ = svf(ar, 7000.0, 0.7)
        ar /= rms(ar)
        # o acorde: tônica, quinta, oitava e décima segunda, subindo uma quarta (5 semitons),
        # cada lado desafinado 6 cents para um brilho largo, sem cara de apito
        f0 = (p.get("f0", 330.0) * 2.0 ** ((p.get("intervalo", 5.0) / 12.0) * u ** 1.5)
              * 2.0 ** (desafino * p.get("cents", 6.0) / 1200.0))
        ph = fase(f0)
        tom = (np.sin(ph) + 0.6 * np.sin(1.5 * ph) + 0.45 * np.sin(2.0 * ph) + 0.15 * np.sin(3.0 * ph))
        tom /= rms(tom)
        canais.append((ar + p.get("tom", 0.35) * tom) * envelope)
    x = np.stack(canais, axis=1)
    return x, (0.002, 0.030)


def som_clarao(rng, p):
    dur = p.get("dur", 0.35)
    t = eixo(dur)
    n = len(t)
    # corpo: uma senoide que cai de 110 para 58 Hz, curta, só para dar peso
    f_fim, f_salto = p.get("corpo_f", (58.0, 52.0))
    f = f_fim + f_salto * np.exp(-t / 0.045)
    corpo = np.sin(fase(f)) * np.exp(-t / p.get("corpo_tau", 0.075)) * ataque(t, 0.006)
    # sopro: ruído num passa-baixa que fecha de 2,8 kHz para 450 Hz, o impacto que o celular toca
    s_fim, s_salto = p.get("sopro_f", (450.0, 2350.0))
    fc = s_fim + s_salto * np.exp(-t / 0.05)
    sopro, _, _ = svf(ruido_rosa(rng, n), fc, 0.8)
    _, _, sopro = svf(sopro, 110.0, 0.7)             # o grave quem dá é o corpo, não o ruído
    sopro = sopro / rms(sopro) * np.exp(-t / p.get("sopro_tau", 0.06)) * ataque(t, 0.004)
    canais = []
    for _ in range(2):
        # brilho: ar agudo, diferente em cada lado, que abre o estéreo como a luz do clarão
        _, brilho, _ = svf(rng.standard_normal(n), p.get("brilho_f", 6500.0), 0.7)
        brilho = brilho / rms(brilho) * np.exp(-t / p.get("brilho_tau", 0.11)) * ataque(t, 0.012)
        canais.append(p.get("corpo", 0.22) * corpo / rms(corpo) + 1.0 * sopro + p.get("brilho", 0.22) * brilho)
    x = np.stack(canais, axis=1)
    x = reverb_curto(x, rng, cauda=p.get("cauda", 0.07), mistura=p.get("mistura", 0.22))
    return x, (0.001, 0.040)


# ---------------------------------------------------------------------------
# As nove da 4.0
# ---------------------------------------------------------------------------

def som_glitch(rng, p):
    """Estalos digitais: grãos de 8 a 40 ms, cada um um defeito diferente, em lados diferentes."""
    dur = p.get("dur", 0.24)
    t = eixo(dur)
    n = len(t)
    x = np.zeros((n, 2))
    graos = p.get("graos", 6)
    curto_l, longo_l = p.get("largura", (0.010, 0.038))
    inicios = np.sort(np.concatenate([[0.0], rng.uniform(0.012, dur * 0.70, graos - 1)]))
    for i, t0 in enumerate(inicios):
        largura = min(rng.uniform(curto_l, longo_l), dur - t0 - 0.006)
        m = int(largura * SR)
        if m < 96:
            continue
        a = int(round(t0 * SR))
        tt = np.arange(m) / SR
        tipo = 0 if i == 0 else int(rng.integers(3))   # o primeiro é sempre o estalo de bits, o mais forte
        if tipo == 0:
            # bits esmagados: ruído retido em 1,8 a 5 kHz e quantizado em 2 a 4 bits
            passo = max(1, int(SR / rng.uniform(*p.get("taxa", (1800.0, 5200.0)))))
            niveis = 2 ** int(rng.integers(2, 5))
            fonte = np.repeat(rng.standard_normal(m // passo + 1), passo)[:m]
            seg = np.round(np.clip(fonte / 2.5, -1.0, 1.0) * (niveis / 2)) / (niveis / 2)
        elif tipo == 1:
            # tom quadrado que salta no meio (uma quarta, quinta ou oitava)
            f1 = rng.uniform(*p.get("tom", (520.0, 2200.0)))
            salto = float(rng.choice(np.array([-7.0, -5.0, 5.0, 7.0, 12.0])))
            f = np.where(tt < largura / 2, f1, f1 * 2.0 ** (salto / 12.0))
            seg = np.sign(np.sin(fase(f)))
        else:
            # gagueira: um pedaço de 3 a 7 ms de zumbido repetido
            pedaco = int(rng.uniform(0.003, 0.007) * SR)
            _, fonte, _ = svf(rng.standard_normal(pedaco * 2), rng.uniform(900.0, 3200.0), 2.0)
            fonte = fonte[pedaco:] * np.hanning(pedaco)
            seg = np.tile(fonte, m // pedaco + 1)[:m]
        envelope = ataque(tt, 0.0008) * descida(tt, largura - 0.0015, 0.0015)
        ganho = (p.get("cai", 0.86) ** i) * (1.0 if i == 0 else rng.uniform(0.55, 1.0))
        lado = 0.0 if i == 0 else rng.uniform(-0.65, 0.65)
        x[a:a + m] += pan(seg / rms(seg) * envelope * ganho, lado)
    # tudo por um passa-baixa em 9 kHz: o defeito é digital, mas não fere
    for c in range(2):
        x[:, c], _, _ = svf(x[:, c], p.get("teto", 9000.0), 0.7)
    return x, (0.0005, 0.006)


def som_rebobina(rng, p):
    """Fita acelerando: o conteúdo da fita sobe de velocidade (e de altura), com wow e flutter."""
    dur = p.get("dur", 0.60)
    t = eixo(dur)
    n = len(t)
    u = t / dur
    v0, v1 = p.get("vel", (0.6, 4.5))
    vel = v0 * (v1 / v0) ** (u ** p.get("curva", 1.6))
    # wow (o prato balançando, ~5 Hz) e flutter (o cabrestante, ~17 Hz)
    vel = (vel * (1.0 + p.get("wow", 0.04) * np.sin(2.0 * np.pi * 5.3 * t + rng.uniform(0.0, 2.0 * np.pi)))
           * (1.0 + 0.012 * np.sin(2.0 * np.pi * 17.0 * t + rng.uniform(0.0, 2.0 * np.pi))))
    # a "fala" da fita: um tom com formantes que sobem com a velocidade, picado em sílabas
    f0 = p.get("f0", 150.0) * vel
    ph = fase(f0)
    tempo_fita = np.cumsum(vel) / SR
    pontos = rng.uniform(0.15, 1.0, int(tempo_fita[-1] * 7.0) + 3)
    silabas = np.interp(tempo_fita * 7.0, np.arange(len(pontos)), pontos)
    tom = np.zeros(n)
    for k in range(1, 48):
        fk = k * f0
        amp = sum(a * np.exp(-0.5 * (np.log(fk / (ff * vel)) / 0.32) ** 2)
                  for ff, a in ((700.0, 1.0), (1250.0, 0.65), (2600.0, 0.35)))
        tom += amp / np.sqrt(k) * np.clip((11000.0 - fk) / 1500.0, 0.0, 1.0) * np.sin(k * ph)
    # perto do fim a fita corre rápido demais para ter sílaba: o som fica cheio até travar
    silabas = 1.0 - (1.0 - silabas) * (1.0 - u ** 2)
    tom = tom / rms(tom) * silabas
    # o chiado da fita abre junto com a velocidade
    fc = np.clip(1100.0 * vel, 400.0, 9000.0)
    canais = []
    for atraso in (0, int(0.0004 * SR)):
        _, chiado, _ = svf(ruido_rosa(rng, n), fc, 0.8)
        lado = np.concatenate([np.zeros(atraso), tom[: n - atraso]]) + p.get("chiado", 0.35) * chiado / rms(chiado)
        canais.append(lado)
    x = np.stack(canais, axis=1)
    # a fita trava: 18 ms de queda e um estalo seco de mecanismo
    para = p.get("para", 0.92) * dur
    envelope = (u ** 2.0) * ataque(t, 0.02) * descida(t, para, 0.018)
    x = x * envelope[:, None]
    tt = t - para
    vivo = tt >= 0
    trava = np.zeros(n)
    for f, tau, a in ((1900.0, 0.0030, 1.0), (3700.0, 0.0012, 0.4), (820.0, 0.0050, 0.5)):
        trava[vivo] += a * np.sin(2.0 * np.pi * f * tt[vivo]) * np.exp(-tt[vivo] / tau)
    trava *= ataque(tt, 0.0003)
    x = x + estereo(p.get("trava", 0.55) * trava * np.max(np.abs(x)) / pico_de(trava))
    return x, (0.003, 0.010)


def som_impacto(rng, p):
    """Hit grave curto com corpo: a senoide que cai, saturada, o soco abafado e uma sala pequena."""
    dur = p.get("dur", 0.55)
    t = eixo(dur)
    n = len(t)
    f_fim, f_salto = p.get("f", (44.0, 76.0))
    f = f_fim + f_salto * np.exp(-t / p.get("queda", 0.035))
    sub = np.sin(fase(f)) * np.exp(-t / p.get("decai", 0.16)) * ataque(t, 0.003)
    drive = p.get("drive", 2.2)
    sub = np.tanh(drive * sub) / np.tanh(drive)   # a saturação dá os harmônicos que o celular toca
    # o soco: ruído abafado num passa-baixa que fecha em 10 ms
    fc = 250.0 + p.get("brilho", 2600.0) * np.exp(-t / 0.010)
    soco, _, _ = svf(ruido_rosa(rng, n), fc, 0.9)
    soco = soco * np.exp(-t / 0.022) * ataque(t, 0.0008)
    # o corpo: médio-grave curto, o "tum" da caixa
    _, corpo, _ = svf(rng.standard_normal(n), p.get("f_corpo", 190.0), 1.4)
    corpo = corpo * np.exp(-t / 0.05) * ataque(t, 0.002)
    # o estalo do golpe: 2 ms de médio-agudo, o que faz o hit existir no alto-falante do celular
    _, estalo, _ = svf(rng.standard_normal(n), 3200.0, 1.2)
    estalo = estalo * np.exp(-t / 0.002) * ataque(t, 0.0003)
    mono = (sub + p.get("soco", 0.7) * soco / pico_de(soco) + p.get("corpo", 0.5) * corpo / pico_de(corpo)
            + p.get("estalo", 0.3) * estalo / pico_de(estalo))
    x = reverb_curto(estereo(mono), rng, cauda=0.10, comprimento=0.40, mistura=p.get("sala", 0.18))
    return x, (0.0005, 0.060)


def som_estatica(rng, p):
    """Chiado de TV que liga e desliga: o tum ao ligar, o chiado tremulando, o zíper ao desligar."""
    dur = p.get("dur", 0.50)
    t = eixo(dur)
    n = len(t)
    tremor = ruido_lento(rng, n, 40.0, 0.55, 1.0)
    canais = []
    for _ in range(2):
        r = rng.standard_normal(n)
        _, _, r = svf(r, p.get("passa_alta", 350.0), 0.7)
        r, _, _ = svf(r, p.get("passa_baixa", 8500.0), 0.7)
        canais.append(r / rms(r))
    x = np.stack(canais, axis=1) * tremor[:, None]
    portas = p.get("portas", ((0.0, dur - 0.05),))
    envelope = sum(ataque(t - a, 0.003) * descida(t, b, 0.004) for a, b in portas)
    # o tubo liga com um golpe e assenta: o ponto forte fica sempre no começo, em cima do evento
    envelope = envelope * (0.62 + 0.38 * np.exp(-t / 0.06))
    x = x * envelope[:, None]
    # o tum de ligar: a rede elétrica (120, 240, 360 Hz) num golpe de 30 ms
    tum = sum(a * np.sin(2.0 * np.pi * f * t) for f, a in ((120.0, 1.0), (240.0, 0.5), (360.0, 0.3)))
    tum = tum * np.exp(-t / 0.03) * ataque(t, 0.002)
    # o zíper de desligar: desce de 2 kHz para 200 Hz em ~40 ms, baixinho
    fim = portas[-1][1]
    tz = np.maximum(t - fim, 0.0)
    ziper = np.sin(fase(200.0 + 1800.0 * np.exp(-tz / 0.012))) * np.exp(-tz / 0.02) * ataque(t - fim, 0.001)
    x = 0.9 * x + estereo(p.get("tum", 0.5) * tum / pico_de(tum) + p.get("ziper", 0.25) * ziper)
    return x, (0.0005, 0.012)


def som_energia(rng, p):
    """Zumbido que cresce, como carga: o tom sobe, o filtro abre e o tremolo acelera até o fim."""
    dur, pico = p.get("dur", 0.90), p.get("pico", 0.86)
    t = eixo(dur)
    n = len(t)
    u = np.clip(t / pico, 0.0, 1.0)
    fa, fb = p.get("f", (70.0, 390.0))
    f0 = fa * (fb / fa) ** (u ** 1.6)
    tremolo = 1.0 - p.get("trem_fundo", 0.35) * (0.5 + 0.5 * np.sin(fase(5.0 + p.get("trem", 24.0) * u ** 2)))
    fc = 300.0 + 4500.0 * u ** 1.5
    canais = []
    for lado in (-1.0, 1.0):
        ff = f0 * 2.0 ** (lado * 5.0 / 1200.0)
        ph = fase(ff)
        tom = harmonicos(ph, ff, lambda k: 1.0 / k, teto=9000.0, k_max=40)
        tom, _, _ = svf(tom / rms(tom), fc, 0.9)   # o filtro abre com a carga
        tom /= rms(tom)
        assobio = np.sin(fase(ff * p.get("assobio", 9.0) * (1.0 + 0.004 * np.sin(2.0 * np.pi * 7.0 * t)))) * u ** 3
        canais.append(tom * tremolo + p.get("assobio_ganho", 0.22) * assobio)
    x = np.stack(canais, axis=1) * (u ** 2.2)[:, None]
    _, ar, _ = svf(ruido_rosa(rng, n), 3000.0, 0.7)
    x = x + estereo(0.05 * ar / rms(ar) * u ** 2)
    return x, (0.002, 0.035)


def som_carimbo(rng, p):
    """Batida seca de borracha e madeira: o baque, os modos de madeira e o tapa do papel."""
    dur = p.get("dur", 0.14)
    t = eixo(dur)
    n = len(t)
    esc, amort = p.get("esc", 1.0), p.get("amort", 1.0)
    f = 105.0 * esc + 70.0 * esc * np.exp(-t / 0.008)
    baque = np.sin(fase(f)) * np.exp(-t / (0.028 * amort)) * ataque(t, 0.0012)
    madeira = sum(a * np.sin(2.0 * np.pi * fm * esc * t) * np.exp(-t / (tau * amort))
                  for fm, tau, a in ((640.0, 0.016, 0.55), (1190.0, 0.009, 0.32),
                                     (2300.0, 0.005, 0.16), (3400.0, 0.003, 0.08)))
    madeira = madeira * ataque(t, 0.0006)
    _, tapa, _ = svf(rng.standard_normal(n), 2400.0 * esc, 0.9)
    tapa = tapa * np.exp(-t / 0.0035) * ataque(t, 0.0003)
    mono = (p.get("baque", 0.7) * baque + p.get("madeira", 1.0) * madeira / pico_de(madeira)
            + p.get("tapa", 0.35) * tapa / pico_de(tapa))
    # o carimbo assenta: um segundo toque, fraco, alguns ms depois
    atraso = int(p.get("assenta", 0.007) * SR)
    mono = mono + 0.22 * np.concatenate([np.zeros(atraso), mono[: n - atraso]])
    x = reverb_curto(estereo(mono), rng, cauda=0.035, comprimento=0.15, mistura=p.get("sala", 0.12))
    return x, (0.0003, 0.020)


def som_bip(rng, p):
    """Bip de chip antigo: onda de pulso somada harmônico a harmônico e quantizada em 16 degraus."""
    dur = p.get("dur", 0.08)
    notas = p.get("notas", ((1568.0, 0.068),))
    t = eixo(dur)
    n = len(t)
    f = np.full(n, notas[-1][0])
    inicio = 0.0
    for freq, d in notas:
        f[(t >= inicio) & (t < inicio + d)] = freq
        inicio += d
    fim = inicio
    duty = p.get("duty", 0.5)
    onda = harmonicos(fase(f), f, lambda k: float(np.sin(np.pi * k * duty)) / k, teto=12000.0, k_max=40, cosseno=True)
    onda = onda / pico_de(onda)
    onda = np.round(onda * 8.0) / 8.0           # os 16 degraus do conversor de 4 bits
    onda, _, _ = svf(onda, 11000.0, 0.7)
    envelope = ataque(t, 0.001) * descida(t, fim - 0.006, 0.006)
    return estereo(onda * envelope), (0.0005, 0.004)


def som_obturador(rng, p):
    """Clique de câmera: o estalo que abre, a mola no meio e o estalo que fecha."""
    dur = p.get("dur", 0.20)
    t = eixo(dur)
    n = len(t)
    esc, vao = p.get("esc", 1.0), p.get("vao", 0.068)

    def estalo(inicio, brilho, ganho):
        tt = t - inicio
        vivo = (tt >= 0).astype(float)
        r = rng.standard_normal(n) * np.exp(-np.maximum(tt, 0.0) / 0.0025) * vivo
        y = np.zeros(n)
        for fm, q, a in ((2700.0, 5.0, 1.0), (4500.0, 6.0, 0.7), (7100.0, 4.0, 0.4 * brilho)):
            _, b, _ = svf(r, fm * esc, q)
            y += a * b
        baque = np.sin(2.0 * np.pi * 170.0 * esc * tt) * np.exp(-np.maximum(tt, 0.0) / 0.008) * vivo * ataque(tt, 0.0005)
        return ganho * (y / pico_de(y) + 0.5 * baque)

    abre = estalo(0.002, 1.0, 1.0)
    fecha = estalo(0.002 + vao, p.get("brilho_fecha", 1.3), p.get("fecha", 0.8))
    _, mola, _ = svf(rng.standard_normal(n), 1500.0 * esc, 2.5)
    mola = mola / rms(mola) * ataque(t - 0.006, 0.004) * descida(t, 0.002 + vao - 0.004, 0.004)
    x = estereo(abre + fecha + p.get("mola", 0.06) * mola)
    x = reverb_curto(x, rng, cauda=0.04, comprimento=0.18, mistura=0.15)
    return x, (0.0005, 0.020)


def som_raio(rng, p):
    """Estalo elétrico: o craque, o arco que zumbe e a crepitação cada vez mais rara."""
    dur = p.get("dur", 0.65)
    t = eixo(dur)
    n = len(t)
    # o craque: ruído brilhante de 3,5 ms e um baque de ar
    _, _, craque = svf(rng.standard_normal(n) * np.exp(-t / 0.0035), 900.0, 0.7)
    craque = craque * ataque(t, 0.0002)
    baque, _, _ = svf(ruido_rosa(rng, n), 400.0, 0.7)
    baque = baque * np.exp(-t / 0.05) * ataque(t, 0.001)
    # o arco: dente de serra com a frequência tremendo ±25%, misturado com ruído
    f_arco = p.get("f_arco", 115.0) * ruido_lento(rng, n, 1.0 / 0.012, 0.75, 1.25)
    arco = harmonicos(fase(f_arco), f_arco, lambda k: 1.0 / k, teto=7000.0, k_max=48)
    arco = arco / rms(arco) * (0.6 + 0.4 * ruido_lento(rng, n, 900.0, -1.0, 1.0))
    arco, _, _ = svf(arco, 6000.0, 0.7)
    arco = arco * ataque(t, 0.01) * np.exp(-t / p.get("arco_tau", 0.22))
    mono = (0.9 * craque / pico_de(craque) + 0.35 * baque / pico_de(baque)
            + p.get("arco", 0.45) * arco / pico_de(arco))
    canais = []
    for _ in range(2):
        # a crepitação: estalos soltos, densos no começo e cada vez mais raros, diferentes em cada lado
        taxa = p.get("taxa", 700.0) * np.exp(-t / 0.14) + 30.0
        impulsos = (rng.random(n) < taxa / SR) * rng.uniform(-1.0, 1.0, n)
        _, crepita, _ = svf(impulsos, p.get("crepita_f", 3800.0), 1.4)
        crepita = crepita / pico_de(crepita) * np.exp(-t / 0.3)
        canais.append(mono + p.get("crepita", 0.5) * crepita)
    return np.stack(canais, axis=1), (0.0002, 0.030)


# ---------------------------------------------------------------------------
# A biblioteca: família, base e variações
# ---------------------------------------------------------------------------
# Cada família tem o base (p = {}) e as variações, cada uma com os parâmetros que
# mudam e uma descrição curta. A ordem das famílias fixa a semente de cada uma:
# acrescente famílias novas no fim, para não mudar o som das que já existem.

SONS = [
    {"nome": "whoosh", "funcao": som_whoosh, "dur": 0.45,
     "uso": "transição (lâmina, chicote, desfoque, inclinada, mergulho, zoom-desfoque)",
     "desenho": "ruído numa banda que sobe e desce, da esquerda para a direita",
     "variacoes": [
         ({"dur": 0.30, "pico": 0.13, "f": (520.0, 2600.0, 900.0), "pan": (0.35, -0.70), "chega": 0.050, "vai": 0.070},
          "curto e mais agudo, da direita para a esquerda"),
         ({"dur": 0.62, "pico": 0.30, "f": (260.0, 1500.0, 420.0), "corpo": 0.45, "chega": 0.100, "vai": 0.140,
           "pan": (-0.45, 0.90)}, "longo e grave, abre mais o estéreo"),
         ({"dur": 0.40, "pico": 0.16, "f": (420.0, 3000.0, 800.0), "q_pico": 0.9, "corpo": 0.20, "pan": (0.30, -0.60)},
          "fio de ar mais definido no pico, da direita para a esquerda"),
         ({"dur": 0.52, "pico": 0.24, "f": (330.0, 1800.0, 500.0), "corpo": 0.38, "pan": (-0.15, 0.30), "teto": 4500.0},
          "médio e escuro, quase no centro"),
     ]},
    {"nome": "pop", "funcao": som_pop, "dur": 0.08,
     "uso": "elemento que entra (card, número, selo)",
     "desenho": "bolha curta: tom que sobe de altura enquanto some",
     "variacoes": [
         ({"dur": 0.07, "f0": 560.0, "sobe": 1.0}, "bolha menor, mais aguda"),
         ({"dur": 0.10, "f0": 400.0, "sobe": 1.4, "tau": 0.022}, "bolha maior, sobe mais"),
         ({"dur": 0.06, "f0": 660.0, "sobe": 0.9, "tau": 0.013, "sopro": 0.09}, "gota curta e clara"),
         ({"dur": 0.09, "f0": 430.0, "h2": 0.14, "sobe_tau": 0.020, "f_sopro": 2800.0}, "bolha redonda, sobe devagar"),
     ]},
    {"nome": "tick", "funcao": som_tick, "dur": 0.02,
     "uso": "contador correndo, item de lista",
     "desenho": "estalo seco e claro",
     "variacoes": [
         ({"esc": 0.85, "corpo": 0.45}, "madeira mais grave"),
         ({"esc": 1.15, "brilho": 0.32}, "mais agudo"),
         ({"dur": 0.025, "esc": 0.95, "tau": 1.3}, "um pouco mais longo, com mais ressonância"),
         ({"dur": 0.018, "esc": 1.25, "corpo": 0.20}, "agulha: curto, agudo e magro"),
     ]},
    {"nome": "clique", "funcao": som_clique, "dur": 0.04,
     "uso": "destaque que acende, marca, botão",
     "desenho": "clique de interface: apertar e soltar",
     "variacoes": [
         ({"esc": 0.90, "vao": 0.009}, "um pouco mais grave, soltar mais rápido"),
         ({"esc": 1.10, "vao": 0.014, "solta": 0.25}, "mais agudo, soltar mais fraco"),
         ({"dur": 0.045, "esc": 0.80, "vao": 0.012, "solta_esc": 1.20}, "botão grande, mais grave"),
         ({"dur": 0.035, "esc": 1.20, "vao": 0.010, "solta": 0.40}, "tecla pequena e clara"),
     ]},
    {"nome": "subida", "funcao": som_subida, "dur": 0.50,
     "uso": "o instante antes de uma revelação; termina em cima do evento",
     "desenho": "riser: ar abrindo para o agudo e um acorde baixo subindo uma quarta",
     "variacoes": [
         ({"dur": 0.40, "pico": 0.375, "f0": 370.0, "intervalo": 7.0}, "mais curto, sobe uma quinta"),
         ({"dur": 0.65, "pico": 0.61, "f0": 294.0, "fc": (350.0, 3500.0)}, "mais longo e mais grave"),
         ({"dur": 0.55, "pico": 0.52, "f0": 349.0, "intervalo": 3.0, "tom": 0.25}, "mais ar, sobe uma terça"),
         ({"dur": 0.45, "pico": 0.42, "f0": 311.0, "tom": 0.50, "fc": (450.0, 5000.0)}, "mais acorde e mais brilho no fim"),
     ]},
    {"nome": "clarao", "funcao": som_clarao, "dur": 0.35,
     "uso": "a transição clarão",
     "desenho": "impacto suave: corpo grave curto, sopro médio e brilho de ar",
     "variacoes": [
         ({"dur": 0.30, "corpo_f": (65.0, 55.0), "brilho_tau": 0.09}, "mais curto, corpo mais alto"),
         ({"dur": 0.45, "corpo_f": (50.0, 45.0), "corpo_tau": 0.09, "mistura": 0.30}, "mais grave, com mais sala"),
         ({"dur": 0.32, "brilho": 0.32, "sopro_tau": 0.05, "brilho_f": 7500.0}, "mais brilho de ar"),
         ({"dur": 0.40, "corpo_f": (62.0, 48.0), "sopro_f": (400.0, 2000.0), "corpo": 0.30}, "sopro mais escuro, mais corpo"),
     ]},
    {"nome": "glitch", "funcao": som_glitch, "dur": 0.24,
     "uso": "transição glitch, palavra decodifica/pixel, erro, virada de opinião",
     "desenho": "estalos digitais: bits esmagados, tom quadrado que salta e gagueira",
     "variacoes": [
         ({"dur": 0.18, "graos": 5, "largura": (0.008, 0.028)}, "curto e mais picado"),
         ({"dur": 0.30, "graos": 7, "taxa": (1200.0, 3600.0), "cai": 0.90}, "mais longo, bits mais grossos"),
         ({"dur": 0.22, "graos": 4, "tom": (900.0, 3000.0), "teto": 10000.0}, "poucos grãos, mais agudo"),
     ]},
    {"nome": "rebobina", "funcao": som_rebobina, "dur": 0.60,
     "uso": "transição vhs, volta no tempo, \"pera, volta\"; termina em cima do corte",
     "desenho": "fita acelerando com wow e flutter, chiado que abre e a trava seca no fim",
     "variacoes": [
         ({"dur": 0.45, "vel": (0.8, 5.0), "f0": 170.0}, "rebobinada curta"),
         ({"dur": 0.75, "vel": (0.5, 4.0), "wow": 0.06, "curva": 1.3}, "mais longa, mais wow"),
         ({"dur": 0.55, "vel": (0.7, 5.5), "f0": 130.0, "chiado": 0.5, "trava": 0.4}, "mais chiado, trava mais leve"),
     ]},
    {"nome": "impacto", "funcao": som_impacto, "dur": 0.55,
     "uso": "momento-herói, número grande, revelação, palavra brutal (só peso 3)",
     "desenho": "hit grave curto: senoide que cai saturada, soco abafado e sala pequena",
     "variacoes": [
         ({"dur": 0.45, "f": (50.0, 70.0), "decai": 0.12, "brilho": 3200.0}, "mais curto e mais seco"),
         ({"dur": 0.70, "f": (38.0, 80.0), "decai": 0.22, "sala": 0.25}, "mais grave e mais longo"),
         ({"dur": 0.50, "f": (46.0, 90.0), "soco": 0.95, "f_corpo": 240.0, "drive": 3.0, "estalo": 0.4}, "mais soco, mais saturado"),
     ]},
    {"nome": "estatica", "funcao": som_estatica, "dur": 0.50,
     "uso": "look crt/vhs ligando, moldura-crt, transição vhs/pixels, liga/desliga de tela",
     "desenho": "chiado de TV que liga e desliga, com o tum da rede e o zíper",
     "variacoes": [
         ({"dur": 0.35, "portas": ((0.0, 0.30),)}, "liga e desliga curto"),
         ({"dur": 0.70, "portas": ((0.0, 0.22), (0.27, 0.45), (0.49, 0.64))}, "falhando: apaga e volta duas vezes"),
         ({"dur": 0.45, "passa_alta": 600.0, "passa_baixa": 4000.0, "portas": ((0.0, 0.40),)}, "abafado, como rádio"),
     ]},
    {"nome": "energia", "funcao": som_energia, "dur": 0.90,
     "uso": "mãos (energia, aura, feixe, raio), carga antes do herói; termina no evento",
     "desenho": "zumbido que cresce: tom que sobe, filtro que abre, tremolo que acelera",
     "variacoes": [
         ({"dur": 0.70, "pico": 0.66, "f": (90.0, 440.0)}, "carga curta"),
         ({"dur": 1.10, "pico": 1.06, "f": (55.0, 330.0), "trem": 30.0}, "carga longa e grave"),
         ({"dur": 0.80, "pico": 0.76, "assobio": 12.0, "assobio_ganho": 0.30, "trem_fundo": 0.25}, "mais assobio, menos tremolo"),
     ]},
    {"nome": "carimbo", "funcao": som_carimbo, "dur": 0.14,
     "uso": "palavra carimbo/marcatexto, selo que bate, papel, recorte",
     "desenho": "batida seca de borracha e madeira, com o segundo toque assentando",
     "variacoes": [
         ({"esc": 0.85, "amort": 1.2}, "mais grave, borracha mais mole"),
         ({"esc": 1.20, "amort": 0.8, "tapa": 0.5}, "madeira mais dura, mais papel"),
         ({"dur": 0.16, "esc": 1.0, "assenta": 0.011, "sala": 0.18}, "carimbo que assenta devagar"),
     ]},
    {"nome": "bip", "funcao": som_bip, "dur": 0.08,
     "uso": "transição pixels, palavra pixel, contador digital, mira travando, terminal",
     "desenho": "bip de chip antigo: onda quadrada em 16 degraus",
     "variacoes": [
         ({"dur": 0.09, "notas": ((1046.5, 0.035), (1568.0, 0.043))}, "duas notas subindo"),
         ({"dur": 0.12, "notas": ((1046.5, 0.108),), "duty": 0.25}, "um bip mais longo e mais anasalado"),
         ({"dur": 0.09, "notas": ((2093.0, 0.026), (1568.0, 0.026), (1318.5, 0.026))}, "arpejo descendo"),
     ]},
    {"nome": "obturador", "funcao": som_obturador, "dur": 0.20,
     "uso": "polaroid, foto, flash branco, print entrando, congela + recorte",
     "desenho": "clique de câmera: o estalo que abre, a mola e o estalo que fecha",
     "variacoes": [
         ({"dur": 0.16, "vao": 0.045, "esc": 1.10}, "câmera pequena, rápida"),
         ({"dur": 0.24, "vao": 0.095, "esc": 0.90, "mola": 0.10}, "câmera grande, mola mais longa"),
         ({"dur": 0.20, "vao": 0.075, "fecha": 0.85, "brilho_fecha": 1.0, "esc": 0.95}, "os dois estalos quase iguais"),
     ]},
    {"nome": "raio", "funcao": som_raio, "dur": 0.65,
     "uso": "mãos raio/faíscas, palavra neon acendendo, curto-circuito",
     "desenho": "estalo elétrico: craque, arco que zumbe e crepitação",
     "variacoes": [
         ({"dur": 0.50, "arco_tau": 0.15, "taxa": 900.0}, "curto, mais crepitação"),
         ({"dur": 0.80, "f_arco": 90.0, "arco_tau": 0.30, "arco": 0.55}, "arco mais grave e mais longo"),
         ({"dur": 0.60, "f_arco": 150.0, "crepita_f": 5000.0, "crepita": 0.65}, "faísca mais aguda"),
     ]},
]


def arquivos_da_biblioteca(familias):
    """[(nome do arquivo sem .wav, família, k da variação ou 0, parâmetros, duração, descrição)]."""
    lista = []
    for f in familias:
        lista.append((f["nome"], f, 0, {}, f["dur"], f["desenho"]))
        for k, (params, descricao) in enumerate(f["variacoes"], start=1):
            lista.append(("%s-%d" % (f["nome"], k), f, k, params, params.get("dur", f["dur"]), descricao))
    return lista



# ---------------------------------------------------------------------------
# Medidas
# ---------------------------------------------------------------------------

def resposta_biquad(b, a, w):
    z1 = np.exp(-1j * w)
    z2 = z1 * z1
    return (b[0] + b[1] * z1 + b[2] * z2) / (a[0] + a[1] * z1 + a[2] * z2)


def ponderar_k(x):
    """Aplica a ponderação K no espectro (os dois biquads da BS.1770, de uma vez só)."""
    n = len(x)
    m = 1 << int(np.ceil(np.log2(n + SR // 2)))
    espectro = np.fft.rfft(x, m, axis=0)
    w = 2.0 * np.pi * np.arange(espectro.shape[0]) / m
    h = resposta_biquad(*K_PRATELEIRA, w) * resposta_biquad(*K_PASSA_ALTA, w)
    return np.fft.irfft(espectro * h[:, None], m, axis=0)[:n]


def nivel_curto(x, janela=0.100):
    """O volume do som no seu momento mais forte: janela de 100 ms, ponderação K, em LUFS.

    Som mais curto que a janela é medido com silêncio em volta, porque o ouvido
    também soma a energia por perto de um décimo de segundo: um tique de 20 ms
    soa mais fraco do que um tom de 100 ms com o mesmo pico.
    """
    w = int(janela * SR)
    y = ponderar_k(np.pad(x, ((w, w), (0, 0))))
    p = np.sum(y ** 2, axis=1)
    acumulado = np.concatenate([[0.0], np.cumsum(p)])
    media = (acumulado[w:] - acumulado[:-w]) / w
    return -0.691 + 10.0 * np.log10(max(float(np.max(media)), 1e-20))


def pico_verdadeiro(x):
    """Pico entre amostras, com sobreamostragem de 4x feita no espectro."""
    n = len(x)
    m = 1 << int(np.ceil(np.log2(n + 2048)))
    espectro = np.fft.rfft(x, m, axis=0)
    maior = np.zeros((2 * m + 1, x.shape[1]), dtype=complex)
    maior[: espectro.shape[0]] = espectro
    y = np.fft.irfft(maior, 4 * m, axis=0) * 4.0
    return float(np.max(np.abs(y)))


def ponto_forte(x):
    """Onde o som é mais forte: o máximo da energia alisada por uma janela de Hann de 20 ms.

    É a mesma conta do audio.py, que alinha esse instante no tempo do evento.
    """
    w = int(0.020 * SR) | 1
    p = np.sum(x.astype(float) ** 2, axis=1)
    h = np.hanning(w)
    return float(np.argmax(np.convolve(np.pad(p, (w // 2, w // 2)), h / h.sum(), mode="valid"))) / SR


def centroide(x):
    mono = x.mean(axis=1)
    espectro = np.abs(np.fft.rfft(mono, 1 << int(np.ceil(np.log2(len(mono) + 1))))) ** 2
    f = np.fft.rfftfreq(2 * (len(espectro) - 1), 1.0 / SR)
    return float(np.sum(f * espectro) / max(np.sum(espectro), 1e-20))


def db(v):
    return 20.0 * np.log10(max(abs(v), 1e-12))


def perfil(x):
    """O espectro do som em bandas de terço de oitava, de 50 Hz a 16 kHz, em dB abaixo da banda mais forte.

    Serve para medir se uma variação é outra mesmo, e não o base com outro grão de ruído.
    """
    mono = x.mean(axis=1)
    m = 1 << int(np.ceil(np.log2(len(mono) + 1)))
    espectro = np.abs(np.fft.rfft(mono, m)) ** 2
    f = np.fft.rfftfreq(m, 1.0 / SR)
    centros = 50.0 * 2.0 ** (np.arange(26) / 3.0)
    bandas = np.array([np.sum(espectro[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))]) for c in centros])
    bandas = 10.0 * np.log10(np.maximum(bandas, 1e-20))
    return np.maximum(bandas - bandas.max(), -60.0)


def medir(inteiro):
    """Mede o som exatamente como ele vai para o disco (inteiros de 16 bits)."""
    x = inteiro.astype(float) / 32768.0
    return {
        "duracao": len(x) / SR,
        "pico": db(np.max(np.abs(x))),
        "pico_verdadeiro": db(pico_verdadeiro(x)),
        "rms": db(np.sqrt(np.mean(np.square(x)))),
        "dc": max(db(x[:, 0].mean()), db(x[:, 1].mean())),
        "pontas": int(max(np.max(np.abs(inteiro[0])), np.max(np.abs(inteiro[-1])))),
        "nivel": nivel_curto(x),
        "ponto_forte": ponto_forte(x),
        "centroide": centroide(x),
        "perfil": perfil(x),
    }


def conferir(m, dur_prevista, base=None):
    problemas = []
    if abs(m["duracao"] - dur_prevista) > 0.001:
        problemas.append("duração %.3f s, o previsto é %.3f s" % (m["duracao"], dur_prevista))
    if m["pico_verdadeiro"] > TETO_DBTP + 0.05:
        problemas.append("pico verdadeiro %.2f dBTP, acima do teto de %.0f" % (m["pico_verdadeiro"], TETO_DBTP))
    if m["dc"] > -70.0:
        problemas.append("componente contínua de %.0f dBFS (o limite é -70)" % m["dc"])
    if m["pontas"] > 1:
        problemas.append("a primeira ou a última amostra não está em zero (%d)" % m["pontas"])
    if m["rms"] < -60.0:
        problemas.append("o som saiu mudo (RMS %.0f dBFS)" % m["rms"])
    if base is not None and m["distancia"] < 0.5 and abs(m["duracao"] - base["duracao"]) < 0.005:
        problemas.append("a variação ficou igual ao base (%.2f dB de distância e a mesma duração)" % m["distancia"])
    return problemas


# ---------------------------------------------------------------------------
# Gravação
# ---------------------------------------------------------------------------

def sintetizar(funcao, params, semente, indice, k):
    # cada som com o seu ruído: mexer num não muda os outros. O base usa a semente da 3.0.
    rng = np.random.default_rng([semente, indice] if k == 0 else [semente, indice, k])
    x, (entrada, saida) = funcao(rng, params)
    if not np.all(np.isfinite(x)):
        raise ValueError("a síntese devolveu NaN ou infinito")
    x = zerar_media(fades(tirar_grave_inutil(x), entrada, saida))
    # o mesmo volume de curto prazo para todos, sem passar do teto de pico verdadeiro
    ganho = 10.0 ** ((NIVEL_CURTO - nivel_curto(x)) / 20.0)
    teto = 10.0 ** ((TETO_DBTP - 0.3) / 20.0) / pico_verdadeiro(x)
    x = x * min(ganho, teto)
    return np.round(np.clip(x, -1.0, 32767.0 / 32768.0) * 32768.0).astype("<i2")


def gravar_wav(caminho, inteiro):
    with wave.open(str(caminho), "wb") as arquivo:
        arquivo.setnchannels(2)
        arquivo.setsampwidth(2)
        arquivo.setframerate(SR)
        arquivo.writeframes(np.ascontiguousarray(inteiro).tobytes())


def ler_wav(caminho):
    with wave.open(str(caminho), "rb") as arquivo:
        if arquivo.getnchannels() != 2 or arquivo.getsampwidth() != 2 or arquivo.getframerate() != SR:
            return None
        dados = arquivo.readframes(arquivo.getnframes())
    return np.frombuffer(dados, dtype="<i2").reshape(-1, 2)


def virgula(v, casas):
    return ("%.*f" % (casas, v)).replace(".", ",")


def escrever_leia(pasta, medidas, semente):
    linhas = []
    for nome, familia, k, _, _, descricao in arquivos_da_biblioteca(SONS):
        m = medidas.get(nome)
        if m is None:
            continue
        linhas.append("| `%s.wav` | %s s | %s dBTP | %s s | %s | %s |" % (
            nome, virgula(m["duracao"], 2), virgula(m["pico_verdadeiro"], 1), virgula(m["ponto_forte"], 3),
            descricao if k == 0 else "variação: " + descricao, familia["uso"] if k == 0 else "↳"))
    familias = ", ".join("`%s`" % f["nome"] for f in SONS)
    texto = """# Sons do pacote

Os efeitos desta pasta são **obra do próprio pacote**. Foram calculados, amostra por amostra,
pelo `gerar_sons.py` (só numpy): ruído filtrado, senoides que decaem e envelopes. Não há gravação,
banco de sons nem trecho de obra de terceiro aqui dentro, então não há licença de ninguém para
respeitar. São livres: use, altere e distribua junto com os seus cortes e dentro do pacote,
inclusive em conteúdo pago ou patrocinado, sem crédito obrigatório.

São %d famílias: %s. Cada uma tem o **base**, com o nome da família (`whoosh.wav`), e as
**variações** numeradas (`whoosh-1.wav`, `whoosh-2.wav`...): o mesmo desenho com outro timbre, outra
duração ou outra altura. O base das seis famílias da 3.0 é o mesmo arquivo de antes, bit a bit.

| arquivo | duração | pico verdadeiro | ponto forte | o som | pensado para |
|---|---|---|---|---|---|
%s

**Ponto forte** é o instante em que o som é mais forte, contado do começo do arquivo. O `audio.py`
põe esse instante em cima do tempo do evento: o whoosh começa uns 0,2 s antes da transição e passa
por ela no auge; a subida, a energia e a rebobinada terminam em cima do que anunciam.

## Como o `audio.py` usa a família

O evento pede a família (`"som": "whoosh"`) e o `audio.py` escolhe o arquivo: o base ou uma das
variações, por um sorteio fixo (o hash do instante e do alvo do evento), nunca o mesmo arquivo em
dois eventos seguidos da mesma família. O mesmo corte sai sempre com os mesmos arquivos. Quem quer
um arquivo exato pede pelo nome dele (`"som": "whoosh-2"`), e aí não há sorteio. O contrato inteiro
está em `skills/produzir/motor/docs-4/variedade-e-som.md`.

## Formato

48 kHz, 16 bits, estéreo. Pico verdadeiro de no máximo -1 dBTP, sem componente contínua, com fade
nas duas pontas (a primeira e a última amostra são zero, então nada estala ao entrar ou sair). Todos
têm o mesmo volume de curto prazo, %s LUFS numa janela de 100 ms, para soarem parelhos quando
ouvidos soltos (o pico verdadeiro manda primeiro: o som muito seco fica um pouco abaixo). O volume
dentro do corte é decidido pelo `audio.py`, que mede a voz antes e põe cada efeito abaixo dela
(`--efeitos-db`, padrão -20 dB).

## Como refazer

```
flow-reels produzir/gerar_sons
flow-reels produzir/gerar_sons --so glitch,raio
```

Esta pasta foi gerada em %s com a semente %d. A mesma semente, no mesmo numpy, gera os mesmos
arquivos, bit a bit. Para outro grão de ruído do mesmo desenho, passe outra semente: `--semente 8`.
Para mudar o desenho (duração, timbre, envelope), o lugar é a função `som_<nome>` e a lista `SONS`
do `gerar_sons.py` (os parâmetros de cada variação), e a conferência no fim do script diz se o
resultado ainda está limpo e se cada variação continua diferente do base.

## Trocar um som pelo seu

Ponha o seu arquivo nesta pasta com o mesmo nome (`whoosh.wav`, `whoosh-3.wav`). O `audio.py`
acha sozinho o ponto forte de qualquer som e o volume dele, e uma variação a mais (`whoosh-5.wav`)
entra no sorteio da família sem mudar nada no código. Só lembre que rodar o `gerar_sons.py` de novo
grava por cima: guarde uma cópia do seu, e use som que você tem direito de usar.
""" % (len(SONS), familias, "\n".join(linhas), virgula(NIVEL_CURTO, 0),
       date.today().strftime("%d/%m/%Y"), semente)
    (pasta / "LEIA.md").write_text(texto, encoding="utf-8")


def main():
    global np
    ap = argparse.ArgumentParser(
        description="Sintetiza a biblioteca de efeitos sonoros do pacote: 15 famílias, cada uma com o base e as variações.")
    ap.add_argument("--saida", help="pasta da biblioteca (padrão: componentes/sons na raiz do pacote)")
    ap.add_argument("--semente", type=int, default=SEMENTE, help="fixa o ruído; a mesma semente gera os mesmos arquivos (padrão %d)" % SEMENTE)
    ap.add_argument("--so", help="só estas famílias, separadas por vírgula (ex.: glitch,raio)")
    args = ap.parse_args()

    if args.semente < 0:
        erro("--semente precisa ser um número inteiro de 0 para cima")
        return 2
    nomes = [f["nome"] for f in SONS]
    pedidas = set(nomes)
    if args.so:
        pedidas = {s.strip() for s in args.so.split(",") if s.strip()}
        desconhecidas = sorted(pedidas - set(nomes))
        if desconhecidas:
            erro("família desconhecida: %s (vale %s)" % (", ".join(desconhecidas), ", ".join(nomes)))
            return 2

    np = carregar_numpy()
    pasta = Path(args.saida) if args.saida else achar_raiz() / "componentes" / "sons"
    try:
        pasta.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        erro("não consegui criar a pasta %s: %s" % (pasta, e))
        return 2

    print("")
    print("  biblioteca de sons  ·  %s  ·  semente %d" % (pasta, args.semente))
    print("")
    print("  %-12s %9s %10s %11s %9s %6s %6s %10s %11s %9s %10s"
          % ("som", "duração", "pico", "pico verd.", "RMS", "DC", "pontas", "nível 100ms",
             "ponto forte", "centroide", "dist. base"))

    gerados, medidas, reprovas = {}, {}, []
    indice_de = {f["nome"]: i for i, f in enumerate(SONS)}
    for nome, familia, k, params, dur, _ in arquivos_da_biblioteca(SONS):
        if familia["nome"] not in pedidas:
            continue
        if k == 0:
            print("")
        try:
            inteiro = sintetizar(familia["funcao"], params, args.semente, indice_de[familia["nome"]], k)
        except ValueError as e:
            reprovas.append("%s: %s" % (nome, e))
            print("  %-12s REPROVADO: %s" % (nome, e))
            continue
        m = medir(inteiro)
        base = medidas.get(familia["nome"]) if k else None
        m["distancia"] = float(np.mean(np.abs(m["perfil"] - base["perfil"]))) if base else 0.0
        problemas = conferir(m, dur, base)
        gerados[nome], medidas[nome] = inteiro, m
        print("  %-12s %7.3f s %5.1f dBFS %6.1f dBTP %4.1f dBFS %6.0f %6d %6.1f LUFS %9.3f s %6.0f Hz %8s%s"
              % (nome, m["duracao"], m["pico"], m["pico_verdadeiro"], m["rms"], m["dc"], m["pontas"],
                 m["nivel"], m["ponto_forte"], m["centroide"],
                 ("%.1f dB" % m["distancia"]) if k else "base",
                 "" if not problemas else "   <- REPROVADO"))
        for p in problemas:
            reprovas.append("%s: %s" % (nome, p))

    print("")
    if reprovas:
        print("  REPROVADO: nada foi gravado.")
        for r in reprovas:
            print("    " + r)
        print("")
        return 1

    try:
        for nome, inteiro in gerados.items():
            gravar_wav(pasta / ("%s.wav" % nome), inteiro)
        # o LEIA.md mede a pasta inteira, inclusive o que esta rodada não refez (--so)
        todas = {}
        for nome, _, _, _, _, _ in arquivos_da_biblioteca(SONS):
            if nome in medidas:
                todas[nome] = medidas[nome]
            elif (pasta / ("%s.wav" % nome)).is_file():
                inteiro = ler_wav(pasta / ("%s.wav" % nome))
                if inteiro is not None and len(inteiro):
                    todas[nome] = medir(inteiro)
        escrever_leia(pasta, todas, args.semente)
    except OSError as e:
        erro("não consegui gravar em %s: %s" % (pasta, e))
        return 2

    print("  ok  pico verdadeiro de todos abaixo de %.0f dBTP, sem DC, pontas em zero, variações diferentes do base" % TETO_DBTP)
    print("  PASSOU: %d sons (%d famílias) e o LEIA.md gravados em %s"
          % (len(gerados), len({n.split("-")[0] for n in gerados}), pasta))
    print("")
    return 0


if __name__ == "__main__":
    sys.exit(main())
