---
name: agile-dynamic-builder
description: >-
  Use this skill when the user asks to create, format, or generate the visual HTML structure (board_html) for an agile dynamic or facilitation technique in the Agile Coach app.
---

# Agile Dynamic Builder

Este agente (skill) é especializado em estruturar o `board_html` de dinâmicas ágeis de forma ultra-didática e passo a passo, no repositório Agile Coach.

## Como Funciona
Sempre que o usuário pedir para formatar ou gerar o HTML visual de uma técnica de facilitação:
1. **Consulte a Web / Conhecimento Interno**: Entenda profundamente como a dinâmica solicitada funciona.
2. **Crie 3 Dicas de Ouro**: Regras práticas para o facilitador (como evitar desvios de tempo ou escopo).
3. **Crie 3 Perguntas Desbloqueadoras**: Perguntas que o facilitador deve fazer ao grupo caso eles não saibam o que preencher.
4. **Divida em Passos**: Mapeie os passos exatos de execução da técnica, gerando post-its de exemplo super concretos e realistas.
5. **Gere o HTML**: Use o modelo base abaixo para produzir o código final.
6. **Injete no Código**: Atualize o arquivo JavaScript de destino (ex: `facilitador_dinamicas_data.js`) com o resultado e lembre de gerar uma versão do timestamp do arquivo no `index.html` (Cache Busting) para o usuário visualizar na hora.

## Modelo Base HTML (Use-o estritamente)
Substitua todos os campos entre colchetes `[...]` pelo conteúdo exclusivo da técnica. Altere as cores de bordas e fundos conforme a necessidade visual (Tailwind Palette).

```html
<div style="font-family: system-ui, sans-serif; background: #f8fafc; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0;">
    <h3 style="text-align: center; color: #1e293b; margin-top: 0;">Dinâmica Passo a Passo: [NOME DA TÉCNICA]</h3>
    
    <!-- Guia de Facilitação -->
    <div style="background: #f1f5f9; padding: 15px; border-radius: 8px; margin-bottom: 20px; border-left: 4px solid #64748b;">
        <h4 style="margin: 0 0 10px 0; color: #334155; font-size: 16px;">🎤 Guia de Facilitação</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <div>
                <strong style="color: #475569;">💡 3 Dicas de Ouro:</strong>
                <ul style="margin: 5px 0 0 0; padding-left: 20px; color: #475569; font-size: 14px;">
                    <li>[Dica prática 1]</li>
                    <li>[Dica prática 2]</li>
                    <li>[Dica prática 3]</li>
                </ul>
            </div>
            <div>
                <strong style="color: #475569;">❓ 3 Perguntas para destravar o grupo:</strong>
                <ul style="margin: 5px 0 0 0; padding-left: 20px; color: #475569; font-size: 14px;">
                    <li>"[Pergunta direcionada 1]"</li>
                    <li>"[Pergunta direcionada 2]"</li>
                    <li>"[Pergunta direcionada 3]"</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- Como Executar (O Método) -->
    <div style="text-align: center; margin-bottom: 15px; margin-top: 20px;">
        <h4 style="margin: 0; color: #1e293b; font-size: 18px;">🛠️ Como Executar (O Método Passo a Passo) 🛠️</h4>
        <p style="color: #64748b; font-size: 14px; margin-top: 5px;">Siga estas etapas com o grupo para chegar ao resultado final</p>
    </div>

    <!-- Passo 1 -->
    <div style="background: #ffffff; padding: 15px; border-radius: 8px; border-left: 4px solid #0ea5e9; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <h4 style="margin: 0 0 10px 0; color: #0ea5e9; font-size: 16px;">Passo 1: [NOME DO PASSO]</h4>
        <p style="margin: 0 0 10px 0; color: #475569; font-style: italic;"><strong>O que fazer:</strong> [Instrução clara para o facilitador de como executar esta etapa]</p>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <div style="background: #fef08a; padding: 10px; border-radius: 2px; font-family: 'Comic Sans MS', cursive; font-size: 13px; transform: rotate(-1deg); box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">[Exemplo de post-it gerado neste passo]</div>
            <div style="background: #fef08a; padding: 10px; border-radius: 2px; font-family: 'Comic Sans MS', cursive; font-size: 13px; transform: rotate(1deg); box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">[Exemplo de post-it gerado neste passo 2]</div>
        </div>
    </div>

    <!-- Passo 2 -->
    <div style="background: #ffffff; padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <h4 style="margin: 0 0 10px 0; color: #f59e0b; font-size: 16px;">Passo 2: [NOME DO PASSO]</h4>
        <p style="margin: 0 0 10px 0; color: #475569; font-style: italic;"><strong>O que fazer:</strong> [Instrução clara para o facilitador]</p>
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <div style="background: #fef08a; padding: 10px; border-radius: 2px; font-family: 'Comic Sans MS', cursive; font-size: 13px; transform: rotate(-2deg); box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">[Exemplo]</div>
        </div>
    </div>
    
    <!-- Adicione quantos passos forem necessários -->

    <div style="text-align: center; margin-bottom: 15px; margin-top: 20px;">
        <h4 style="margin: 0; color: #1e293b; font-size: 18px;">✨ Quadro Final da Dinâmica ✨</h4>
        <p style="color: #64748b; font-size: 14px; margin-top: 5px;">Como o board ficaria ao final da sessão</p>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <!-- Quadrante Exemplo 1 -->
        <div style="background: #e0f2fe; padding: 15px; border-radius: 8px; border-top: 4px solid #0ea5e9;">
            <h4 style="margin: 0 0 10px 0; color: #0369a1; text-align: center;">[NOME DO QUADRANTE/ÁREA]</h4>
            <div style="background: #fef08a; padding: 12px; margin: 8px 0; border-radius: 2px; box-shadow: 2px 2px 5px rgba(0,0,0,0.15); transform: rotate(-1deg); font-family: 'Comic Sans MS', cursive; font-size: 13px; color: #333;">[Post-it consolidado]</div>
        </div>
        <!-- Adicione quantos quadrantes forem necessários para o resultado final -->
    </div>

    <!-- O que fazer depois -->
    <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin-top: 20px; border: 2px dashed #94a3b8; text-align: center;">
        <h4 style="margin: 0 0 10px 0; color: #334155; font-size: 16px;">🚀 Próximos Passos (O que fazer com esse resultado?)</h4>
        <p style="margin: 0; color: #475569; font-size: 14px; font-style: italic;">[Explique aqui para onde esse artefato vai. Ex: Isso vai virar Épicos no Jira? Vai pra um deck de investidores? Vai ser usado na Sprint Planning?]</p>
    </div>
</div>
```
