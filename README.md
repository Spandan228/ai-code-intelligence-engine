# 🧠 AI Code Intelligence Engine

> **AI-powered developer intelligence platform for exploring, searching, and analyzing large codebases.**

---

## 🌟 Project Overview

The **AI Code Intelligence Engine** is a sophisticated developer tool designed to bridge the gap between complex codebases and developer understanding. By leveraging state-of-the-art Natural Language Processing (NLP) and graph analysis, it provides a comprehensive suite of tools for semantic exploration, dependency visualization, and automated code comprehension.

Whether you're onboarding to a new repository, performing a large-scale refactor, or simply trying to find "where that logic is," this engine provides the insights you need instantly.

---

## 🚀 Features

- **📂 Multi-Source Indexing**: Index local directories or clone and index GitHub repositories directly from the dashboard.
- **🔍 Semantic Code Search**: Look beyond keywords. Search for logic and intent using natural language queries powered by FAISS and sentence embeddings.
- **🧩 Dependency Visualization**: Interactive, project-wide dependency graphs showing how entities connect.
- **🎯 Focused Graph Analysis**: Isolation of specific functions or classes to see their immediate callers and callees.
- **🏗️ Architecture Insights**: High-level module dependency maps to understand the macro-structure of your project.
- **📈 Repository Analytics**: Real-time metrics on function density, class distribution, and project "hotspots."
- **🤖 AI Code Explainer**: Instant, context-aware explanations of code snippets using semantic neighborhood analysis.
- **🚩 Quality Guard**: Automated code smell detection to identify potential refactoring candidates.

---

## 🏗️ Architecture Overview

The system is built with a modular, service-oriented architecture:

- **Frontend**: A reactive **Streamlit** dashboard providing an interactive user experience.
- **Backend**: A high-performance **FastAPI** server managing indexing, search, and analysis logic.
- **Parsing**: **Tree-sitter** based multi-language parsers for precise Abstract Syntax Tree (AST) traversal.
- **Intelligence**: **Sentence-Transformers** for embedding generation and **FAISS** for millisecond-latency similarity search.
- **Analysis**: **NetworkX** and **Plotly** for complex graph computations and interactive visualizations.

---

## 🛠️ Tech Stack

- **Languge**: Python 3.11+
- **API Framework**: FastAPI & Uvicorn
- **UI Framework**: Streamlit
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Code Parsing**: Tree-sitter
- **Graph Engine**: NetworkX & Plotly
- **Data Handling**: NumPy & Pandas
- **Logging**: Rich

---

## 📁 Project Folder Structure

```text
ai-code-intelligence-engine/
├── ai_explainer/         # AI-based code explanation module
├── analysis/             # Advanced repository analysis tools (Focused & Architecture)
├── api/                  # FastAPI backend services & endpoints
├── data/                 # Local storage for vector indices and metadata
├── dependency_graph/     # Core dependency graph building logic
├── indexer/              # Codebase scanning, parsing, and embedding engine
├── parsers/              # Tree-sitter language-specific configurations
├── refactoring/          # Code smell detection and quality analysis
├── search/               # Semantic search logic
├── ui/                   # Streamlit dashboard interface
│   └── components/       # Reusable UI modules (metrics, graphs, etc.)
├── utils/                # Shared helper utilities (logging, decorators)
├── vector_store/         # FAISS vector database integration
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

## ⚙️ Installation Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-code-intelligence-engine.git
cd ai-code-intelligence-engine
```

### 2. Set Up Environment
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🖥️ How to Run the Project

The project requires both the backend API and the frontend dashboard to be running.

### 1. Start the FastAPI Backend
```bash
uvicorn api.server:app --reload
```
The API will be available at `http://localhost:8000`. You can view the interactive API docs at `/docs`.

### 2. Start the Streamlit Dashboard
Open a new terminal and run:
```bash
streamlit run ui/dashboard.py
```
The dashboard will launch in your default browser at `http://localhost:8501`.

---

## 💡 Example Usage

1.  **Index Your Code**: Go to the **Home** tab and paste the absolute path to your local repository.
2.  **Search Logic**: Use the **Semantic Search** tab to ask "How does the authentication flow work?".
3.  **Visualize Deps**: Switch to **Dependency Graph** to see a full interactive map of your project.
4.  **Target Analysis**: Use **Focused Graph** and type a function name (e.g., `login_user`) to see exactly what calls it.
5.  **Get Explanations**: Paste a confusing block of code into the **AI Code Explanation** tab to understand its purpose.

---

## 🔮 Future Improvements

- [ ] Support for additional languages (Go, Rust, Ruby).
- [ ] Integration with Large Language Models (LLMs) like GPT-4 or Claude for deeper code synthesis.
- [ ] Real-time indexing via file watchers.
- [ ] Multi-user support and collaborative workspaces.
- [ ] Enhanced dependency tracking for external libraries.

---

## 🤝 Contribution Guide

Contributions are welcome! If you'd like to improve the engine:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

*Built with ❤️ using Python, FastAPI, FAISS, Tree-sitter, and Streamlit.*
