---
name: focused-fix
description: Correção profunda de feature — repara sistematicamente uma feature/módulo inteiro em todos os seus arquivos e dependências. Uso: /focused-fix <caminho-da-feature>
---

# /focused-fix

Repara sistematicamente uma feature ou módulo inteiro usando o protocolo de 5 fases. Alvo: `$ARGUMENTS` (caminho de feature ou nome de módulo).

Se `$ARGUMENTS` estiver vazio, pergunte ao usuário qual feature/módulo corrigir.

## Protocolo — Execute TODAS as 5 Fases EM ORDEM

### Fase 1: ESCOPO — Mapeie o Limite da Feature

1. Identifique a pasta/arquivos principais da feature alvo
2. Leia TODOS os arquivos dessa pasta — entenda seu propósito
3. Crie um manifesto da feature:

```
ESCOPO DA FEATURE:
  Caminho principal: <caminho>
  Pontos de entrada: [arquivos importados por outras partes do app]
  Arquivos internos: [arquivos usados apenas dentro desta feature]
  Total de arquivos: N
```

### Fase 2: RASTREAMENTO — Mapeie Todas as Dependências

**ENTRADA** (o que esta feature importa):
- Para cada instrução de importação, rastreie até a origem, verifique se existe e está exportada
- Verifique variáveis de ambiente, arquivos de config, modelos de DB, endpoints de API, pacotes de terceiros

**SAÍDA** (o que importa desta feature):
- Pesquise todo o codebase por importações desta feature
- Verifique se os consumidores usam a API/interface correta

Produza um mapa de dependências com entradas, saídas, variáveis de ambiente e arquivos de configuração.

### Fase 3: DIAGNÓSTICO — Encontre Todos os Problemas

Execute TODAS as verificações de diagnóstico:

- **Código**: importações resolvidas, sem dependências circulares, tipos consistentes, tratamento de erros, TODO/FIXME
- **Runtime**: variáveis de ambiente definidas, migrations atualizadas, shapes de API corretos
- **Testes**: execute TODOS os testes relacionados, registre falhas, verifique cobertura
- **Logs**: verifique git log para alterações recentes, pesquise logs de erro
- **Config**: valide arquivos de config, verifique divergências entre dev e prod

Para cada problema encontrado:
- Confirme a causa raiz com evidências antes de adicionar à lista de correções
- Atribua risco: ALTO (API pública, auth, >3 consumidores) / MÉDIO (interno com testes) / BAIXO (módulo folha)

Produza um relatório de diagnóstico com problemas agrupados por severidade.

### Fase 4: CORREÇÃO — Repare Sistematicamente

Corrija nesta ORDEM EXATA:
1. **Dependências** — importações quebradas, pacotes ausentes
2. **Tipos** — incompatibilidades de tipo nas fronteiras
3. **Lógica** — bugs de lógica de negócio
4. **Testes** — corrija ou crie testes para cada correção
5. **Integração** — verifique o fluxo completo com os consumidores

Regras:
- Corrija UM problema de cada vez, execute o teste relacionado após cada correção
- Se uma correção quebrar outra coisa → volte ao DIAGNÓSTICO
- Corrija ALTO antes de MÉDIO antes de BAIXO
- **Regra dos 3 Erros**: Se 3+ correções gerarem NOVOS problemas, PARE. Informe ao usuário que a arquitetura pode precisar de replanejamento, não de remendos.

### Fase 5: VERIFICAÇÃO — Confirme que Tudo Funciona

1. Execute TODOS os testes na pasta da feature
2. Execute TODOS os testes nos arquivos que importam desta feature
3. Execute o suite completo de testes se disponível
4. Resuma todas as alterações realizadas

Produza um relatório de conclusão com arquivos alterados, correções aplicadas, resultados dos testes e consumidores verificados.

## Lei de Ferro

```
SEM CORREÇÕES SEM COMPLETAR ESCOPO → RASTREAMENTO → DIAGNÓSTICO PRIMEIRO
```

Se você não completou a Fase 3, não pode propor correções.

## Skills Relacionadas

- `engineering/focused-fix` — SKILL.md completo com checklists detalhados, templates de saída e anti-padrões
- `superpowers:systematic-debugging` — Para bugs complexos individuais encontrados durante a Fase 3
