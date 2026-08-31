# PRD: AI Code Intelligence Engine

## 1. Objective & Target Audience
- **Objective**: AI-powered developer intelligence platform for indexing, semantic search, dependency visualization, architecture inspection, code smell analysis, and explanation across large multi-language codebases.
- **Target Audience**: Software engineers, architects, and development teams onboarding, refactoring, or navigating complex codebases.

## 2. Core Functional Requirements
- **[P0] Multi-Language AST Parsing**: Extract functions, classes, methods, and structs from Python, JavaScript, Java, C, and C++ using Tree-sitter.
- **[P0] Semantic Code Search**: High-performance semantic retrieval using Sentence-Transformers (`all-MiniLM-L6-v2`) and FAISS with L2-normalized Inner Product similarity.
- **[P0] REST API Backend**: High-performance FastAPI server for local/GitHub indexing, query search, metrics, and graph endpoints.
- **[P0] Reactive UI Dashboard**: Streamlit dashboard providing interactive panels for indexing, search, dependency visualization, metrics, architecture, and code explanation.
- **[P1] Dependency & Architecture Visualization**: NetworkX and Plotly-powered call graphs, focused entity graphs, and module-level architecture maps.
- **[P1] Code Smells & Quality Guard**: Radon cyclomatic complexity and large-function detection across languages.
- **[P1] AI Code Explainer**: Semantic neighborhood retrieval with structured purpose and quality tips.
- **[P2] Code Navigation**: Jump-to-definition and find-usages symbol indexer.

## 3. Acceptance Criteria
- 100% pass rate across all automated unit and integration tests.
- Backend API running on `http://127.0.0.1:8000` responding with valid JSON schemas.
- Frontend Streamlit UI on `http://localhost:8501` executing all user flows without runtime exceptions.
- Cross-platform path normalization for Windows, Linux, and macOS.

## 4. Non-Goals (v1)
- Multi-user authentication & role-based access control (deferred to v2).
- Real-time file system watchers (deferred to v2).
