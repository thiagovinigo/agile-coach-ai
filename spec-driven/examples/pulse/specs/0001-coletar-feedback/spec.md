---
name: spec
description: Spec — Coletar feedback (exemplo golden). Base enquanto a feature está ativa.
alwaysApply: true
---

# Spec — Coletar feedback

## Resumo
O widget envia um feedback (texto + contexto) e o sistema o armazena, devolvendo um id.

## Critérios de aceite

### AC-1: feedback válido é aceito
- **Dado** um texto não vazio e um contexto
- **Quando** o widget envia
- **Então** o feedback é armazenado e retorna um `id`

### AC-2: feedback vazio é rejeitado
- **Dado** um texto vazio (ou só espaços)
- **Quando** envia
- **Então** retorna erro de validação e **não** armazena

### AC-3: feedback acima do tamanho máximo é rejeitado
- **Dado** um texto com mais de 1000 caracteres
- **Quando** envia
- **Então** retorna erro de validação

## Fora de escopo
- Moderação / anti-spam.
