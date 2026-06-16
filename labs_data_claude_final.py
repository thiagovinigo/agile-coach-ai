# labs_data_claude_final.py

claude_final = [
    {
        "id": 44, "icon": "🖥️", "title": "Marco 1: Consumo do Backlog e Regras (IDE)",
        "oque": "O desenvolvedor (ou automação) inicia o Claude Code localmente, que consome o ticket #501 preparado pelo Kiro, e carrega as convenções do projeto.",
        "porque": "Demonstrar a esteira Downstream. O Claude Code atua como o 'Operário Sênior' que pega a especificação pronta do Arquiteto (ADR) e executa sem alucinar, balizado por regras locais.",
        "steps": [
            {
                "title": "O Arquivo de Convenção",
                "text": "As amarras locais que garantem que o Claude Code usará TDD.",
                "code": "# .claudecode/CONVENTIONS.md\n- Você DEVE ler os ADRs da pasta `docs/adr/` antes de escrever código.\n- O Desenvolvimento deve ser ESTRITAMENTE guiado por testes (TDD).\n- Escreva o teste primeiro, rode (falhe), e só depois crie a classe.",
                "lang": "markdown"
            },
            {
                "title": "O Comando e o Download do Ticket",
                "text": "A execução no terminal da máquina do desenvolvedor.",
                "code": "> claude /task tfs-get-story 501\n\n[Claude Code] Lendo Convenções: TDD mandatório.\n[Claude Code] Baixando a Story #501 do Azure DevOps...\n[Claude Code] Baixando o ADR '001-motor-validacao.md'.\n[Claude Code] O Arquiteto exige TypeScript e Strategy Pattern. Vamos iniciar.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 45, "icon": "🔴", "title": "Marco 2: O Loop TDD (Fase Vermelha)",
        "oque": "O Claude Code escreve o teste unitário (Jest) para a classe `ValidationStrategy`, executa no terminal e garante que o teste quebra.",
        "porque": "Provar que a IA não está fingindo. O teste vermelho garante que o código não existe e que a automação do ambiente está capturando as falhas.",
        "steps": [
            {
                "title": "A Geração do Teste (Jest)",
                "text": "A IA escreve o arquivo `.test.ts` sem a implementação real.",
                "code": "// src/__tests__/validation.test.ts\nimport { EslintValidator } from '../validators';\n\ntest('EslintValidator deve disparar erro se achar console.log', () => {\n  const validator = new EslintValidator();\n  const result = validator.validate('console.log(\"oi\")');\n  expect(result.isValid).toBe(false);\n});",
                "lang": "typescript"
            },
            {
                "title": "O Teste Quebrando no Terminal",
                "text": "A IDE roda o comando e falha.",
                "code": "> npm run test\n\nFAIL src/__tests__/validation.test.ts\n  ● EslintValidator deve disparar erro\n    TypeError: EslintValidator is not a constructor\n\n[Claude Code] Teste falhou como esperado. Iniciando fase Verde.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 46, "icon": "🟢", "title": "Marco 3: A Autocura (Green & Refactor)",
        "oque": "O Claude Code escreve o código real, passa no teste, mas toma bronca do Linter. Ele lê a saída de erro e corrige o próprio código.",
        "porque": "É a 'Autonomia Resiliente'. Um desenvolvedor humano perderia minutos consertando chaves e tipagens esquecidas. O agente entra em um loop infinito de `code -> lint -> fix` até estar impecável.",
        "steps": [
            {
                "title": "A Implementação Real",
                "text": "O código TypeScript escrito pelo Claude.",
                "code": "// src/validators.ts\nexport class EslintValidator {\n  validate(code: any) { // erro proposital de tipagem\n    if(code.includes('console.log')) return { isValid: false };\n    return { isValid: true };\n  }\n}",
                "lang": "typescript"
            },
            {
                "title": "A Autocura do Terminal",
                "text": "A IA lê o erro do compilador e conserta.",
                "code": "> npm run test\n✅ PASS src/__tests__/validation.test.ts\n\n> npm run lint\n❌ Erro na linha 2: Unexpected 'any'. Especifique o tipo 'string'.\n\n[Claude Code] Corrigindo erro de ESLint...\n> cat src/validators.ts\nexport class EslintValidator {\n  validate(code: string) { ... }\n\n> npm run lint\n✅ Clean.",
                "lang": "bash"
            }
        ]
    },
    {
        "id": 47, "icon": "🛡️", "title": "Marco 4: Validação Segura e Handoff",
        "oque": "O bloqueio do Git Hook local e a criação do Pull Request direto via terminal.",
        "porque": "Termina a jornada E2E garantindo rastreabilidade e segurança. O código perfeito não serve de nada se quebrar o repositório central.",
        "steps": [
            {
                "title": "O Hook do Git",
                "text": "O script Bash local que barra commits sujos.",
                "code": "#!/bin/sh\n# .git/hooks/pre-commit\n\nnpm run lint && npm run test\nif [ $? -ne 0 ]; then\n  echo \"Bloqueado: Código não atende aos padrões.\"\n  exit 1\nfi",
                "lang": "bash"
            },
            {
                "title": "O Pull Request Criado",
                "text": "O encerramento majestoso com a integração de MCP.",
                "code": "> [Claude Code] Comitando código com rastreabilidade.\n> git commit -m \"#[501] feat: motor de validacao Strategy\"\n\n> [Claude Code] Acionando MCP TFS Repos...\n> Criando PR na branch 'master' linkando a Task #501.\n\n[Claude Code] 🎉 Sucesso! Pull Request #900 criado. O Tech Lead foi notificado no Teams.",
                "lang": "bash"
            }
        ]
    }
]
