import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

new_mapping = """            } else if(viewId === 'kb-agil') {
                sectionsToExtract = [
                    { title: 'Transformação Ágil', parts: [ { id: 's-agil', context: 'Transf. Ágil' } ] },
                    { title: 'Transformação Digital', parts: [ { id: 's-digital', context: 'Transf. Digital' } ] },
                    { title: 'Diferenças Lado a Lado', parts: [ { id: 's-diff', context: 'Diferenças' } ] },
                    { title: 'Fases da Transformação Ágil', parts: [ { id: 's-passo-agil', context: 'Jornada' } ] },
                    { title: 'Fases da Transformação Digital', parts: [ { id: 's-passo-digital', context: 'Jornada' } ] },
                    { title: 'O Case Nubank', parts: [ { id: 's-nubank', context: 'Estudo de Caso' } ] }
                ];
            } else if(viewId === 'kb-kanban') {
                sectionsToExtract = [
                    { title: 'O que é Kanban', parts: [ { id: 's-kanban', context: 'Guia Profundo' } ] },
                    { title: 'Os 9 Valores', parts: [ { id: 's-kanban-valores', context: 'Guia Profundo' } ] },
                    { title: 'Os 6 Princípios', parts: [ { id: 's-kanban-principios', context: 'Guia Profundo' } ] },
                    { title: 'As 6 Práticas', parts: [ { id: 's-kanban-praticas', context: 'Guia Profundo' } ] },
                    { title: 'As 3 Agendas', parts: [ { id: 's-kanban-agendas', context: 'Guia Profundo' } ] },
                    { title: 'Upstream & Downstream', parts: [ { id: 's-kanban-upstream', context: 'Guia Profundo' } ] },
                    { title: 'O Framework STATIK', parts: [ { id: 's-kanban-statik', context: 'Guia Profundo' } ] },
                    { title: 'Classes de Serviço', parts: [ { id: 's-kanban-classes', context: 'Guia Profundo' } ] },
                    { title: 'Previsão & Monte Carlo', parts: [ { id: 's-kanban-previsao', context: 'Guia Profundo' } ] },
                    { title: 'Kanban em Escala', parts: [ { id: 's-kanban-escala', context: 'Guia Profundo' } ] },
                    { title: 'Casos Reais', parts: [ { id: 's-kanban-casos', context: 'Guia Profundo' } ] }
                ];
            } else if(viewId === 'kb-scrum') {
                sectionsToExtract = [
                    { title: 'Scrum Refinado', parts: [ { id: 's-scrum', context: 'Scrum' } ] }
                ];
            } else if(viewId === 'kb-po') {
                sectionsToExtract = [
                    { title: 'O Papel do PO', parts: [ { id: 's-po', context: 'Gestão de Produto' } ] },
                    { title: 'Quebrando Histórias', parts: [ { id: 's-po-quebrando', context: 'Gestão de Produto' } ] },
                    { title: 'Refinamento Eficaz', parts: [ { id: 's-po-refinamento', context: 'Gestão de Produto' } ] },
                    { title: 'Priorização do Backlog', parts: [ { id: 's-po-priorizacao', context: 'Gestão de Produto' } ] },
                    { title: 'Formatos de Histórias', parts: [ { id: 's-po-formatos', context: 'Gestão de Produto' } ] },
                    { title: 'Roadmap Ágil', parts: [ { id: 's-po-roadmap', context: 'Gestão de Produto' } ] },
                    { title: 'Critérios de Aceite & BDD', parts: [ { id: 's-po-ac', context: 'Gestão de Produto' } ] }
                ];
            } else if(viewId === 'kb-metricas') {
                sectionsToExtract = [
                    { title: 'Métricas de Fluxo', parts: [ { id: 's-metricas-fluxo', context: 'Métricas' } ] },
                    { title: 'Gráficos Kanban', parts: [ { id: 's-metricas-graficos', context: 'Métricas' } ] },
                    { title: 'Visão Executiva (C-Level)', parts: [ { id: 's-metricas-clevel', context: 'Métricas' } ] }
                ];
            } else if(viewId === 'kb-lider') {
                sectionsToExtract = [
                    { title: 'Ensinando o Novo Fluxo', parts: [ { id: 's-lider-fluxo', context: 'Guia do Líder' } ] },
                    { title: 'Regras de Transição', parts: [ { id: 's-lider-transicao', context: 'Guia do Líder' } ] },
                    { title: 'Políticas Explícitas', parts: [ { id: 's-lider-politicas', context: 'Guia do Líder' } ] },
                    { title: 'Nivelando o Time Misto', parts: [ { id: 's-lider-misto', context: 'Guia do Líder' } ] },
                    { title: 'Plano de 90 Dias', parts: [ { id: 's-lider-90dias', context: 'Guia do Líder' } ] },
                    { title: 'Checklist Semanal', parts: [ { id: 's-lider-checklist', context: 'Guia do Líder' } ] },
                    { title: 'Gestão de Resistência', parts: [ { id: 's-lider-resistencia', context: 'Guia do Líder' } ] }
                ];
            } else if(viewId === 'kb-case') {
                sectionsToExtract = [
                    { title: 'Squad Open Banking', parts: [ { id: 's-exemplo', context: 'Estudo de Caso' } ] },
                    { title: 'Uma Semana no Squad', parts: [ { id: 's-story', context: 'Estudo de Caso' } ] },
                    { title: 'Entregas em Produção', parts: [ { id: 's-prod-extra', context: 'Estudo de Caso' } ] }
                ];
            }"""

# Insert the new views mapping just after kb-elite mapping
app_js = app_js.replace("            }\n\n            // Create layout structure for Light Mode", new_mapping + "\n            }\n\n            // Create layout structure for Light Mode")

# Insert the new extract calls
new_extracts = """        extractSection('kb-agil', 'kb-agil');
        extractSection('kb-kanban', 'kb-kanban');
        extractSection('kb-scrum', 'kb-scrum');
        extractSection('kb-po', 'kb-po');
        extractSection('kb-metricas', 'kb-metricas');
        extractSection('kb-lider', 'kb-lider');
        extractSection('kb-case', 'kb-case');"""

app_js = app_js.replace("        extractSection('ng-elite', 'kb-elite');", "        extractSection('ng-elite', 'kb-elite');\n" + new_extracts)

# Notice I need to change fetch path to the correct scrumban_guia.html
app_js = app_js.replace("'./contexto/scrumban_guia - Copia (7).html'", "'./contexto/scrumban_guia.html'")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
