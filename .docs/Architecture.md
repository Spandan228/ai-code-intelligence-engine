# Architecture & System Flow

## 1. Technology Stack
- **Language**: Python 3.10+
- **Backend API**: FastAPI, Uvicorn, Pydantic v2
- **Vector Database**: FAISS-CPU (L2 Normalized Inner Product)
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`, 384 dimensions)
- **Parsing Engine**: Tree-sitter (`tree-sitter-python`, `tree-sitter-javascript`, `tree-sitter-java`, `tree-sitter-c`, `tree-sitter-cpp`)
- **Graph & Visualization**: NetworkX, Plotly
- **Quality & Metrics**: Radon, AST, NumPy, Pandas
- **Frontend Dashboard**: Streamlit

## 2. Directory Layout
```
ai-code-intelligence-engine/
├── .docs/                  # 6-Document AI Specification Framework
│   ├── PRD.md
│   ├── Architecture.md
│   ├── Rules.md
│   ├── Phases.md
│   ├── Design.md
│   └── Memory.md
├── ai_explainer/           # AI code explanation logic
├── analysis/               # Repo metrics, focused graph, architecture graph
├── api/                    # FastAPI server & route handlers
├── data/                   # FAISS index and metadata storage
├── dependency_graph/       # NetworkX call graph builder
├── indexer/                # Scanner, language detector, embedding generator, GitHub cloner
├── navigation/             # Jump to definition & symbol usages
├── parsers/                # Tree-sitter multi-language parsers
├── refactoring/            # Radon complexity & code smell detector
├── search/                 # Semantic search coordinator
├── tests/                  # Unit and integration test suites
├── ui/                     # Streamlit frontend & UI components
│   └── components/
├── utils/                  # Config, logger, constants
├── requirements.txt
└── README.md
```

## 3. Data Flow & Contracts
1. **Indexing Flow**: `RepoScanner` -> `LanguageDetector` -> `CodeParserOrchestrator` -> `EmbeddingGenerator` -> `FaissIndex` -> `data/indices/`.
2. **Search Flow**: Query string -> `EmbeddingGenerator` -> `FaissIndex.search()` -> cosine similarity ranked results.
3. **Graph Flow**: `FaissIndex.metadata` -> `GraphBuilder` / `build_architecture_graph` / `build_focused_graph` -> Plotly JSON figure -> Streamlit / API client.
4. **API Endpoints**:
   - `POST /index/local`, `POST /index/github`, `POST /index/clear`
   - `POST /search`, `GET /stats`
   - `GET /dependency-graph`, `GET /dependency-graph/full`, `GET /architecture`, `GET /focused-graph`
   - `GET /metrics`, `GET /refactoring/smells`
   - `GET /navigation/definition`, `GET /navigation/usages`
   - `POST /explain`
