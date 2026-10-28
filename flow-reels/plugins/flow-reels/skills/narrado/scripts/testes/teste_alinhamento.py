# -*- coding: utf-8 -*-
"""Testes do leitor de alinhamento da ElevenLabs (voz.py), sem chamar a API.

A resposta de exemplo e montada a mao no mesmo formato que a API devolve:
um tempo de inicio e de fim para cada caractere, inclusive espacos e colchetes.

Rodar:

    python skills/narrado/scripts/testes/teste_alinhamento.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import voz  # noqa: E402
import respirar  # noqa: E402


def alinhamento_de(texto, passo=0.05, pausas=None):
    """Monta um alinhamento falso: cada caractere dura 'passo'; pausas soma tempo extra
    depois do indice dado."""
    pausas = pausas or {}
    chars, ini, fim, t = [], [], [], 0.0
    for i, c in enumerate(texto):
        chars.append(c)
        ini.append(round(t, 3))
        t += passo
        fim.append(round(t, 3))
        t += pausas.get(i, 0.0)
    return {"characters": chars, "character_start_times_seconds": ini, "character_end_times_seconds": fim}


class TesteAlinhamento(unittest.TestCase):

    def test_palavras_e_tempos(self):
        al = alinhamento_de("Olha isso, agora.")
        p = voz.palavras_do_alinhamento(al)
        self.assertEqual([w["texto"] for w in p], ["Olha", "isso,", "agora."])
        self.assertAlmostEqual(p[0]["inicio"], 0.0)
        self.assertAlmostEqual(p[0]["fim"], 0.20)
        self.assertAlmostEqual(p[1]["inicio"], 0.25)
        self.assertAlmostEqual(p[2]["fim"], 0.85)

    def test_marcacao_entre_colchetes_some(self):
        al = alinhamento_de("[animado] Saiu a nova versao [pausa] hoje.")
        p = voz.palavras_do_alinhamento(al)
        self.assertEqual([w["texto"] for w in p], ["Saiu", "a", "nova", "versao", "hoje."])
        # o tempo de "Saiu" comeca no S, depois do colchete e do espaco
        self.assertAlmostEqual(p[0]["inicio"], round(len("[animado] ") * 0.05, 3))

    def test_colchete_grudado_na_palavra(self):
        al = alinhamento_de("agora[risos] sim")
        p = voz.palavras_do_alinhamento(al)
        self.assertEqual([w["texto"] for w in p], ["agora", "sim"])

    def test_pontuacao_solta_gruda_na_anterior(self):
        al = alinhamento_de("Espera ... olha")
        p = voz.palavras_do_alinhamento(al)
        self.assertEqual([w["texto"] for w in p], ["Espera...", "olha"])
        self.assertAlmostEqual(p[0]["fim"], 0.50)

    def test_acentos_e_numeros(self):
        al = alinhamento_de("Ele é 100% grátis, né?")
        p = voz.palavras_do_alinhamento(al)
        self.assertEqual([w["texto"] for w in p], ["Ele", "é", "100%", "grátis,", "né?"])

    def test_quebra_de_linha_separa(self):
        al = alinhamento_de("uma\nduas")
        p = voz.palavras_do_alinhamento(al)
        self.assertEqual([w["texto"] for w in p], ["uma", "duas"])

    def test_listas_de_tamanhos_diferentes(self):
        al = alinhamento_de("oi")
        al["character_end_times_seconds"].pop()
        with self.assertRaises(ValueError):
            voz.palavras_do_alinhamento(al)

    def test_prefere_alinhamento_original(self):
        resposta = {"alignment": alinhamento_de("Custa 10 reais."),
                    "normalized_alignment": alinhamento_de("Custa dez reais.")}
        al, qual = voz.escolher_alinhamento(resposta)
        self.assertEqual(qual, "alignment")
        self.assertEqual(voz.palavras_do_alinhamento(al)[1]["texto"], "10")

    def test_cai_no_normalizado(self):
        resposta = {"alignment": None, "normalized_alignment": alinhamento_de("Custa dez reais.")}
        al, qual = voz.escolher_alinhamento(resposta)
        self.assertEqual(qual, "normalized_alignment")

    def test_resposta_sem_alinhamento(self):
        with self.assertRaises(ValueError):
            voz.escolher_alinhamento({"audio_base64": ""})


class TesteRespiro(unittest.TestCase):

    def test_respiro_depois_de_frase(self):
        import numpy as np
        sr = 1000
        palavras = [{"texto": "Primeira.", "inicio": 0.0, "fim": 0.5},
                    {"texto": "Segunda", "inicio": 0.7, "fim": 1.0},
                    {"texto": "frase:", "inicio": 1.1, "fim": 1.4},
                    {"texto": "fim", "inicio": 1.6, "fim": 1.9}]
        audio = np.ones(2000, np.float32)
        novo, novas, n = respirar.respirar(audio, palavras, 0.2, sr=sr)
        self.assertEqual(n, 2)
        self.assertEqual(len(novo), 2000 + 2 * 200)
        self.assertAlmostEqual(novas[1]["inicio"], 0.9)
        self.assertAlmostEqual(novas[3]["inicio"], 2.0)
        # o silencio caiu no meio do vao entre 0.5 e 0.7
        self.assertTrue(np.all(novo[600:800] == 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
