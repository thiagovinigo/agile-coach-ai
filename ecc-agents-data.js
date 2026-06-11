const eccAgentsData = [
    {
        "id": "a11y-architect",
        "title": "A11Y Architect",
        "description": "Accessibility Architect specializing in WCAG 2.2 compliance for Web and Native platforms. Use PROACTIVELY when designing UI components, establishing design systems, or auditing code for inclusive user experiences.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/a11y-architect.md"
    },
    {
        "id": "architect",
        "title": "Architect",
        "description": "Software architecture specialist for system design, scalability, and technical decision-making. Use PROACTIVELY when planning new features, refactoring large systems, or making architectural decisions.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/architect.md"
    },
    {
        "id": "build-error-resolver",
        "title": "Build Error Resolver",
        "description": "Build and TypeScript error resolution specialist. Use PROACTIVELY when build fails or type errors occur. Fixes build/type errors only with minimal diffs, no architectural edits. Focuses on getting the build green quickly.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/build-error-resolver.md"
    },
    {
        "id": "chief-of-staff",
        "title": "Chief Of Staff",
        "description": "Personal communication chief of staff that triages email, Slack, LINE, and Messenger. Classifies messages into 4 tiers (skip/info_only/meeting_info/action_required), generates draft replies, and enforces post-send follow-through via hooks. Use when managing multi-channel communication workflows.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/chief-of-staff.md"
    },
    {
        "id": "code-architect",
        "title": "Code Architect",
        "description": "Designs feature architectures by analyzing existing codebase patterns and conventions, then providing implementation blueprints with concrete files, interfaces, data flow, and build order.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/code-architect.md"
    },
    {
        "id": "code-explorer",
        "title": "Code Explorer",
        "description": "Deeply analyzes existing codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies to inform new development.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/code-explorer.md"
    },
    {
        "id": "code-reviewer",
        "title": "Code Reviewer",
        "description": "Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code. MUST BE USED for all code changes.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/code-reviewer.md"
    },
    {
        "id": "code-simplifier",
        "title": "Code Simplifier",
        "description": "Simplifies and refines code for clarity, consistency, and maintainability while preserving behavior. Focus on recently modified code unless instructed otherwise.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/code-simplifier.md"
    },
    {
        "id": "comment-analyzer",
        "title": "Comment Analyzer",
        "description": "Analyze code comments for accuracy, completeness, maintainability, and comment rot risk.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/comment-analyzer.md"
    },
    {
        "id": "conversation-analyzer",
        "title": "Conversation Analyzer",
        "description": "Use this agent when analyzing conversation transcripts to find behaviors worth preventing with hooks. Triggered by /hookify without arguments.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/conversation-analyzer.md"
    },
    {
        "id": "cpp-build-resolver",
        "title": "Cpp Build Resolver",
        "description": "C++ build, CMake, and compilation error resolution specialist. Fixes build errors, linker issues, and template errors with minimal changes. Use when C++ builds fail.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/cpp-build-resolver.md"
    },
    {
        "id": "cpp-reviewer",
        "title": "Cpp Reviewer",
        "description": "Expert C++ code reviewer specializing in memory safety, modern C++ idioms, concurrency, and performance. Use for all C++ code changes. MUST BE USED for C++ projects.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/cpp-reviewer.md"
    },
    {
        "id": "csharp-reviewer",
        "title": "Csharp Reviewer",
        "description": "Expert C# code reviewer specializing in .NET conventions, async patterns, security, nullable reference types, and performance. Use for all C# code changes. MUST BE USED for C# projects.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/csharp-reviewer.md"
    },
    {
        "id": "dart-build-resolver",
        "title": "Dart Build Resolver",
        "description": "Dart/Flutter build, analysis, and dependency error resolution specialist. Fixes `dart analyze` errors, Flutter compilation failures, pub dependency conflicts, and build_runner issues with minimal, surgical changes. Use when Dart/Flutter builds fail.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/dart-build-resolver.md"
    },
    {
        "id": "database-reviewer",
        "title": "Database Reviewer",
        "description": "PostgreSQL database specialist for query optimization, schema design, security, and performance. Use PROACTIVELY when writing SQL, creating migrations, designing schemas, or troubleshooting database performance. Incorporates Supabase best practices.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/database-reviewer.md"
    },
    {
        "id": "django-build-resolver",
        "title": "Django Build Resolver",
        "description": "Django/Python build, migration, and dependency error resolution specialist. Fixes pip/Poetry errors, migration conflicts, import errors, Django configuration issues, and collectstatic failures with minimal changes. Use when Django setup or startup fails.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/django-build-resolver.md"
    },
    {
        "id": "django-reviewer",
        "title": "Django Reviewer",
        "description": "Expert Django code reviewer specializing in ORM correctness, DRF patterns, migration safety, security misconfigurations, and production-grade Django practices. Use for all Django code changes. MUST BE USED for Django projects.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/django-reviewer.md"
    },
    {
        "id": "doc-updater",
        "title": "Doc Updater",
        "description": "Documentation and codemap specialist. Use PROACTIVELY for updating codemaps and documentation. Runs /update-codemaps and /update-docs, generates docs/CODEMAPS/*, updates READMEs and guides.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/doc-updater.md"
    },
    {
        "id": "docs-lookup",
        "title": "Docs Lookup",
        "description": "When the user asks how to use a library, framework, or API or needs up-to-date code examples, use Context7 MCP to fetch current documentation and return answers with examples. Invoke for docs/API/setup questions.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/docs-lookup.md"
    },
    {
        "id": "e2e-runner",
        "title": "E2E Runner",
        "description": "End-to-end testing specialist using Vercel Agent Browser (preferred) with Playwright fallback. Use PROACTIVELY for generating, maintaining, and running E2E tests. Manages test journeys, quarantines flaky tests, uploads artifacts (screenshots, videos, traces), and ensures critical user flows work.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/e2e-runner.md"
    },
    {
        "id": "fastapi-reviewer",
        "title": "Fastapi Reviewer",
        "description": "Reviews FastAPI applications for async correctness, dependency injection, Pydantic schemas, security, OpenAPI quality, testing, and production readiness.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/fastapi-reviewer.md"
    },
    {
        "id": "flutter-reviewer",
        "title": "Flutter Reviewer",
        "description": "Flutter and Dart code reviewer. Reviews Flutter code for widget best practices, state management patterns, Dart idioms, performance pitfalls, accessibility, and clean architecture violations. Library-agnostic — works with any state management solution and tooling.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/flutter-reviewer.md"
    },
    {
        "id": "fsharp-reviewer",
        "title": "Fsharp Reviewer",
        "description": "Expert F# code reviewer specializing in functional idioms, type safety, pattern matching, computation expressions, and performance. Use for all F# code changes. MUST BE USED for F# projects.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/fsharp-reviewer.md"
    },
    {
        "id": "gan-evaluator",
        "title": "Gan Evaluator",
        "description": "GAN Harness — Evaluator agent. Tests the live running application via Playwright, scores against rubric, and provides actionable feedback to the Generator.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/gan-evaluator.md"
    },
    {
        "id": "gan-generator",
        "title": "Gan Generator",
        "description": "GAN Harness — Generator agent. Implements features according to the spec, reads evaluator feedback, and iterates until quality threshold is met.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/gan-generator.md"
    },
    {
        "id": "gan-planner",
        "title": "Gan Planner",
        "description": "GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features, sprints, evaluation criteria, and design direction.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/gan-planner.md"
    },
    {
        "id": "go-build-resolver",
        "title": "Go Build Resolver",
        "description": "Go build, vet, and compilation error resolution specialist. Fixes build errors, go vet issues, and linter warnings with minimal changes. Use when Go builds fail.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/go-build-resolver.md"
    },
    {
        "id": "go-reviewer",
        "title": "Go Reviewer",
        "description": "Expert Go code reviewer specializing in idiomatic Go, concurrency patterns, error handling, and performance. Use for all Go code changes. MUST BE USED for Go projects.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/go-reviewer.md"
    },
    {
        "id": "harmonyos-app-resolver",
        "title": "Harmonyos App Resolver",
        "description": "HarmonyOS application development expert specializing in ArkTS and ArkUI. Reviews code for V2 state management compliance, Navigation routing patterns, API usage, and performance best practices. Use for HarmonyOS/OpenHarmony projects.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/harmonyos-app-resolver.md"
    },
    {
        "id": "harness-optimizer",
        "title": "Harness Optimizer",
        "description": "Analyze and improve the local agent harness configuration for reliability, cost, and throughput.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/harness-optimizer.md"
    },
    {
        "id": "healthcare-reviewer",
        "title": "Healthcare Reviewer",
        "description": "Reviews healthcare application code for clinical safety, CDSS accuracy, PHI compliance, and medical data integrity. Specialized for EMR/EHR, clinical decision support, and health information systems.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/healthcare-reviewer.md"
    },
    {
        "id": "homelab-architect",
        "title": "Homelab Architect",
        "description": "Designs home and small-lab network plans from hardware inventory, goals, and operator experience level, with safe staged changes and rollback guidance.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/homelab-architect.md"
    },
    {
        "id": "java-build-resolver",
        "title": "Java Build Resolver",
        "description": "Java/Maven/Gradle build, compilation, and dependency error resolution specialist. Automatically detects Spring Boot or Quarkus and applies framework-specific fixes. Fixes build errors, Java compiler errors, and Maven/Gradle issues with minimal changes. Use when Java builds fail.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/java-build-resolver.md"
    },
    {
        "id": "java-reviewer",
        "title": "Java Reviewer",
        "description": "Expert Java code reviewer for Spring Boot and Quarkus projects. Automatically detects the framework and applies the appropriate review rules. Covers layered architecture, JPA/Panache, MongoDB, security, and concurrency. MUST BE USED for all Java code changes.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/java-reviewer.md"
    },
    {
        "id": "kotlin-build-resolver",
        "title": "Kotlin Build Resolver",
        "description": "Kotlin/Gradle build, compilation, and dependency error resolution specialist. Fixes build errors, Kotlin compiler errors, and Gradle issues with minimal changes. Use when Kotlin builds fail.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/kotlin-build-resolver.md"
    },
    {
        "id": "kotlin-reviewer",
        "title": "Kotlin Reviewer",
        "description": "Kotlin and Android/KMP code reviewer. Reviews Kotlin code for idiomatic patterns, coroutine safety, Compose best practices, clean architecture violations, and common Android pitfalls.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/kotlin-reviewer.md"
    },
    {
        "id": "loop-operator",
        "title": "Loop Operator",
        "description": "Operate autonomous agent loops, monitor progress, and intervene safely when loops stall.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/loop-operator.md"
    },
    {
        "id": "marketing-agent",
        "title": "Marketing Agent",
        "description": "Marketing strategist and copywriter for campaign planning, audience research, positioning, copy creation, and content review. Covers landing pages, email sequences, social posts, ad copy, short-form video scripts, and content calendars. Use when the user wants to plan or execute a product launch or marketing campaign.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/marketing-agent.md"
    },
    {
        "id": "mle-reviewer",
        "title": "Mle Reviewer",
        "description": "Production machine-learning engineering reviewer for data contracts, feature pipelines, training reproducibility, offline/online evaluation, model serving, monitoring, and rollback. Use when ML, MLOps, model training, inference, feature store, or evaluation code changes.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/mle-reviewer.md"
    },
    {
        "id": "network-architect",
        "title": "Network Architect",
        "description": "Designs enterprise or multi-site network architecture from requirements, using existing network skills for focused routing, validation, automation, and troubleshooting detail.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/network-architect.md"
    },
    {
        "id": "network-config-reviewer",
        "title": "Network Config Reviewer",
        "description": "Reviews router and switch configurations for security, correctness, stale references, risky change-window commands, and missing operational guardrails.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/network-config-reviewer.md"
    },
    {
        "id": "network-troubleshooter",
        "title": "Network Troubleshooter",
        "description": "Diagnoses network connectivity, routing, DNS, interface, and policy symptoms with a read-only OSI-layer workflow and evidence-backed root cause summary.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/network-troubleshooter.md"
    },
    {
        "id": "opensource-forker",
        "title": "Opensource Forker",
        "description": "Fork any project for open-sourcing. Copies files, strips secrets and credentials (20+ patterns), replaces internal references with placeholders, generates .env.example, and cleans git history. First stage of the opensource-pipeline skill.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/opensource-forker.md"
    },
    {
        "id": "opensource-packager",
        "title": "Opensource Packager",
        "description": "Generate complete open-source packaging for a sanitized project. Produces CLAUDE.md, setup.sh, README.md, LICENSE, CONTRIBUTING.md, and GitHub issue templates. Makes any repo immediately usable with Claude Code. Third stage of the opensource-pipeline skill.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/opensource-packager.md"
    },
    {
        "id": "opensource-sanitizer",
        "title": "Opensource Sanitizer",
        "description": "Verify an open-source fork is fully sanitized before release. Scans for leaked secrets, PII, internal references, and dangerous files using 20+ regex patterns. Generates a PASS/FAIL/PASS-WITH-WARNINGS report. Second stage of the opensource-pipeline skill. Use PROACTIVELY before any public release.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/opensource-sanitizer.md"
    },
    {
        "id": "performance-optimizer",
        "title": "Performance Optimizer",
        "description": "Performance analysis and optimization specialist. Use PROACTIVELY for identifying bottlenecks, optimizing slow code, reducing bundle sizes, and improving runtime performance. Profiling, memory leaks, render optimization, and algorithmic improvements.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/performance-optimizer.md"
    },
    {
        "id": "planner",
        "title": "Planner",
        "description": "Expert planning specialist for complex features and refactoring. Use PROACTIVELY when users request feature implementation, architectural changes, or complex refactoring. Automatically activated for planning tasks.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/planner.md"
    },
    {
        "id": "pr-test-analyzer",
        "title": "Pr Test Analyzer",
        "description": "Review pull request test coverage quality and completeness, with emphasis on behavioral coverage and real bug prevention.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/pr-test-analyzer.md"
    },
    {
        "id": "python-reviewer",
        "title": "Python Reviewer",
        "description": "Expert Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance. Use for all Python code changes. MUST BE USED for Python projects.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/python-reviewer.md"
    },
    {
        "id": "pytorch-build-resolver",
        "title": "Pytorch Build Resolver",
        "description": "PyTorch runtime, CUDA, and training error resolution specialist. Fixes tensor shape mismatches, device errors, gradient issues, DataLoader problems, and mixed precision failures with minimal changes. Use when PyTorch training or inference crashes.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/pytorch-build-resolver.md"
    },
    {
        "id": "refactor-cleaner",
        "title": "Refactor Cleaner",
        "description": "Dead code cleanup and consolidation specialist. Use PROACTIVELY for removing unused code, duplicates, and refactoring. Runs analysis tools (knip, depcheck, ts-prune) to identify dead code and safely removes it.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/refactor-cleaner.md"
    },
    {
        "id": "rust-build-resolver",
        "title": "Rust Build Resolver",
        "description": "Rust build, compilation, and dependency error resolution specialist. Fixes cargo build errors, borrow checker issues, and Cargo.toml problems with minimal changes. Use when Rust builds fail.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/rust-build-resolver.md"
    },
    {
        "id": "rust-reviewer",
        "title": "Rust Reviewer",
        "description": "Expert Rust code reviewer specializing in ownership, lifetimes, error handling, unsafe usage, and idiomatic patterns. Use for all Rust code changes. MUST BE USED for Rust projects.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/rust-reviewer.md"
    },
    {
        "id": "security-reviewer",
        "title": "Security Reviewer",
        "description": "Security vulnerability detection and remediation specialist. Use PROACTIVELY after writing code that handles user input, authentication, API endpoints, or sensitive data. Flags secrets, SSRF, injection, unsafe crypto, and OWASP Top 10 vulnerabilities.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/security-reviewer.md"
    },
    {
        "id": "seo-specialist",
        "title": "Seo Specialist",
        "description": "SEO specialist for technical SEO audits, on-page optimization, structured data, Core Web Vitals, and content/keyword mapping. Use for site audits, meta tag reviews, schema markup, sitemap and robots issues, and SEO remediation plans.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/seo-specialist.md"
    },
    {
        "id": "silent-failure-hunter",
        "title": "Silent Failure Hunter",
        "description": "Review code for silent failures, swallowed errors, bad fallbacks, and missing error propagation.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/silent-failure-hunter.md"
    },
    {
        "id": "swift-build-resolver",
        "title": "Swift Build Resolver",
        "description": "Swift/Xcode build, compilation, and dependency error resolution specialist. Fixes swift build errors, Xcode build failures, SPM dependency issues, and code signing problems with minimal changes. Use when Swift builds fail.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/swift-build-resolver.md"
    },
    {
        "id": "swift-reviewer",
        "title": "Swift Reviewer",
        "description": "Expert Swift code reviewer specializing in protocol-oriented design, value semantics, ARC memory management, Swift Concurrency, and idiomatic patterns. Use for all Swift code changes. MUST BE USED for Swift projects.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/swift-reviewer.md"
    },
    {
        "id": "tdd-guide",
        "title": "Tdd Guide",
        "description": "Test-Driven Development specialist enforcing write-tests-first methodology. Use PROACTIVELY when writing new features, fixing bugs, or refactoring code. Ensures 80%+ test coverage.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/tdd-guide.md"
    },
    {
        "id": "type-design-analyzer",
        "title": "Type Design Analyzer",
        "description": "Analyze type design for encapsulation, invariant expression, usefulness, and enforcement.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/type-design-analyzer.md"
    },
    {
        "id": "typescript-reviewer",
        "title": "Typescript Reviewer",
        "description": "Expert TypeScript/JavaScript code reviewer specializing in type safety, async correctness, Node/web security, and idiomatic patterns. Use for all TypeScript and JavaScript code changes. MUST BE USED for TypeScript/JavaScript projects.",
        "icon": "🤖",
        "path": "contexto/ECC-main/agents/typescript-reviewer.md"
    }
];
