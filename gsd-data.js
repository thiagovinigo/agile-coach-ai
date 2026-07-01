const gsdData = {
    "GSD Agents": [
        {
            "id": "gsd-advisor-researcher",
            "title": "Advisor Researcher",
            "description": "Researches a single gray area decision and returns a structured comparison table with rationale. Spawned by discuss-phase advisor mode.",
            "path": "contexto/get-shit-done/agents/gsd-advisor-researcher.md"
        },
        {
            "id": "gsd-ai-researcher",
            "title": "Ai Researcher",
            "description": "Researches a chosen AI framework's official docs to produce implementation-ready guidance \u2014 best practices, syntax, core patterns, and pitfalls distilled for the specific use case. Writes the Framework Quick Reference and Implementation Guidance sections of AI-SPEC.md. Spawned by /gsd:ai-integration-phase orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-ai-researcher.md"
        },
        {
            "id": "gsd-assumptions-analyzer",
            "title": "Assumptions Analyzer",
            "description": "Deeply analyzes codebase for a phase and returns structured assumptions with evidence. Spawned by discuss-phase assumptions mode.",
            "path": "contexto/get-shit-done/agents/gsd-assumptions-analyzer.md"
        },
        {
            "id": "gsd-code-fixer",
            "title": "Code Fixer",
            "description": "Applies fixes to code review findings from REVIEW.md. Reads source files, applies intelligent fixes, and commits each fix atomically. Spawned by /gsd:code-review --fix.",
            "path": "contexto/get-shit-done/agents/gsd-code-fixer.md"
        },
        {
            "id": "gsd-code-reviewer",
            "title": "Code Reviewer",
            "description": "Reviews source files for bugs, security issues, and code quality problems. Produces structured REVIEW.md with severity-classified findings. Spawned by /gsd:code-review.",
            "path": "contexto/get-shit-done/agents/gsd-code-reviewer.md"
        },
        {
            "id": "gsd-codebase-mapper",
            "title": "Codebase Mapper",
            "description": "Explores codebase and writes structured analysis documents. Spawned by map-codebase with a focus area (tech, arch, quality, concerns). Writes documents directly to reduce orchestrator context load.",
            "path": "contexto/get-shit-done/agents/gsd-codebase-mapper.md"
        },
        {
            "id": "gsd-debug-session-manager",
            "title": "Debug Session Manager",
            "description": "Manages multi-cycle /gsd:debug checkpoint and continuation loop in isolated context. Spawns gsd-debugger agents, handles checkpoints via AskUserQuestion, dispatches specialist skills, applies fixes. Returns compact summary to main context. Spawned by /gsd:debug command.",
            "path": "contexto/get-shit-done/agents/gsd-debug-session-manager.md"
        },
        {
            "id": "gsd-debugger",
            "title": "Debugger",
            "description": "Investigates bugs using scientific method, manages debug sessions, handles checkpoints. Spawned by /gsd:debug orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-debugger.md"
        },
        {
            "id": "gsd-doc-classifier",
            "title": "Doc Classifier",
            "description": "Classifies a single planning document as ADR, PRD, SPEC, DOC, or UNKNOWN. Extracts title, scope summary, and cross-references. Spawned in parallel by /gsd:ingest-docs. Writes a JSON classification file and returns a one-line confirmation.",
            "path": "contexto/get-shit-done/agents/gsd-doc-classifier.md"
        },
        {
            "id": "gsd-doc-synthesizer",
            "title": "Doc Synthesizer",
            "description": "Synthesizes classified planning docs into a single consolidated context. Applies precedence rules, detects cross-ref cycles, enforces LOCKED-vs-LOCKED hard-blocks, and writes INGEST-CONFLICTS.md with three buckets (auto-resolved, competing-variants, unresolved-blockers). Spawned by /gsd:ingest-docs.",
            "path": "contexto/get-shit-done/agents/gsd-doc-synthesizer.md"
        },
        {
            "id": "gsd-doc-verifier",
            "title": "Doc Verifier",
            "description": "Verifies factual claims in generated docs against the live codebase. Returns structured JSON per doc.",
            "path": "contexto/get-shit-done/agents/gsd-doc-verifier.md"
        },
        {
            "id": "gsd-doc-writer",
            "title": "Doc Writer",
            "description": "Writes and updates project documentation. Spawned with a doc_assignment block specifying doc type, mode (create/update/supplement), and project context.",
            "path": "contexto/get-shit-done/agents/gsd-doc-writer.md"
        },
        {
            "id": "gsd-domain-researcher",
            "title": "Domain Researcher",
            "description": "Researches the business domain and real-world application context of the AI system being built. Surfaces domain expert evaluation criteria, industry-specific failure modes, regulatory context, and what \"good\" looks like for practitioners in this field \u2014 before the eval-planner turns it into measurable rubrics. Spawned by /gsd:ai-integration-phase orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-domain-researcher.md"
        },
        {
            "id": "gsd-eval-auditor",
            "title": "Eval Auditor",
            "description": "Retroactive audit of an implemented AI phase's evaluation coverage. Checks implementation against the AI-SPEC.md evaluation plan. Scores each eval dimension as COVERED/PARTIAL/MISSING. Produces a scored EVAL-REVIEW.md with findings, gaps, and remediation guidance. Spawned by /gsd:eval-review orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-eval-auditor.md"
        },
        {
            "id": "gsd-eval-planner",
            "title": "Eval Planner",
            "description": "Designs a structured evaluation strategy for an AI phase. Identifies critical failure modes, selects eval dimensions with rubrics, recommends tooling, and specifies the reference dataset. Writes the Evaluation Strategy, Guardrails, and Production Monitoring sections of AI-SPEC.md. Spawned by /gsd:ai-integration-phase orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-eval-planner.md"
        },
        {
            "id": "gsd-executor",
            "title": "Executor",
            "description": "Executes GSD plans with atomic commits, deviation handling, checkpoint protocols, and state management. Spawned by execute-phase orchestrator or execute-plan command.",
            "path": "contexto/get-shit-done/agents/gsd-executor.md"
        },
        {
            "id": "gsd-framework-selector",
            "title": "Framework Selector",
            "description": "Presents an interactive decision matrix to surface the right AI/LLM framework for the user's specific use case. Produces a scored recommendation with rationale. Spawned by /gsd:ai-integration-phase and /gsd-select-framework orchestrators.",
            "path": "contexto/get-shit-done/agents/gsd-framework-selector.md"
        },
        {
            "id": "gsd-integration-checker",
            "title": "Integration Checker",
            "description": "Verifies cross-phase integration and E2E flows. Checks that phases connect properly and user workflows complete end-to-end.",
            "path": "contexto/get-shit-done/agents/gsd-integration-checker.md"
        },
        {
            "id": "gsd-intel-updater",
            "title": "Intel Updater",
            "description": "Analyzes codebase and writes structured intel files to .planning/intel/.",
            "path": "contexto/get-shit-done/agents/gsd-intel-updater.md"
        },
        {
            "id": "gsd-nyquist-auditor",
            "title": "Nyquist Auditor",
            "description": "Fills Nyquist validation gaps by generating tests and verifying coverage for phase requirements",
            "path": "contexto/get-shit-done/agents/gsd-nyquist-auditor.md"
        },
        {
            "id": "gsd-pattern-mapper",
            "title": "Pattern Mapper",
            "description": "Analyzes codebase for existing patterns and produces PATTERNS.md mapping new files to closest analogs. Read-only codebase analysis spawned by /gsd:plan-phase orchestrator before planning.",
            "path": "contexto/get-shit-done/agents/gsd-pattern-mapper.md"
        },
        {
            "id": "gsd-phase-researcher",
            "title": "Phase Researcher",
            "description": "Researches how to implement a phase before planning. Produces RESEARCH.md consumed by gsd-planner. Spawned by /gsd:plan-phase orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-phase-researcher.md"
        },
        {
            "id": "gsd-plan-checker",
            "title": "Plan Checker",
            "description": "Verifies plans will achieve phase goal before execution. Goal-backward analysis of plan quality. Spawned by /gsd:plan-phase orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-plan-checker.md"
        },
        {
            "id": "gsd-planner",
            "title": "Planner",
            "description": "Creates executable phase plans with task breakdown, dependency analysis, and goal-backward verification. Spawned by /gsd:plan-phase orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-planner.md"
        },
        {
            "id": "gsd-project-researcher",
            "title": "Project Researcher",
            "description": "Researches domain ecosystem before roadmap creation. Produces files in .planning/research/ consumed during roadmap creation. Spawned by /gsd:new-project or /gsd:new-milestone orchestrators.",
            "path": "contexto/get-shit-done/agents/gsd-project-researcher.md"
        },
        {
            "id": "gsd-research-synthesizer",
            "title": "Research Synthesizer",
            "description": "Synthesizes research outputs from parallel researcher agents into SUMMARY.md. Spawned by /gsd:new-project after 4 researcher agents complete.",
            "path": "contexto/get-shit-done/agents/gsd-research-synthesizer.md"
        },
        {
            "id": "gsd-roadmapper",
            "title": "Roadmapper",
            "description": "Creates project roadmaps with phase breakdown, requirement mapping, success criteria derivation, and coverage validation. Spawned by /gsd:new-project orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-roadmapper.md"
        },
        {
            "id": "gsd-security-auditor",
            "title": "Security Auditor",
            "description": "Verifies threat mitigations from PLAN.md threat model exist in implemented code. Produces SECURITY.md. Spawned by /gsd:secure-phase.",
            "path": "contexto/get-shit-done/agents/gsd-security-auditor.md"
        },
        {
            "id": "gsd-ui-auditor",
            "title": "Ui Auditor",
            "description": "Retroactive 6-pillar visual audit of implemented frontend code. Produces scored UI-REVIEW.md. Spawned by /gsd:ui-review orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-ui-auditor.md"
        },
        {
            "id": "gsd-ui-checker",
            "title": "Ui Checker",
            "description": "Validates UI-SPEC.md design contracts against 6 quality dimensions. Produces BLOCK/FLAG/PASS verdicts. Spawned by /gsd:ui-phase orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-ui-checker.md"
        },
        {
            "id": "gsd-ui-researcher",
            "title": "Ui Researcher",
            "description": "Produces UI-SPEC.md design contract for frontend phases. Reads upstream artifacts, detects design system state, asks only unanswered questions. Spawned by /gsd:ui-phase orchestrator.",
            "path": "contexto/get-shit-done/agents/gsd-ui-researcher.md"
        },
        {
            "id": "gsd-user-profiler",
            "title": "User Profiler",
            "description": "Analyzes extracted session messages across 8 behavioral dimensions to produce a scored developer profile with confidence levels and evidence. Spawned by profile orchestration workflows.",
            "path": "contexto/get-shit-done/agents/gsd-user-profiler.md"
        },
        {
            "id": "gsd-verifier",
            "title": "Verifier",
            "description": "Verifies phase goal achievement through goal-backward analysis. Checks codebase delivers what phase promised, not just that tasks completed. Creates VERIFICATION.md report.",
            "path": "contexto/get-shit-done/agents/gsd-verifier.md"
        }
    ]
};
if(typeof module !== 'undefined') module.exports = gsdData;
