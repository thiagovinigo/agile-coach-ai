const rufloData = {
    "VISÃO GERAL & GUIAS": [
        {
            "id": "ruflo-readme",
            "title": "Visão Geral do Ruflo (Meta-Harness)",
            "description": "Arquitetura completa do Ruflo: meta-harness para Claude Code e Codex, swarms, memória vetorial e MCP.",
            "icon": "🌊",
            "path": "ruflo/README.md"
        },
        {
            "id": "ruflo-explained",
            "title": "RuFlo Explained (Guia dos 14 Capítulos)",
            "description": "Artigo completo por rUv Cohen: do zero ao swarm coordenado, memória adaptativa, plugins e governança.",
            "icon": "📖",
            "path": "ruflo/docs/ruflo-explained.md"
        },
        {
            "id": "ruflo-agents-guide",
            "title": "Guia de Orquestração (AGENTS.md)",
            "description": "Regras de ouro: Codex/Claude executa, Ruflo orquestra. Padrões de swarm, memória e recipes prontas.",
            "icon": "🤖",
            "path": "ruflo/AGENTS.md"
        },
        {
            "id": "ruflo-claude-guide",
            "title": "Diretrizes e Invariantes (CLAUDE.md)",
            "description": "Regras de governança estritas, isolamento em worktrees, contratos de autorização e política anti-drift.",
            "icon": "🛡️",
            "path": "ruflo/CLAUDE.md"
        },
        {
            "id": "ruflo-metaharness-guide",
            "title": "MetaHarness User Guide",
            "description": "Flywheel de evolução contínua: avaliação empírica, auto-otimização e envelopes de segurança.",
            "icon": "⚙️",
            "path": "ruflo/docs/metaharness-user-guide.md"
        },
        {
            "id": "ruflo-userguide",
            "title": "Manual do Usuário Completo (USERGUIDE.md)",
            "description": "Referência exaustiva de configuração, comandos CLI, Terminal UI (TUI) e integração de ecossistema.",
            "icon": "📚",
            "path": "ruflo/docs/USERGUIDE.md"
        }
    ],
    "PLUGINS: CORE & SWARM": [
        {
            "id": "ruflo-autopilot",
            "title": "Autopilot (ruflo-autopilot)",
            "description": "Autonomous /loop-driven task completion with learning and prediction.",
            "icon": "🚀",
            "path": "ruflo/plugins/ruflo-autopilot/README.md"
        },
        {
            "id": "ruflo-console",
            "title": "Console (ruflo-console)",
            "description": "ruflo's cockpit inside Claude Code: the `/ruflo` command, its pages, and a band above the prompt. It reads ruflo's own files; anything it cannot measure reads `n/a`. Design notes: ...",
            "icon": "💻",
            "path": "ruflo/plugins/ruflo-console/README.md"
        },
        {
            "id": "ruflo-core",
            "title": "Core (ruflo-core)",
            "description": "Foundation plugin. Registers the `ruflo` MCP server (314 tools), provides three generalist agents (`coder`, `researcher`, `reviewer`), three first-run helpers (`init-project`, `ruf...",
            "icon": "🎛️",
            "path": "ruflo/plugins/ruflo-core/README.md"
        },
        {
            "id": "ruflo-loop-workers",
            "title": "Loop Workers (ruflo-loop-workers)",
            "description": "Cache-aware /loop workers and CronCreate background automation. Substrate plugin for every recurring task in the ruflo family.",
            "icon": "🔄",
            "path": "ruflo/plugins/ruflo-loop-workers/README.md"
        },
        {
            "id": "ruflo-mods",
            "title": "Mods (ruflo-mods)",
            "description": "ruflo as a Claude Code mod (function hooks): on by default in Claude Code >= 2.1.287; from 2.1.277 with `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`. Design and evidence: [ADR-404](../../...",
            "icon": "🛡️",
            "path": "ruflo/plugins/ruflo-mods/README.md"
        },
        {
            "id": "ruflo-swarm",
            "title": "Swarm (ruflo-swarm)",
            "description": "Agent teams, swarm coordination, Monitor streams, and worktree isolation.",
            "icon": "🐝",
            "path": "ruflo/plugins/ruflo-swarm/README.md"
        },
        {
            "id": "ruflo-workflows",
            "title": "Workflows (ruflo-workflows)",
            "description": "Workflow automation across **two complementary surfaces**:",
            "icon": "🔀",
            "path": "ruflo/plugins/ruflo-workflows/README.md"
        }
    ],
    "PLUGINS: MEMÓRIA & VETORIAL": [
        {
            "id": "ruflo-agentdb",
            "title": "Agentdb (ruflo-agentdb)",
            "description": "The substrate plugin for Ruflo memory. Wraps three CLI MCP families — `agentdb_*` (controller bridge, 20 tools), `embeddings_*` (RuVector ONNX engine, 10 tools), and `ruvllm_hnsw_*...",
            "icon": "💾",
            "path": "ruflo/plugins/ruflo-agentdb/README.md"
        },
        {
            "id": "ruflo-daa",
            "title": "Daa (ruflo-daa)",
            "description": "Dynamic Agentic Architecture with cognitive patterns, knowledge sharing, and adaptive agents.",
            "icon": "🧩",
            "path": "ruflo/plugins/ruflo-daa/README.md"
        },
        {
            "id": "ruflo-graph-intelligence",
            "title": "Graph Intelligence (ruflo-graph-intelligence)",
            "description": "Graph Intelligence Engine for RuFlo: single-entry personalized PageRank, streaming delta updates and witness-signed reasoning artifacts (ADR-123), built on sublinear-time-solver. L...",
            "icon": "🔬",
            "path": "ruflo/plugins/ruflo-graph-intelligence/README.md"
        },
        {
            "id": "ruflo-intelligence",
            "title": "Intelligence (ruflo-intelligence)",
            "description": "User-facing surface for Ruflo's self-learning system. Wraps **29 intelligence-related MCP tools** across four families into discoverable skills, commands, and the canonical 4-step ...",
            "icon": "💡",
            "path": "ruflo/plugins/ruflo-intelligence/README.md"
        },
        {
            "id": "ruflo-knowledge-graph",
            "title": "Knowledge Graph (ruflo-knowledge-graph)",
            "description": "Knowledge graph construction -- entity extraction, relation mapping, and pathfinder graph traversal.",
            "icon": "🕸️",
            "path": "ruflo/plugins/ruflo-knowledge-graph/README.md"
        },
        {
            "id": "ruflo-rag-memory",
            "title": "Rag Memory (ruflo-rag-memory)",
            "description": "Retrieval-Augmented Generation memory with HNSW vector search, AgentDB persistence, and Claude Code memory bridge.",
            "icon": "📚",
            "path": "ruflo/plugins/ruflo-rag-memory/README.md"
        },
        {
            "id": "ruflo-ruvector",
            "title": "Ruvector (ruflo-ruvector)",
            "description": "Self-learning vector database powered by [`ruvector@0.3.3`](https://www.npmjs.com/package/ruvector) — HNSW, Adaptive LoRA embeddings, hooks-based intelligence, SONA self-optimizing...",
            "icon": "🧠",
            "path": "ruflo/plugins/ruflo-ruvector/README.md"
        },
        {
            "id": "ruflo-rvf",
            "title": "Rvf (ruflo-rvf)",
            "description": "RVF format for portable agent memory, session persistence, and cross-platform transfer.",
            "icon": "📦",
            "path": "ruflo/plugins/ruflo-rvf/README.md"
        }
    ],
    "PLUGINS: ARQUITETURA & MÉTODOS": [
        {
            "id": "ruflo-adr",
            "title": "Adr (ruflo-adr)",
            "description": "ADR lifecycle management -- create, index, reconcile, supersede, and link Architecture Decision Records to code.",
            "icon": "📝",
            "path": "ruflo/plugins/ruflo-adr/README.md"
        },
        {
            "id": "ruflo-ddd",
            "title": "Ddd (ruflo-ddd)",
            "description": "Domain-Driven Design scaffolding -- bounded contexts, aggregate roots, domain events, and anti-corruption layers.",
            "icon": "🏛️",
            "path": "ruflo/plugins/ruflo-ddd/README.md"
        },
        {
            "id": "ruflo-goals",
            "title": "Goals (ruflo-goals)",
            "description": "Long-horizon goal planning, deep research orchestration, and adaptive replanning.",
            "icon": "🎯",
            "path": "ruflo/plugins/ruflo-goals/README.md"
        },
        {
            "id": "ruflo-metaharness",
            "title": "Metaharness (ruflo-metaharness)",
            "description": "MetaHarness integration plugin for ruflo. Surfaces the upstream `metaharness` / `harness` / `@metaharness/darwin` CLIs through eleven ruflo skills, honoring [ADR-150](../../v3/docs...",
            "icon": "⚙️",
            "path": "ruflo/plugins/ruflo-metaharness/README.md"
        },
        {
            "id": "ruflo-sparc",
            "title": "Sparc (ruflo-sparc)",
            "description": "SPARC methodology -- Specification, Pseudocode, Architecture, Refinement, Completion phases with quality gates between each phase.",
            "icon": "⚡",
            "path": "ruflo/plugins/ruflo-sparc/README.md"
        }
    ],
    "PLUGINS: SEGURANÇA & QA": [
        {
            "id": "ruflo-aidefence",
            "title": "Aidefence (ruflo-aidefence)",
            "description": "AI safety scanning, PII detection, prompt injection defense, and adaptive threat learning.",
            "icon": "🛡️",
            "path": "ruflo/plugins/ruflo-aidefence/README.md"
        },
        {
            "id": "ruflo-browser",
            "title": "Browser (ruflo-browser)",
            "description": "Session-as-skill browser automation. Playwright-backed via 23 `mcp__plugin_ruflo-core_ruflo__browser_*` tools, with each session captured as a first-class **RVF cognitive container...",
            "icon": "🌐",
            "path": "ruflo/plugins/ruflo-browser/README.md"
        },
        {
            "id": "ruflo-protector",
            "title": "Protector (ruflo-protector)",
            "description": "**Project Anatole** is an optional, learning watchdog for unattended agents (`/loop` ticks, headless `claude -p` workers, overnight swarms). It is a mod ([ADR-404](../../v3/docs/ad...",
            "icon": "🐕",
            "path": "ruflo/plugins/ruflo-protector/README.md"
        },
        {
            "id": "ruflo-security-audit",
            "title": "Security Audit (ruflo-security-audit)",
            "description": "Security review, dependency scanning, policy gates, and CVE monitoring.",
            "icon": "🔒",
            "path": "ruflo/plugins/ruflo-security-audit/README.md"
        },
        {
            "id": "ruflo-testgen",
            "title": "Testgen (ruflo-testgen)",
            "description": "Test gap detection, coverage analysis, and automated test generation. SPARC Refinement-phase canonical owner.",
            "icon": "🧪",
            "path": "ruflo/plugins/ruflo-testgen/README.md"
        }
    ],
    "PLUGINS: FERRAMENTAS & DEV": [
        {
            "id": "ruflo-agent",
            "title": "Agent (ruflo-agent)",
            "description": "Agent runtimes for ruflo — one mental model, two backends (a third planned):",
            "icon": "📦",
            "path": "ruflo/plugins/ruflo-agent/README.md"
        },
        {
            "id": "ruflo-arena",
            "title": "Arena (ruflo-arena)",
            "description": "Competitive ruliology for Ruflo swarms — **arenas**, **tournaments**, and **adaptive co-evolution** of program strategies. Implements the first executable slice of Ruflo",
            "icon": "🏟️",
            "path": "ruflo/plugins/ruflo-arena/README.md"
        },
        {
            "id": "ruflo-cost-tracker",
            "title": "Cost Tracker (ruflo-cost-tracker)",
            "description": "Token usage tracking, model cost attribution per agent, budget alerts, and optimization recommendations.",
            "icon": "💰",
            "path": "ruflo/plugins/ruflo-cost-tracker/README.md"
        },
        {
            "id": "ruflo-docs",
            "title": "Docs (ruflo-docs)",
            "description": "Documentation generation, drift detection, and API docs automation.",
            "icon": "📑",
            "path": "ruflo/plugins/ruflo-docs/README.md"
        },
        {
            "id": "ruflo-jujutsu",
            "title": "Jujutsu (ruflo-jujutsu)",
            "description": "Advanced git workflows with diff analysis, risk scoring, and reviewer recommendations.",
            "icon": "🪓",
            "path": "ruflo/plugins/ruflo-jujutsu/README.md"
        },
        {
            "id": "ruflo-migrations",
            "title": "Migrations (ruflo-migrations)",
            "description": "Schema migration management -- generate, validate, dry-run, and rollback database migrations.",
            "icon": "🗄️",
            "path": "ruflo/plugins/ruflo-migrations/README.md"
        },
        {
            "id": "ruflo-observability",
            "title": "Observability (ruflo-observability)",
            "description": "Structured logging, distributed tracing, and metrics -- correlate agent swarm activity with application telemetry.",
            "icon": "📊",
            "path": "ruflo/plugins/ruflo-observability/README.md"
        },
        {
            "id": "ruflo-plugin-creator",
            "title": "Plugin Creator (ruflo-plugin-creator)",
            "description": "Scaffold, validate, and publish new Claude Code plugins with proper structure, MCP tool wiring, AND the canonical plugin contract (ADR + smoke + Compatibility + namespace coordinat...",
            "icon": "🛠️",
            "path": "ruflo/plugins/ruflo-plugin-creator/README.md"
        },
        {
            "id": "ruflo-ruvllm",
            "title": "Ruvllm (ruflo-ruvllm)",
            "description": "RuVLLM local inference with chat formatting, model configuration, MicroLoRA fine-tuning, and SONA real-time adaptation.",
            "icon": "🤖",
            "path": "ruflo/plugins/ruflo-ruvllm/README.md"
        }
    ],
    "PLUGINS: DOMÍNIO & ECOSSISTEMA": [
        {
            "id": "ruflo-agntcy",
            "title": "Agntcy (ruflo-agntcy)",
            "description": "AGNTCY/Outshift Internet-of-Cognition (IOC) runtime integration for Ruflo — the \"AGNTCY-identified, SLIM-transported, CASA-authorized\" leg of the clean-positioning stack described ...",
            "icon": "🤝",
            "path": "ruflo/plugins/ruflo-agntcy/README.md"
        },
        {
            "id": "ruflo-ai-team",
            "title": "Ai Team (ruflo-ai-team)",
            "description": "Give Claude a tenant-isolated AI team that divides work, coordinates progress, recalls approved context, and returns evidence-backed results.",
            "icon": "👥",
            "path": "ruflo/plugins/ruflo-ai-team/README.md"
        },
        {
            "id": "ruflo-bbs-federation",
            "title": "Bbs Federation (ruflo-bbs-federation)",
            "description": "Function hooks (ADR-445 pattern, `hooks/register.ts`) that need no model call, no network and no process:",
            "icon": "📻",
            "path": "ruflo/plugins/ruflo-bbs-federation/README.md"
        },
        {
            "id": "ruflo-business-pods",
            "title": "Business Pods (ruflo-business-pods)",
            "description": "Function hooks (ADR-445 pattern, `hooks/register.ts`) that need no model call, no network and no process:",
            "icon": "🏢",
            "path": "ruflo/plugins/ruflo-business-pods/README.md"
        },
        {
            "id": "ruflo-chatgpt-federation",
            "title": "Chatgpt Federation (ruflo-chatgpt-federation)",
            "description": "The ChatGPT Federation connector's publisher. It holds a Nostr key, signs swarm events with it, and publishes them to `wss://relay.ruv.io` over a connection it",
            "icon": "💬",
            "path": "ruflo/plugins/ruflo-chatgpt-federation/README.md"
        },
        {
            "id": "ruflo-deepseek-harness",
            "title": "Deepseek Harness (ruflo-deepseek-harness)",
            "description": "DeepSeek chat and reasoning completions as ruflo skills (see `commands/ruflo-deepseek-harness.md`).",
            "icon": "🐋",
            "path": "ruflo/plugins/ruflo-deepseek-harness/README.md"
        },
        {
            "id": "ruflo-federation",
            "title": "Federation (ruflo-federation)",
            "description": "The comms layer for multi-agent AI. Cross-installation agent federation with zero-trust security, PII-gated data flow, and compliance-grade audit trails.",
            "icon": "🌐",
            "path": "ruflo/plugins/ruflo-federation/README.md"
        },
        {
            "id": "ruflo-iot-cognitum",
            "title": "Iot Cognitum (ruflo-iot-cognitum)",
            "description": "IoT device lifecycle, telemetry anomaly detection, fleet management, and witness chain verification for Cognitum Seed hardware.",
            "icon": "📡",
            "path": "ruflo/plugins/ruflo-iot-cognitum/README.md"
        },
        {
            "id": "ruflo-market-data",
            "title": "Market Data (ruflo-market-data)",
            "description": "Market data ingestion -- feed normalization, OHLCV vectorization, and candlestick pattern detection (read-only analysis, no order placement).",
            "icon": "📉",
            "path": "ruflo/plugins/ruflo-market-data/README.md"
        },
        {
            "id": "ruflo-music",
            "title": "Music (ruflo-music)",
            "description": "AI music generation via [Cognitum Music](https://music.cognitum.one) — compose lyrics/prompts, generate tracks, separate stems, extract MIDI, and master, all through the `cogmusic`...",
            "icon": "🎵",
            "path": "ruflo/plugins/ruflo-music/README.md"
        },
        {
            "id": "ruflo-neural-trader",
            "title": "Neural Trader (ruflo-neural-trader)",
            "description": "Neural trading strategies powered by [`neural-trader`](https://www.npmjs.com/package/neural-trader) (v2.7+) — self-learning LSTM/Transformer/N-BEATS models, Rust/NAPI backtesting (...",
            "icon": "📈",
            "path": "ruflo/plugins/ruflo-neural-trader/README.md"
        },
        {
            "id": "ruflo-ruos",
            "title": "Ruos (ruflo-ruos)",
            "description": "Run ruflo swarm agents on **your own ruOS cloud desktops**. The plugin can:",
            "icon": "🖥️",
            "path": "ruflo/plugins/ruflo-ruos/README.md"
        },
        {
            "id": "ruflo-x-gateway",
            "title": "X Gateway (ruflo-x-gateway)",
            "description": "MCP gateway for the **open ruflo swarm federation**. Coordination rides an open, **membership-gated, signed Nostr relay** — every message is a signed Nostr event",
            "icon": "🚪",
            "path": "ruflo/plugins/ruflo-x-gateway/README.md"
        }
    ],
    "AGENTES: CORE & DEV": [
        {
            "id": "agent-coder",
            "title": "Coder",
            "description": "Implementation specialist for writing clean, efficient code",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/core/coder.md"
        },
        {
            "id": "agent-planner",
            "title": "Planner",
            "description": "Strategic planning and task orchestration agent",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/core/planner.md"
        },
        {
            "id": "agent-researcher",
            "title": "Researcher",
            "description": "Deep research and information gathering specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/core/researcher.md"
        },
        {
            "id": "agent-reviewer",
            "title": "Reviewer",
            "description": "Code review and quality assurance specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/core/reviewer.md"
        },
        {
            "id": "agent-tester",
            "title": "Tester",
            "description": "Comprehensive testing and quality assurance specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/core/tester.md"
        },
        {
            "id": "agent-backend-dev",
            "title": "Backend Dev",
            "description": "Specialized agent for backend API development with self-learning and pattern recognition",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/development/dev-backend-api.md"
        },
        {
            "id": "agent-backend-dev",
            "title": "Backend Dev",
            "description": "Specialized agent for backend API development, including REST and GraphQL endpoints",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/development/backend/dev-backend-api.md"
        }
    ],
    "AGENTES: CONSENSO & HIVE-MIND": [
        {
            "id": "agent-byzantine-coordinator",
            "title": "Byzantine Coordinator",
            "description": "Coordinates Byzantine fault-tolerant consensus protocols with malicious actor detection",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/consensus/byzantine-coordinator.md"
        },
        {
            "id": "agent-crdt-synchronizer",
            "title": "Crdt Synchronizer",
            "description": "Implements Conflict-free Replicated Data Types for eventually consistent state synchronization",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/consensus/crdt-synchronizer.md"
        },
        {
            "id": "agent-gossip-coordinator",
            "title": "Gossip Coordinator",
            "description": "Coordinates gossip-based consensus protocols for scalable eventually consistent systems",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/consensus/gossip-coordinator.md"
        },
        {
            "id": "agent-performance-benchmarker",
            "title": "Performance Benchmarker",
            "description": "Implements comprehensive performance benchmarking for distributed consensus protocols",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/consensus/performance-benchmarker.md"
        },
        {
            "id": "agent-quorum-manager",
            "title": "Quorum Manager",
            "description": "Implements dynamic quorum adjustment and intelligent membership management",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/consensus/quorum-manager.md"
        },
        {
            "id": "agent-raft-manager",
            "title": "Raft Manager",
            "description": "Manages Raft consensus algorithm with leader election and log replication",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/consensus/raft-manager.md"
        },
        {
            "id": "agent-security-manager",
            "title": "Security Manager",
            "description": "Implements comprehensive security mechanisms for distributed consensus protocols",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/consensus/security-manager.md"
        },
        {
            "id": "agent-collective-intelligence-coordinator",
            "title": "Collective Intelligence Coordinator",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/hive-mind/collective-intelligence-coordinator.md"
        },
        {
            "id": "agent-queen-coordinator",
            "title": "Queen Coordinator",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/hive-mind/queen-coordinator.md"
        },
        {
            "id": "agent-scout-explorer",
            "title": "Scout Explorer",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/hive-mind/scout-explorer.md"
        },
        {
            "id": "agent-swarm-memory-manager",
            "title": "Swarm Memory Manager",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/hive-mind/swarm-memory-manager.md"
        },
        {
            "id": "agent-worker-specialist",
            "title": "Worker Specialist",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/hive-mind/worker-specialist.md"
        }
    ],
    "AGENTES: SWARM & COORDENAÇÃO": [
        {
            "id": "agent-codex-coordinator",
            "title": "Codex Coordinator",
            "description": "Coordinates multiple headless Codex workers for parallel execution",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/dual-mode/codex-coordinator.md"
        },
        {
            "id": "agent-codex-worker",
            "title": "Codex Worker",
            "description": "Headless Codex background worker for parallel task execution with self-learning",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/dual-mode/codex-worker.md"
        },
        {
            "id": "agent-dual-orchestrator",
            "title": "Dual Orchestrator",
            "description": "Orchestrates Claude Code (interactive) + Codex (headless) for hybrid workflows",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/dual-mode/dual-orchestrator.md"
        },
        {
            "id": "agent-sublinear-goal-planner",
            "title": "Sublinear Goal Planner",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/goal/agent.md"
        },
        {
            "id": "agent-code-goal-planner",
            "title": "Code Goal Planner",
            "description": "Code-centric Goal-Oriented Action Planning specialist that creates intelligent plans for software development objectives. Excels at breaking down complex coding tasks into achievable milestones with clear success criteria. Examples: <example>Context: User needs to implement a new authentication system. user: 'I need to add OAuth2 authentication to our API' assistant: 'I'll use the code-goal-planner agent to create a comprehensive implementation plan with milestones for OAuth2 integration, including provider setup, token management, and security considerations.' <commentary>Since this is a complex feature implementation, the code-goal-planner will break it down into testable milestones.</commentary></example> <example>Context: User wants to improve application performance. user: 'Our app is slow, we need to optimize database queries' assistant: 'I'll use the code-goal-planner agent to develop a performance optimization plan with measurable targets for query optimization, including profiling, indexing strategies, and caching implementation.' <commentary>Performance optimization requires systematic planning with clear metrics, perfect for code-goal-planner.</commentary></example>",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/goal/code-goal-planner.md"
        },
        {
            "id": "agent-goal-planner",
            "title": "Goal Planner",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/goal/goal-planner.md"
        },
        {
            "id": "agent-sublinear-goal-planner",
            "title": "Sublinear Goal Planner",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/reasoning/agent.md"
        },
        {
            "id": "agent-goal-planner",
            "title": "Goal Planner",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/reasoning/goal-planner.md"
        },
        {
            "id": "agent-adaptive-coordinator",
            "title": "Adaptive Coordinator",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/swarm/adaptive-coordinator.md"
        },
        {
            "id": "agent-hierarchical-coordinator",
            "title": "Hierarchical Coordinator",
            "description": "Queen-led hierarchical swarm coordination with specialized worker delegation",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/swarm/hierarchical-coordinator.md"
        },
        {
            "id": "agent-mesh-coordinator",
            "title": "Mesh Coordinator",
            "description": "Peer-to-peer mesh network swarm with distributed decision making and fault tolerance",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/swarm/mesh-coordinator.md"
        }
    ],
    "AGENTES: SPARC & ARQUITETURA": [
        {
            "id": "agent-system-architect",
            "title": "System Architect",
            "description": "Expert agent for system architecture design, patterns, and high-level technical decisions",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/architecture/system-design/arch-system-design.md"
        },
        {
            "id": "agent-architecture",
            "title": "Architecture",
            "description": "SPARC Architecture phase specialist for system design",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/sparc/architecture.md"
        },
        {
            "id": "agent-pseudocode",
            "title": "Pseudocode",
            "description": "SPARC Pseudocode phase specialist for algorithm design",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/sparc/pseudocode.md"
        },
        {
            "id": "agent-refinement",
            "title": "Refinement",
            "description": "SPARC Refinement phase specialist for iterative improvement",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/sparc/refinement.md"
        },
        {
            "id": "agent-specification",
            "title": "Specification",
            "description": "SPARC Specification phase specialist for requirements analysis",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/sparc/specification.md"
        }
    ],
    "AGENTES: DEVOPS & GITHUB": [
        {
            "id": "agent-cicd-engineer",
            "title": "Cicd Engineer",
            "description": "Specialized agent for GitHub Actions CI/CD pipeline creation and optimization",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/devops/ci-cd/ops-cicd-github.md"
        },
        {
            "id": "agent-api-docs",
            "title": "Api Docs",
            "description": "Expert agent for creating and maintaining OpenAPI/Swagger documentation",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/documentation/api-docs/docs-api-openapi.md"
        },
        {
            "id": "agent-code-review-swarm",
            "title": "Code Review Swarm",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/code-review-swarm.md"
        },
        {
            "id": "agent-github-modes",
            "title": "Github Modes",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/github-modes.md"
        },
        {
            "id": "agent-issue-tracker",
            "title": "Issue Tracker",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/issue-tracker.md"
        },
        {
            "id": "agent-multi-repo-swarm",
            "title": "Multi Repo Swarm",
            "description": "Cross-repository swarm orchestration for organization-wide automation and intelligent collaboration",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/multi-repo-swarm.md"
        },
        {
            "id": "agent-pr-manager",
            "title": "Pr Manager",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/pr-manager.md"
        },
        {
            "id": "agent-project-board-sync",
            "title": "Project Board Sync",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/project-board-sync.md"
        },
        {
            "id": "agent-release-manager",
            "title": "Release Manager",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/release-manager.md"
        },
        {
            "id": "agent-release-swarm",
            "title": "Release Swarm",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/release-swarm.md"
        },
        {
            "id": "agent-repo-architect",
            "title": "Repo Architect",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/repo-architect.md"
        },
        {
            "id": "agent-swarm-issue",
            "title": "Swarm Issue",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/swarm-issue.md"
        },
        {
            "id": "agent-swarm-pr",
            "title": "Swarm Pr",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/swarm-pr.md"
        },
        {
            "id": "agent-sync-coordinator",
            "title": "Sync Coordinator",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/sync-coordinator.md"
        },
        {
            "id": "agent-workflow-automation",
            "title": "Workflow Automation",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/github/workflow-automation.md"
        }
    ],
    "AGENTES: OTIMIZAÇÃO & PERFORMANCE": [
        {
            "id": "agent-safla-neural",
            "title": "Safla Neural",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/neural/safla-neural.md"
        },
        {
            "id": "agent-Benchmark Suite",
            "title": "Benchmark Suite",
            "description": "Comprehensive performance benchmarking, regression detection and performance validation",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/optimization/benchmark-suite.md"
        },
        {
            "id": "agent-Load Balancing Coordinator",
            "title": "Load Balancing Coordinator",
            "description": "Dynamic task distribution, work-stealing algorithms and adaptive load balancing",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/optimization/load-balancer.md"
        },
        {
            "id": "agent-Performance Monitor",
            "title": "Performance Monitor",
            "description": "Real-time metrics collection, bottleneck analysis, SLA monitoring and anomaly detection",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/optimization/performance-monitor.md"
        },
        {
            "id": "agent-Resource Allocator",
            "title": "Resource Allocator",
            "description": "Adaptive resource allocation, predictive scaling and intelligent capacity planning",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/optimization/resource-allocator.md"
        },
        {
            "id": "agent-Topology Optimizer",
            "title": "Topology Optimizer",
            "description": "Dynamic swarm topology reconfiguration and communication pattern optimization",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/optimization/topology-optimizer.md"
        },
        {
            "id": "agent-sona-learning-optimizer",
            "title": "Sona Learning Optimizer",
            "description": "SONA-powered self-optimizing agent with LoRA fine-tuning and EWC++ memory preservation",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/sona/sona-learning-optimizer.md"
        },
        {
            "id": "agent-consensus-coordinator",
            "title": "Consensus Coordinator",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/sublinear/consensus-coordinator.md"
        },
        {
            "id": "agent-matrix-optimizer",
            "title": "Matrix Optimizer",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/sublinear/matrix-optimizer.md"
        },
        {
            "id": "agent-pagerank-analyzer",
            "title": "Pagerank Analyzer",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/sublinear/pagerank-analyzer.md"
        },
        {
            "id": "agent-performance-optimizer",
            "title": "Performance Optimizer",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/sublinear/performance-optimizer.md"
        },
        {
            "id": "agent-trading-predictor",
            "title": "Trading Predictor",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/sublinear/trading-predictor.md"
        }
    ],
    "AGENTES: V3 FLEET & ESPECIALISTAS": [
        {
            "id": "agent-ml-developer",
            "title": "Ml Developer",
            "description": "Specialized agent for machine learning model development, training, and deployment",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/data/ml/data-ml-model.md"
        },
        {
            "id": "agent-mobile-dev",
            "title": "Mobile Dev",
            "description": "Expert agent for React Native mobile application development across iOS and Android",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/specialized/mobile/spec-mobile-react-native.md"
        },
        {
            "id": "agent-production-validator",
            "title": "Production Validator",
            "description": "Production validation specialist ensuring applications are fully implemented and deployment-ready",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/testing/production-validator.md"
        },
        {
            "id": "agent-tdd-london-swarm",
            "title": "Tdd London Swarm",
            "description": "TDD London School specialist for mock-driven development within swarm coordination",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/testing/tdd-london-swarm.md"
        },
        {
            "id": "agent-tdd-london-swarm",
            "title": "Tdd London Swarm",
            "description": "TDD London School specialist for mock-driven development within swarm coordination",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/testing/unit/tdd-london-swarm.md"
        },
        {
            "id": "agent-production-validator",
            "title": "Production Validator",
            "description": "Production validation specialist ensuring applications are fully implemented and deployment-ready",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/testing/validation/production-validator.md"
        },
        {
            "id": "agent-database-specialist",
            "title": "Database Specialist",
            "description": "Database design and optimization specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/v3/database-specialist.md"
        },
        {
            "id": "agent-project-coordinator",
            "title": "Project Coordinator",
            "description": "Coordinates multi-agent workflows for this project",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/v3/project-coordinator.md"
        },
        {
            "id": "agent-python-specialist",
            "title": "Python Specialist",
            "description": "Python development specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/v3/python-specialist.md"
        },
        {
            "id": "agent-test-architect",
            "title": "Test Architect",
            "description": "Testing and quality assurance specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/v3/test-architect.md"
        },
        {
            "id": "agent-typescript-specialist",
            "title": "Typescript Specialist",
            "description": "TypeScript development specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/v3/typescript-specialist.md"
        },
        {
            "id": "agent-v3-integration-architect",
            "title": "V3 Integration Architect",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/v3/v3-integration-architect.md"
        },
        {
            "id": "agent-v3-memory-specialist",
            "title": "V3 Memory Specialist",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/v3/v3-memory-specialist.md"
        },
        {
            "id": "agent-v3-performance-engineer",
            "title": "V3 Performance Engineer",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/v3/v3-performance-engineer.md"
        },
        {
            "id": "agent-v3-queen-coordinator",
            "title": "V3 Queen Coordinator",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/v3/v3-queen-coordinator.md"
        },
        {
            "id": "agent-v3-security-architect",
            "title": "V3 Security Architect",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/v3/v3-security-architect.md"
        }
    ],
    "AGENTES: ESPECIALIZADOS DIVERSOS": [
        {
            "id": "agent-base-template-generator",
            "title": "Base Template Generator",
            "description": "Use this agent when you need to create foundational templates, boilerplate code, or starter configurations for new projects, components, or features. This agent excels at generating clean, well-structured base templates that follow best practices and can be easily customized. Examples: <example>Context: User needs to start a new React component and wants a solid foundation. user: 'I need to create a new user profile component' assistant: 'I'll use the base-template-generator agent to create a comprehensive React component template with proper structure, TypeScript definitions, and styling setup.' <commentary>Since the user needs a foundational template for a new component, use the base-template-generator agent to create a well-structured starting point.</commentary></example> <example>Context: User is setting up a new API endpoint and needs a template. user: 'Can you help me set up a new REST API endpoint for user management?' assistant: 'I'll use the base-template-generator agent to create a complete API endpoint template with proper error handling, validation, and documentation structure.' <commentary>The user needs a foundational template for an API endpoint, so use the base-template-generator agent to provide a comprehensive starting point.</commentary></example>",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/base-template-generator.md"
        },
        {
            "id": "agent-database-specialist",
            "title": "Database Specialist",
            "description": "Database design and optimization specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/database-specialist.md"
        },
        {
            "id": "agent-project-coordinator",
            "title": "Project Coordinator",
            "description": "Coordinates multi-agent workflows for this project",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/project-coordinator.md"
        },
        {
            "id": "agent-python-specialist",
            "title": "Python Specialist",
            "description": "Python development specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/python-specialist.md"
        },
        {
            "id": "agent-security-auditor",
            "title": "Security Auditor",
            "description": "Security audit and hardening specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/security-auditor.md"
        },
        {
            "id": "agent-typescript-specialist",
            "title": "Typescript Specialist",
            "description": "TypeScript development specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/typescript-specialist.md"
        },
        {
            "id": "agent-code-analyzer",
            "title": "Code Analyzer",
            "description": "Advanced code quality analysis agent for comprehensive code reviews and improvements",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/analysis/analyze-code-quality.md"
        },
        {
            "id": "agent-analyst",
            "title": "Analyst",
            "description": "Advanced code quality analysis agent for comprehensive code reviews and improvements",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/analysis/code-analyzer.md"
        },
        {
            "id": "agent-code-analyzer",
            "title": "Code Analyzer",
            "description": "Advanced code quality analysis agent for comprehensive code reviews and improvements",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/analysis/code-review/analyze-code-quality.md"
        },
        {
            "id": "agent-test-long-runner",
            "title": "Test Long Runner",
            "description": "Test agent that can run for 30+ minutes on complex tasks",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/custom/test-long-runner.md"
        },
        {
            "id": "agent-flow-nexus-app-store",
            "title": "Flow Nexus App Store",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/flow-nexus/app-store.md"
        },
        {
            "id": "agent-flow-nexus-auth",
            "title": "Flow Nexus Auth",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/flow-nexus/authentication.md"
        },
        {
            "id": "agent-flow-nexus-challenges",
            "title": "Flow Nexus Challenges",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/flow-nexus/challenges.md"
        },
        {
            "id": "agent-flow-nexus-neural",
            "title": "Flow Nexus Neural",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/flow-nexus/neural-network.md"
        },
        {
            "id": "agent-flow-nexus-payments",
            "title": "Flow Nexus Payments",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/flow-nexus/payments.md"
        },
        {
            "id": "agent-flow-nexus-sandbox",
            "title": "Flow Nexus Sandbox",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/flow-nexus/sandbox.md"
        },
        {
            "id": "agent-flow-nexus-swarm",
            "title": "Flow Nexus Swarm",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/flow-nexus/swarm.md"
        },
        {
            "id": "agent-flow-nexus-user-tools",
            "title": "Flow Nexus User Tools",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/flow-nexus/user-tools.md"
        },
        {
            "id": "agent-flow-nexus-workflow",
            "title": "Flow Nexus Workflow",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/flow-nexus/workflow.md"
        },
        {
            "id": "agent-agentic-payments",
            "title": "Agentic Payments",
            "description": "|",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/payments/agentic-payments.md"
        },
        {
            "id": "agent-smart-agent",
            "title": "Smart Agent",
            "description": "Intelligent agent coordination and dynamic spawning specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/templates/automation-smart-agent.md"
        },
        {
            "id": "agent-swarm-init",
            "title": "Swarm Init",
            "description": "Swarm initialization and topology optimization specialist",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/templates/coordinator-swarm-init.md"
        },
        {
            "id": "agent-pr-manager",
            "title": "Pr Manager",
            "description": "Complete pull request lifecycle management and GitHub workflow coordination",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/templates/github-pr-manager.md"
        },
        {
            "id": "agent-sparc-coder",
            "title": "Sparc Coder",
            "description": "Transform specifications into working code with TDD practices",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/templates/implementer-sparc-coder.md"
        },
        {
            "id": "agent-memory-coordinator",
            "title": "Memory Coordinator",
            "description": "Manage persistent memory across sessions and facilitate cross-agent memory sharing",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/templates/memory-coordinator.md"
        },
        {
            "id": "agent-migration-planner",
            "title": "Migration Planner",
            "description": "Comprehensive migration plan for converting commands to agent-based system",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/templates/migration-plan.md"
        },
        {
            "id": "agent-task-orchestrator",
            "title": "Task Orchestrator",
            "description": "Central coordination agent for task decomposition, execution planning, and result synthesis",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/templates/orchestrator-task.md"
        },
        {
            "id": "agent-perf-analyzer",
            "title": "Perf Analyzer",
            "description": "Performance bottleneck analyzer for identifying and resolving workflow inefficiencies",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/templates/performance-analyzer.md"
        },
        {
            "id": "agent-sparc-coord",
            "title": "Sparc Coord",
            "description": "SPARC methodology orchestrator for systematic development phase coordination",
            "icon": "🤖",
            "path": "ruflo/.claude/agents/templates/sparc-coordinator.md"
        }
    ]
};

if(typeof module !== 'undefined') module.exports = rufloData;
