# Contributing to AI Code Intelligence Engine

Thank you for your interest in contributing to the **AI Code Intelligence Engine**! This project is an open-source platform dedicated to multi-language code comprehension, AST parsing, dense vector similarity search, and interactive topology analytics.

We welcome contributions of all kinds: bug fixes, performance improvements, new AST parsers, architectural enhancements, UI/UX polish, and documentation refinements.

---

## 🛠️ Development Setup

### 1. Prerequisites
- **Python 3.10 or 3.11+**
- **Git**
- A C/C++ compiler toolchain (standard on macOS/Linux; Build Tools for Visual Studio on Windows) for Tree-sitter native compilation if installing from source.

### 2. Fork and Clone
```bash
git clone https://github.com/your-username/ai-code-intelligence-engine.git
cd ai-code-intelligence-engine
```

### 3. Create a Virtual Environment
```bash
# On Linux / macOS
python3 -m venv venv
source venv/bin/activate

# On Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🧪 Running Local Services

### Start the FastAPI Backend
```bash
python -m uvicorn api.server:app --host 127.0.0.1 --port 8000 --reload
```
The REST API documentation will be available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### Start the Streamlit Dashboard
In a separate terminal window:
```bash
python -m streamlit run ui/dashboard.py --server.port 8501
```
The web interface will launch at [http://localhost:8501](http://localhost:8501).

---

## 🔬 Testing Guidelines

All submissions must include corresponding automated tests and maintain a 100% pass rate.

### Run All Automated Tests
```bash
python -m pytest tests/ -v
```

### Test Coverage Checklist:
- **Parser tests** in `tests/test_parsers.py` and `tests/test_full_suite.py`.
- **API endpoint tests** in `tests/test_api_endpoints.py`.
- **Robustness, input validation, and security edge-case tests** in `tests/test_robustness_and_security.py`.

---

## 📐 Architecture & Coding Standards

1. **Strict No-Fake-Functionality Rule**: Never create synthetic analytics, fake trends, or simulated metrics. All visualizations and tables must derive from actual AST parsing, FAISS vector search, or Radon metrics.
2. **Design Tokens & UI Consistency**: When modifying UI components in `ui/components/`, strictly use the Reference Design System tokens defined in `ui/components/styles.py` (Warm Alabaster Canvas `#f1f3f7`, Pure White Bento Cards `#ffffff`, Sunset Tangerine Brand `#f97316`, Plus Jakarta Sans, and JetBrains Mono).
3. **Typing & Docstrings**: Include type hints and concise docstrings on all public functions, classes, and REST route handlers.
4. **Error Handling**: Gracefully handle missing files, unsupported extensions, syntax errors, and empty indices without crashing the application.

---

## 🚀 Submitting a Pull Request

1. **Branch Naming**: Use descriptive branch prefixes:
   - `feature/add-rust-parser`
   - `fix/git-clone-timeout`
   - `docs/update-api-guide`
   - `refactor/optimize-vector-batching`
2. **Commit Messages**: Follow Conventional Commits format (e.g. `feat(indexer): add support for rust ast parsing`, `fix(api): sanitize search query whitespace`).
3. **Verify Locally**:
   - Ensure all automated tests pass: `python -m pytest tests/`
   - Run the application and test your changes end-to-end.
4. **Open a PR**: Fill out the provided Pull Request template and link any relevant open issues.

---

## 📜 Community & Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
