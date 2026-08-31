# Changelog

All notable changes to the **AI Code Intelligence Engine** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-08-31

### Major Architecture & UI/UX Overhaul
- **Enterprise Design System**: Transitioned the entire frontend from legacy dark prototype styles to the Reference Design System featuring a Warm Alabaster Canvas (`#f1f3f7`), floating Pure White Bento Cards (`#ffffff`), Sunset Tangerine Brand palette (`#f97316`), and curated typography (Plus Jakarta Sans & JetBrains Mono).
- **Categorized Sidebar Navigation**: Redesigned navigation into 4 distinct functional zones (`WORKSPACE`, `INTELLIGENCE & SEARCH`, `TOPOLOGY & ARCHITECTURE`, `CODE QUALITY`) with custom active pill styling and zero radio circles.
- **Repository Ingestion Suite**: Dual-card Bento onboarding for Local Disk and Remote GitHub repositories with AST language tag indicator strip (`.py`, `.js`, `.java`, `.c`, `.cpp`).
- **Hero Analytics Dashboard**: 5 top KPI pods (Functions, Classes, Files, Modules, Dependencies) with horizontal baselines, alongside Connectivity Hotspots progress meters and Entity Composition breakdowns.
- **Semantic Vector Code Search**: Natural language query resolution with dense 384-dimensional embeddings, ranked result cards, exact cosine similarity scores, file breadcrumbs, and syntax blocks.
- **Topology Visualizers**: Interactive whole-repository call graph with layout physics options (`Force-Directed`, `Kamada-Kawai`), Max Node Budget slider, and degree filters on a clean white surface.
- **Focused Entity Radial Graph**: Radial concentric caller/callee isolation with dynamic quick-select hub suggestion chips.
- **Architecture Insights View**: Two-column split with a 360° Circular Package Shell Map on the left and Package Coupling Telemetry Table on the right.
- **Quality Guard & Code Smells**: Automated Radon cyclomatic complexity and large routine smell detection, 4 Health KPI pods, 3-tier Severity Risk Matrix (Critical, High, Medium), and prioritized refactoring candidate table with 1-click AI Explainer integration.
- **Contextual AI Code Explainer**: Multi-section context synthesis leveraging nearest vector neighbors to generate architectural purpose and quality guidance.
- **Robustness & Input Validation**: Added strict validation, shallow git cloning, comprehensive edge-case handling, and 25 automated unit/integration tests with a 100% pass rate.

---

## [1.0.0] - Initial Release

- Core FastAPI backend implementation.
- Basic Tree-sitter parsers for Python, JavaScript, Java, C, and C++.
- Initial FAISS vector indexing with sentence-transformers.
- Prototype Streamlit dashboard.
