# Project Roadmap

The **AI Code Intelligence Engine** roadmap outlines planned enhancements and strategic milestones for upcoming releases.

---

## 🎯 Short-Term Goals (v2.1 - v2.2)

- [ ] **Additional Tree-sitter Parsers**:
  - Add native AST parsing support for **Rust** (`.rs`), **Go** (`.go`), **TypeScript** (`.ts`, `.tsx`), and **C#** (`.cs`).
- [ ] **Real-Time File Watcher (Live Indexing)**:
  - Implement an optional background daemon (`watchdog`) to re-index modified files incrementally without needing full repository re-scans.
- [ ] **Export & Reporting Tools**:
  - Add one-click CSV and JSON report exports for Code Smell candidates and Module Coupling metrics directly from the UI.
- [ ] **Theme Customization**:
  - Provide an optional syntax highlighting theme switcher (Light / Dark code blocks) within the floating header.

---

## 🚀 Medium-Term Goals (v2.3 - v2.5)

- [ ] **Local LLM Integration (Ollama / vLLM)**:
  - Add native support for local open-weight coding LLMs (e.g. `deepseek-coder`, `qwen2.5-coder`, `codellama`) for fully offline generative explanations and automated refactoring suggestions.
- [ ] **Cross-Language Semantic Call Tracking**:
  - Enhance call-graph extraction to recognize inter-service communication (REST API calls, gRPC endpoints, and microservice definitions).
- [ ] **FAISS Index Scaling (HNSW & IVF)**:
  - Add configuration switches to use FAISS HNSW or IVF indices for ultra-large codebases (> 1 million LOC) to guarantee sub-10ms query times.

---

## 🌟 Long-Term Vision (v3.0+)

- [ ] **IDE Extensions**:
  - Release lightweight VS Code and JetBrains plugins connecting directly to the running FastAPI engine for in-editor semantic navigation and architectural overlays.
- [ ] **Team & CI/CD Quality Gate**:
  - GitHub Action to run Quality Guard audits during Pull Requests and block merges that introduce critical cyclomatic complexity spikes or circular dependencies.
- [ ] **Multi-Repository Knowledge Federation**:
  - Support federated indexing across multiple interrelated microservices in an enterprise organization.
