import pytest
import os
import numpy as np
from fastapi.testclient import TestClient
from api.server import app
from ai_explainer.code_explainer import CodeExplainer
from search.semantic_search import SemanticSearch
from vector_store.faiss_index import FaissIndex
from indexer.embedding_generator import EmbeddingGenerator
from indexer.repo_scanner import RepoScanner
from analysis.repo_metrics import analyze_repository
from analysis.architecture_graph import compute_architecture_data, build_architecture_graph
from analysis.focused_graph import build_focused_graph

client = TestClient(app)

def test_cors_headers():
    response = client.get("/stats", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") in ["*", "http://localhost:3000"]

def test_ai_explainer_multi_paradigms():
    embs_gen = EmbeddingGenerator()
    vs = FaissIndex(dimension=384)
    search_eng = SemanticSearch(embs_gen, vs)
    explainer = CodeExplainer(search_eng)

    # 1. Python function
    res_py = explainer.explain_code("def authenticate_user(token: str):\n    return verify_jwt(token)")
    assert "functional entity" in res_py
    assert "authentication" in res_py.lower()

    # 2. Database query block
    res_db = explainer.explain_code("def query_user_records(db_conn):\n    return db.query('SELECT * FROM users')")
    assert "database operations" in res_db.lower()

    # 3. Class structure
    res_class = explainer.explain_code("class VectorEngine:\n    def __init__(self):\n        pass")
    assert "class structure" in res_class

    # 4. Search and retrieval snippet
    res_search = explainer.explain_code("def retrieve_vector_index(query_embed, index):\n    return index.search(query_embed)")
    assert "information retrieval" in res_search.lower()

def test_repo_scanner_ignore_rules(tmp_path):
    # Create test directory structure with ignored and included folders
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "main.py").write_text("def main(): pass", encoding="utf-8")

    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "config.py").write_text("# ignored", encoding="utf-8")

    node_dir = tmp_path / "node_modules"
    node_dir.mkdir()
    (node_dir / "package.js").write_text("// ignored", encoding="utf-8")

    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    (venv_dir / "lib.py").write_text("# ignored", encoding="utf-8")

    scanner = RepoScanner(str(tmp_path))
    scanned = scanner.scan()
    
    assert len(scanned) == 1
    assert "main.py" in scanned[0]

def test_embedding_generator_properties():
    gen = EmbeddingGenerator()
    assert gen.device in ["cuda", "mps", "cpu"]
    
    # Empty list handling
    empty_res = gen.generate([])
    assert isinstance(empty_res, np.ndarray)
    assert empty_res.shape == (0, 384)

    # Single string batching
    single_res = gen.generate(["test query"])
    assert single_res.shape == (1, 384)
    assert single_res.dtype == np.float32

def test_architecture_coupling_analytics():
    sample_meta = [
        {"name": "AuthController", "file_path": "auth/controller.py", "type": "class", "code_snippet": "import db\nfrom utils import log\ndef login(): db_connect()"},
        {"name": "db_connect", "file_path": "db/connector.py", "type": "function", "code_snippet": "def db_connect(): pass"},
        {"name": "log", "file_path": "utils/logger.py", "type": "function", "code_snippet": "def log(): pass"},
        {"name": "App", "file_path": "main.py", "type": "class", "code_snippet": "import auth\ndef run(): AuthController()"}
    ]

    metrics = analyze_repository(sample_meta)
    assert metrics["number_of_functions"] == 2
    assert metrics["number_of_classes"] == 2
    assert metrics["number_of_files"] == 4
    assert metrics["number_of_modules"] >= 3
    assert metrics["total_functions"] == 2
    assert metrics["total_classes"] == 2

    G = compute_architecture_data(sample_meta)
    assert len(G.nodes) > 0
    
    fig = build_architecture_graph(sample_meta)
    assert fig is not None

def test_focused_neighborhood_graph():
    sample_meta = [
        {"name": "parse_code", "file_path": "parser.py", "type": "function", "code_snippet": "def parse_code(): extract_tokens()"},
        {"name": "extract_tokens", "file_path": "lexer.py", "type": "function", "code_snippet": "def extract_tokens(): pass"},
        {"name": "run_pipeline", "file_path": "main.py", "type": "function", "code_snippet": "def run_pipeline(): parse_code()"}
    ]

    fig = build_focused_graph("parse_code", sample_meta)
    assert fig is not None
    
    # Non-existent symbol returns None
    fig_none = build_focused_graph("non_existent_symbol_123", sample_meta)
    assert fig_none is None
