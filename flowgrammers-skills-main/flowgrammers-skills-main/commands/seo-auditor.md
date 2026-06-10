---
name: seo-auditor
description: |
  Varre e otimiza arquivos de documentação para SEO. Audita arquivos README.md e páginas docs/ verificando
  meta tags, headings, palavras-chave, legibilidade, conteúdo duplicado e links quebrados. Aplica
  correções, atualiza sitemap.xml e gera um relatório. Uso: /seo-auditor [caminho]
---

# /seo-auditor

Varre, audita e otimiza sistematicamente arquivos de documentação para SEO. Foca em README.md e páginas docs/ — corrige problemas in-place, preserva rankings de páginas de alto desempenho e gera um relatório final.

## Uso

```bash
/seo-auditor                    # Audita todos os docs/ e README.md raiz
/seo-auditor docs/skills/       # Audita um subdiretório específico
/seo-auditor --report-only      # Varre sem fazer alterações
```

## O que faz

Executa todas as 7 fases sequencialmente. Corrige automaticamente problemas não destrutivos. Preserva conteúdo já bem posicionado. Reporta tudo ao final.

---

## Fase 1: Descoberta e Linha de Base

### 1a. Identificar arquivos alvo

```bash
find docs/ -name '*.md' -type f | sort
find . -maxdepth 2 -name 'README.md' -not -path './.codex/*' -not -path './.gemini/*' | sort
```

Classifica cada arquivo:
- **Novos/modificados recentemente** — arquivos alterados nos últimos 2 commits
- **Páginas índice** — arquivos `index.md` (alta autoridade, tratar com cuidado)
- **Páginas de skill** — `docs/skills/**/*.md`
- **Páginas estáticas** — `docs/index.md`, `docs/getting-started.md`, etc.
- **Arquivos README** — README.md raiz e de domínios

### 1b. Capturar linha de base

Para cada arquivo alvo, extrai o estado SEO atual: campo `title:`, campo `description:`, primeiro `# H1`, todos os H2/H3, contagem de palavras, links internos e externos.

---

## Fase 2: Auditoria de Meta Tags

### Tag de Título (`title:`)

- Deve existir e não estar vazia
- Tamanho ideal: 50–60 caracteres
- Deve conter uma palavra-chave principal
- Não deve duplicar o título de outra página

### Meta Descrição (`description:`)

- Deve existir e não estar vazia
- Tamanho: 120–160 caracteres
- Deve conter a palavra-chave principal de forma natural
- Deve ser única entre todas as páginas
- Não deve começar com "Esta página..." ou "Este documento..."

---

## Fase 3: Qualidade de Conteúdo e Legibilidade

### Estrutura de Headings

- Exatamente um `# H1` por página
- H2s seguem H1, H3s seguem H2 — sem pular níveis
- Headings devem conter palavras-chave de forma natural
- Sem headings duplicados na mesma página

### Legibilidade

Executa o pontuador de conteúdo em cada arquivo:

```bash
python3 marketing-skill/content-production/scripts/content_scorer.py {arquivo}
```

Metas: Legibilidade ≥ 70, Estrutura ≥ 60, Engajamento ≥ 50.

---

## Fase 4: Otimização de Palavras-chave

Para cada página, verifica se a palavra-chave principal aparece em:
- [ ] Tag de título
- [ ] Meta descrição
- [ ] Heading H1
- [ ] Primeiro parágrafo (dentro das primeiras 100 palavras)
- [ ] Pelo menos um H2
- [ ] Texto alternativo de imagens (se houver)

Densidade ideal: 1–2% para palavra-chave principal. Nenhuma inserção excessiva (acima de 3%).

**Importante:** Nunca altere URLs de páginas existentes.

---

## Fase 5: Auditoria de Links

### Links internos

Verifica todos os links markdown `[texto](url)`:
- Verifica se o destino existe
- Verifica links relativos quebrados
- Verifica links de âncora (`#seção`) para headings existentes

### Detecção de conteúdo duplicado

Compara meta descrições entre todas as páginas. Compara H1s — nenhuma página deve ter o mesmo H1.

### Detecção de páginas órfãs

Verifica se todas as páginas em `docs/` estão referenciadas no nav do `mkdocs.yml`.

---

## Fase 6: Sitemap e Build

```bash
mkdocs build
python3 marketing-skill/site-architecture/scripts/sitemap_analyzer.py site/sitemap.xml
```

Verifica que todas as páginas de documentação aparecem no sitemap, sem URLs quebradas.

---

## Fase 7: Relatório

```
╔══════════════════════════════════════════════════════════════╗
║  RELATÓRIO DO SEO AUDITOR                                   ║
╠══════════════════════════════════════════════════════════════╣
║  Páginas varridas:          {n}                              ║
║  Problemas encontrados:     {n}                              ║
║  Corrigidos automaticamente:{n}                              ║
║  Revisão manual necessária: {n}                              ║
║                                                              ║
║  META TAGS                                                   ║
║    Títulos otimizados:      {n}                              ║
║    Descrições corrigidas:   {n}                              ║
║    Títulos duplicados:      {n} → {n} (corrigido)            ║
║    Descs duplicadas:        {n} → {n} (corrigido)            ║
║                                                              ║
║  CONTEÚDO                                                    ║
║    Legibilidade melhorada:  {n} páginas                      ║
║    Correções de heading:    {n}                              ║
║                                                              ║
║  LINKS                                                       ║
║    Links quebrados:         {n} → {n} (corrigido)            ║
║    Páginas órfãs:           {n} → {n} (adicionado ao nav)    ║
║                                                              ║
║  SITEMAP                                                     ║
║    Total de URLs:           {n}                              ║
║    Sitemap regenerado:      ✅                               ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Referências de Skill

| Ferramenta | Caminho |
|------------|---------|
| Verificador SEO | `marketing-skill/seo-audit/scripts/seo_checker.py` |
| Pontuador de Conteúdo | `marketing-skill/content-production/scripts/content_scorer.py` |
| Pontuador de Humanização | `marketing-skill/content-humanizer/scripts/humanizer_scorer.py` |
| Otimizador SEO | `marketing-skill/content-production/scripts/seo_optimizer.py` |
| Analisador de Sitemap | `marketing-skill/site-architecture/scripts/sitemap_analyzer.py` |
