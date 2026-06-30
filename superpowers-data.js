const superpowersData = {
    "Superpowers": [
        {
            "id": "brainstorming",
            "title": "Brainstorming",
            "description": "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.",
            "path": "contexto/superpowers/skills/brainstorming/SKILL.md"
        },
        {
            "id": "dispatching-parallel-agents",
            "title": "Dispatching Parallel Agents",
            "description": "Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies",
            "path": "contexto/superpowers/skills/dispatching-parallel-agents/SKILL.md"
        },
        {
            "id": "executing-plans",
            "title": "Executing Plans",
            "description": "Use when you have a written implementation plan to execute in a separate session with review checkpoints",
            "path": "contexto/superpowers/skills/executing-plans/SKILL.md"
        },
        {
            "id": "finishing-a-development-branch",
            "title": "Finishing A Development Branch",
            "description": "Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup",
            "path": "contexto/superpowers/skills/finishing-a-development-branch/SKILL.md"
        },
        {
            "id": "receiving-code-review",
            "title": "Receiving Code Review",
            "description": "Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation",
            "path": "contexto/superpowers/skills/receiving-code-review/SKILL.md"
        },
        {
            "id": "requesting-code-review",
            "title": "Requesting Code Review",
            "description": "Use when completing tasks, implementing major features, or before merging to verify work meets requirements",
            "path": "contexto/superpowers/skills/requesting-code-review/SKILL.md"
        },
        {
            "id": "subagent-driven-development",
            "title": "Subagent Driven Development",
            "description": "Use when executing implementation plans with independent tasks in the current session",
            "path": "contexto/superpowers/skills/subagent-driven-development/SKILL.md"
        },
        {
            "id": "systematic-debugging",
            "title": "Systematic Debugging",
            "description": "Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes",
            "path": "contexto/superpowers/skills/systematic-debugging/SKILL.md"
        },
        {
            "id": "test-driven-development",
            "title": "Test Driven Development",
            "description": "Use when implementing any feature or bugfix, before writing implementation code",
            "path": "contexto/superpowers/skills/test-driven-development/SKILL.md"
        },
        {
            "id": "using-git-worktrees",
            "title": "Using Git Worktrees",
            "description": "Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback",
            "path": "contexto/superpowers/skills/using-git-worktrees/SKILL.md"
        },
        {
            "id": "using-superpowers",
            "title": "Using Superpowers",
            "description": "Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions",
            "path": "contexto/superpowers/skills/using-superpowers/SKILL.md"
        },
        {
            "id": "verification-before-completion",
            "title": "Verification Before Completion",
            "description": "Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always",
            "path": "contexto/superpowers/skills/verification-before-completion/SKILL.md"
        },
        {
            "id": "writing-plans",
            "title": "Writing Plans",
            "description": "Use when you have a spec or requirements for a multi-step task, before touching code",
            "path": "contexto/superpowers/skills/writing-plans/SKILL.md"
        },
        {
            "id": "writing-skills",
            "title": "Writing Skills",
            "description": "Use when creating new skills, editing existing skills, or verifying skills work before deployment",
            "path": "contexto/superpowers/skills/writing-skills/SKILL.md"
        }
    ]
};
if(typeof module !== 'undefined') module.exports = superpowersData;
