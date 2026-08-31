import pytest
import os
import numpy as np
from fastapi.testclient import TestClient

from parsers.python_parser import PythonParser
from parsers.javascript_parser import JavaScriptParser
from parsers.java_parser import JavaParser
from parsers.c_parser import CParser
from parsers.cpp_parser import CPPParser
from indexer.repo_scanner import RepoScanner
from indexer.language_detector import LanguageDetector
from indexer.code_parser import CodeParserOrchestrator
from indexer.embedding_generator import EmbeddingGenerator
from vector_store.faiss_index import FaissIndex
from search.semantic_search import SemanticSearch
from dependency_graph.graph_builder import GraphBuilder
from analysis.repo_metrics import analyze_repository
from analysis.architecture_graph import build_architecture_graph
from analysis.focused_graph import build_focused_graph
from refactoring.code_smell_detector import CodeSmellDetector
from navigation.code_navigation import CodeNavigation
from ai_explainer.code_explainer import CodeExplainer
from api.server import app

client = TestClient(app)

# ==================== 1. PARSER TESTS ====================

def test_python_parser():
    parser = PythonParser()
    code = """
def standalone_func(a, b):
    return a + b

class Calculator:
    def add(self, x, y):
        return x + y
"""
    results = parser.parse_code(code, "calc.py")
    assert len(results) == 3
    names = [r["name"] for r in results]
    assert "standalone_func" in names
    assert "Calculator" in names
    assert "add" in names
    assert results[0]["language"] == "python"

def test_javascript_parser():
    parser = JavaScriptParser()
    code = """
class DataService {
    fetchData() { return []; }
}
function processItems(items) { return items.map(x => x * 2); }
const handleEvent = (event) => { console.log(event); };
"""
    results = parser.parse_code(code, "service.js")
    assert len(results) >= 3
    names = [r["name"] for r in results]
    assert "DataService" in names
    assert "processItems" in names
    assert "handleEvent" in names
    assert results[0]["language"] == "javascript"

def test_java_parser():
    parser = JavaParser()
    code = """
public class AccountManager {
    public AccountManager() {}
    public boolean authenticate(String user, String pass) {
        return true;
    }
}
"""
    results = parser.parse_code(code, "AccountManager.java")
    assert len(results) == 3
    names = [r["name"] for r in results]
    assert "AccountManager" in names
    assert "authenticate" in names

def test_c_parser():
    parser = CParser()
    code = """
struct Config {
    int port;
    char* host;
};

int start_server(struct Config* cfg) {
    return 0;
}
"""
    results = parser.parse_code(code, "server.c")
    assert len(results) == 2
    names = [r["name"] for r in results]
    assert "Config" in names
    assert "start_server" in names

def test_cpp_parser():
    parser = CPPParser()
    code = """
namespace graphics {
class Renderer {
public:
    void render_frame() {}
};
struct Color { int r, g, b; };
int initialize_renderer() { return 1; }
}
"""
    results = parser.parse_code(code, "renderer.cpp")
    assert len(results) >= 3
    names = [r["name"] for r in results]
    assert "graphics" in names
    assert "Renderer" in names
    assert "initialize_renderer" in names

# ==================== 2. SCANNER & DETECTOR TESTS ====================

def test_language_detector():
    assert LanguageDetector.get_language("foo.py") == "python"
    assert LanguageDetector.get_language("bar.js") == "javascript"
    assert LanguageDetector.get_language("baz.java") == "java"
    assert LanguageDetector.get_language("qux.c") == "c"
    assert LanguageDetector.get_language("qux.cpp") == "cpp"
    assert LanguageDetector.get_language("header.h") == "c"
    assert LanguageDetector.get_language("header.hpp") == "cpp"
    assert LanguageDetector.get_language("unknown.txt") == "unknown"
    assert LanguageDetector.is_supported("test.py") is True
    assert LanguageDetector.is_supported("test.rs") is False

def test_repo_scanner_and_orchestrator():
    scanner = RepoScanner(".")
    files = scanner.scan()
    assert len(files) > 0
    # Should not include .git
    for f in files:
        assert "\\.git\\" not in f and "/.git/" not in f

    orchestrator = CodeParserOrchestrator()
    snippets = orchestrator.parse_file(files[0])
    assert isinstance(snippets, list)

# ==================== 3. VECTOR STORE & SEARCH TESTS ====================

def test_faiss_vector_store():
    vs = FaissIndex(dimension=4)
    embs = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]], dtype=np.float32)
    meta = [
        {"name": "func_a", "file_path": "a.py", "type": "function", "language": "python", "code_snippet": "def func_a(): pass", "start_line": 1},
        {"name": "func_b", "file_path": "b.py", "type": "function", "language": "python", "code_snippet": "def func_b(): pass", "start_line": 1}
    ]
    vs.add_embeddings(embs, meta)
    assert len(vs.metadata) == 2
    assert vs.index.ntotal == 2

    # Query closest to func_a
    query = np.array([[0.9, 0.1, 0.0, 0.0]], dtype=np.float32)
    res = vs.search(query, top_k=2)
    assert len(res) == 2
    assert res[0][0]["name"] == "func_a"

    # Reset
    vs.reset()
    assert len(vs.metadata) == 0
    assert vs.index.ntotal == 0
    assert vs.search(query) == []

# ==================== 4. GRAPH & ANALYSIS TESTS ====================

def test_dependency_graph():
    metadata = [
        {"name": "init_app", "file_path": "app.py", "type": "function", "code_snippet": "def init_app(): create_db(); run_server()"},
        {"name": "create_db", "file_path": "db.py", "type": "function", "code_snippet": "def create_db(): pass"},
        {"name": "run_server", "file_path": "server.py", "type": "function", "code_snippet": "def run_server(): pass"}
    ]
    gb = GraphBuilder()
    gb.build_from_metadata(metadata)
    assert len(gb.graph.nodes) == 3
    assert len(gb.graph.edges) == 2

    fig = gb.get_visualization()
    assert fig is not None

    # Empty graph safeguard
    gb_empty = GraphBuilder()
    fig_empty = gb_empty.get_visualization()
    assert fig_empty is not None

def test_repo_metrics_and_architecture():
    metadata = [
        {"name": "login", "file_path": "auth/login.py", "type": "function", "code_snippet": "def login(): connect_db()"},
        {"name": "connect_db", "file_path": "db/connector.py", "type": "function", "code_snippet": "def connect_db(): pass"},
        {"name": "User", "file_path": "models/user.py", "type": "class", "code_snippet": "class User: pass"}
    ]
    metrics = analyze_repository(metadata)
    assert metrics["number_of_functions"] == 2
    assert metrics["number_of_classes"] == 1
    assert metrics["number_of_files"] == 3
    assert metrics["number_of_modules"] == 3
    assert metrics["total_dependencies"] == 1

    arch_fig = build_architecture_graph(metadata)
    assert arch_fig is not None

    # Focused graph
    focused_fig = build_focused_graph("login", metadata)
    assert focused_fig is not None

    # Non-existent target
    assert build_focused_graph("nonexistent_target_12345", metadata) is None

# ==================== 5. CODE SMELLS & AI EXPLAINER ====================

def test_code_smells_detection():
    detector = CodeSmellDetector()
    # Complex function
    complex_code = """
def complex_fn(a, b, c, d, e):
    if a:
        if b:
            if c:
                if d:
                    return e
                elif e:
                    return d
            elif b:
                return c
        elif a:
            return b
    return 0
"""
    smells = detector.detect_smells(complex_code, "complex.py")
    assert isinstance(smells, list)

    # Large function
    large_code = "def large_fn():\n" + "    x = 1\n" * 60
    large_smells = detector.detect_smells(large_code, "large.py")
    assert any(s["type"] == "Large Function" for s in large_smells)

def test_ai_explainer():
    class DummySearch:
        def search(self, query, top_k=3):
            return [{"name": "login_user", "file_path": "auth.py", "score": 0.85}]

    explainer = CodeExplainer(DummySearch())
    exp = explainer.explain_code("def login_user(username, password): return check_credentials(username, password)")
    assert "AI Code Explanation" in exp
    assert "login_user" in exp
    assert "authentication" in exp

def test_code_navigation():
    meta = [
        {"name": "AuthService", "file_path": "services/auth.py", "type": "class", "code_snippet": "class AuthService: pass"},
        {"name": "main", "file_path": "main.py", "type": "function", "code_snippet": "def main(): s = AuthService()"}
    ]
    nav = CodeNavigation(meta)
    defs = nav.jump_to_definition("AuthService")
    assert len(defs) == 1
    assert defs[0]["file_path"] == "services/auth.py"

    usages = nav.find_usages("AuthService")
    assert len(usages) == 1
    assert usages[0]["name"] == "main"

# ==================== 6. FASTAPI ENDPOINTS VIA TESTCLIENT ====================

def test_api_endpoints():
    # Clear index
    r = client.post("/index/clear")
    assert r.status_code == 200

    # Stats when empty
    r = client.get("/stats")
    assert r.status_code == 200
    assert r.json()["total_snippets"] == 0

    # Index tests dir
    r = client.post("/index/local", json={"path": "tests"})
    assert r.status_code == 200
    assert r.json()["status"] == "success"

    # Search
    r = client.post("/search", json={"query": "authenticate and login", "top_k": 3})
    assert r.status_code == 200
    assert "results" in r.json()

    # Metrics
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "number_of_functions" in r.json()

    # Dependency graph count
    r = client.get("/dependency-graph")
    assert r.status_code == 200
    assert "nodes" in r.json()

    # Architecture graph
    r = client.get("/architecture")
    assert r.status_code == 200

    # Code smells
    r = client.get("/refactoring/smells")
    assert r.status_code == 200

    # Navigation definition & usages
    r = client.get("/navigation/definition", params={"name": "login"})
    assert r.status_code == 200

    r = client.get("/navigation/usages", params={"name": "login"})
    assert r.status_code == 200

    # Explain
    r = client.post("/explain", json={"code_snippet": "def login(user, pass): return True"})
    assert r.status_code == 200
    assert "explanation" in r.json()
