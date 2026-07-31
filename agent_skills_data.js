const agentSkillsData = {
    "Agent Skills": [
        {
            "id": "agent_skill_api-and-interface-design",
            "title": "Api And Interface Design",
            "path": "agent-skills/skills/api-and-interface-design/SKILL.md",
            "description": "Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend."
        },
        {
            "id": "agent_skill_browser-testing-with-devtools",
            "title": "Browser Testing With Devtools",
            "path": "agent-skills/skills/browser-testing-with-devtools/SKILL.md",
            "description": "Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need to inspect the DOM, capture console errors, analyze network requests, profile performance, or verify visual output with real runtime data. Requires the chrome-devtools MCP server to be configured."
        },
        {
            "id": "agent_skill_ci-cd-and-automation",
            "title": "Ci Cd And Automation",
            "path": "agent-skills/skills/ci-cd-and-automation/SKILL.md",
            "description": "Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gates, configure test runners in CI, or establish deployment strategies."
        },
        {
            "id": "agent_skill_code-review-and-quality",
            "title": "Code Review And Quality",
            "path": "agent-skills/skills/code-review-and-quality/SKILL.md",
            "description": "Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch."
        },
        {
            "id": "agent_skill_code-simplification",
            "title": "Code Simplification",
            "path": "agent-skills/skills/code-simplification/SKILL.md",
            "description": "Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be. Use when reviewing code that has accumulated unnecessary complexity."
        },
        {
            "id": "agent_skill_context-engineering",
            "title": "Context Engineering",
            "path": "agent-skills/skills/context-engineering/SKILL.md",
            "description": "Optimizes agent context setup. Use when starting a new session, when agent output quality degrades, when switching between tasks, or when you need to configure rules files and context for a project."
        },
        {
            "id": "agent_skill_debugging-and-error-recovery",
            "title": "Debugging And Error Recovery",
            "path": "agent-skills/skills/debugging-and-error-recovery/SKILL.md",
            "description": "Guides systematic root-cause debugging. Use when tests fail, builds break, behavior doesn't match expectations, or you encounter any unexpected error. Use when you need a systematic approach to finding and fixing the root cause rather than guessing."
        },
        {
            "id": "agent_skill_deprecation-and-migration",
            "title": "Deprecation And Migration",
            "path": "agent-skills/skills/deprecation-and-migration/SKILL.md",
            "description": "Manages deprecation and migration. Use when removing old systems, APIs, or features. Use when migrating users from one implementation to another. Use when deciding whether to maintain or sunset existing code."
        },
        {
            "id": "agent_skill_documentation-and-adrs",
            "title": "Documentation And Adrs",
            "path": "agent-skills/skills/documentation-and-adrs/SKILL.md",
            "description": "Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need to understand the codebase."
        },
        {
            "id": "agent_skill_doubt-driven-development",
            "title": "Doubt Driven Development",
            "path": "agent-skills/skills/doubt-driven-development/SKILL.md",
            "description": "Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when correctness matters more than speed, when working in unfamiliar code, when stakes are high (production, security-sensitive logic, irreversible operations), or any time a confident output would be cheaper to verify now than to debug later."
        },
        {
            "id": "agent_skill_frontend-ui-engineering",
            "title": "Frontend Ui Engineering",
            "path": "agent-skills/skills/frontend-ui-engineering/SKILL.md",
            "description": "Builds production-quality, accessible, responsive user-facing UIs. Use when building or modifying interfaces and pages, creating components, implementing layouts, meeting WCAG accessibility requirements, managing state, or when the output needs to look and feel production-quality rather than AI-generated."
        },
        {
            "id": "agent_skill_git-workflow-and-versioning",
            "title": "Git Workflow And Versioning",
            "path": "agent-skills/skills/git-workflow-and-versioning/SKILL.md",
            "description": "Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, or when you need to organize work across multiple parallel streams. Use when cutting a release, choosing a semantic version bump, tagging, or writing a changelog."
        },
        {
            "id": "agent_skill_idea-refine",
            "title": "Idea Refine",
            "path": "agent-skills/skills/idea-refine/SKILL.md",
            "description": "Refines raw ideas into sharp, actionable concepts through structured divergent and convergent thinking. Use when an idea is still vague, when you need to stress-test assumptions before committing to a plan, or when you want to expand options before converging on one. Triggers on \"ideate\", \"refine this idea\", or \"stress-test my plan\"."
        },
        {
            "id": "agent_skill_incremental-implementation",
            "title": "Incremental Implementation",
            "path": "agent-skills/skills/incremental-implementation/SKILL.md",
            "description": "Delivers changes incrementally. Use when implementing any feature or change that touches more than one file. Use when you're about to write a large amount of code at once, or when a task feels too big to land in one step."
        },
        {
            "id": "agent_skill_interview-me",
            "title": "Interview Me",
            "path": "agent-skills/skills/interview-me/SKILL.md",
            "description": "Extracts what the user actually wants instead of what they think they should want. Achieves this through one-question-at-a-time interview until ~95% confidence about the underlying intent. Use when an ask is underspecified (\"build me X\" without \"for whom\" or \"why now\"), when the user explicitly invokes (\"interview me\", \"grill me\", \"are we sure?\", \"stress-test my thinking\"), or when you catch yourself silently filling in ambiguous requirements before any plan, spec, or code exists."
        },
        {
            "id": "agent_skill_observability-and-instrumentation",
            "title": "Observability And Instrumentation",
            "path": "agent-skills/skills/observability-and-instrumentation/SKILL.md",
            "description": "Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting. Use when shipping any feature that runs in production and you need evidence it works. Use when production issues are reported but you can't tell what happened from the available data."
        },
        {
            "id": "agent_skill_performance-optimization",
            "title": "Performance Optimization",
            "path": "agent-skills/skills/performance-optimization/SKILL.md",
            "description": "Optimizes application performance across frontend, backend, queries, and databases. Use when performance requirements exist, when you suspect performance regressions, when Core Web Vitals or load times need improvement, when N+1 query patterns need fixing, or when profiling reveals bottlenecks."
        },
        {
            "id": "agent_skill_planning-and-task-breakdown",
            "title": "Planning And Task Breakdown",
            "path": "agent-skills/skills/planning-and-task-breakdown/SKILL.md",
            "description": "Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible."
        },
        {
            "id": "agent_skill_security-and-hardening",
            "title": "Security And Hardening",
            "path": "agent-skills/skills/security-and-hardening/SKILL.md",
            "description": "Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services."
        },
        {
            "id": "agent_skill_shipping-and-launch",
            "title": "Shipping And Launch",
            "path": "agent-skills/skills/shipping-and-launch/SKILL.md",
            "description": "Prepares production launches. Use when preparing to deploy to production. Use when you need a pre-launch checklist, when setting up monitoring, when planning a staged rollout, or when you need a rollback strategy."
        },
        {
            "id": "agent_skill_source-driven-development",
            "title": "Source Driven Development",
            "path": "agent-skills/skills/source-driven-development/SKILL.md",
            "description": "Grounds every implementation decision in official documentation. Use when you want authoritative, source-cited code free from outdated patterns. Use when building with any framework or library where correctness matters."
        },
        {
            "id": "agent_skill_spec-driven-development",
            "title": "Spec Driven Development",
            "path": "agent-skills/skills/spec-driven-development/SKILL.md",
            "description": "Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea."
        },
        {
            "id": "agent_skill_test-driven-development",
            "title": "Test Driven Development",
            "path": "agent-skills/skills/test-driven-development/SKILL.md",
            "description": "Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behavior. Use when you need to prove that code works, when a bug report arrives, or when you're about to modify existing functionality."
        },
        {
            "id": "agent_skill_using-agent-skills",
            "title": "Using Agent Skills",
            "path": "agent-skills/skills/using-agent-skills/SKILL.md",
            "description": "Discovers and invokes agent skills. Use when starting a session or when you need to discover which skill applies to the current task. This is the meta-skill that governs how all other skills are discovered and invoked."
        }
    ]
};

if(typeof module !== 'undefined') module.exports = agentSkillsData;