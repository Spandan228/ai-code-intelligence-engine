import pytest
import os
import tempfile
import numpy as np
from fastapi.testclient import TestClient
from api.server import app
from parsers.python_parser import PythonParser
from parsers.javascript_parser import JavaScriptParser
from parsers.java_parser import JavaParser
from parsers.c_parser import CParser
from parsers.cpp_parser import CPPParser
from indexer.code_parser import CodeParserOrchestrator
from vector_store.faiss_index import FaissIndex

client = TestClient(app)

# ==================== 1. API INPUT VALIDATION & ERROR HANDLING ====================

def test_index_local_invalid_paths():
    # Empty path
    r = client.post("/index/local", json={"path": "   "})
    assert r.status_code == 400
    assert "cannot be empty" in r.json()["detail"]

    # Non-existent path
    r = client.post("/index/local", json={"path": "non_existent_folder_xyz_123456"})
    assert r.status_code == 400
    assert "does not exist" in r.json()["detail"]

    # Path is a file, not a directory
    temp_f = tempfile.NamedTemporaryFile(delete=False)
    temp_f.close()
    try:
        r = client.post("/index/local", json={"path": temp_f.name})
        assert r.status_code == 400
        assert "not a directory" in r.json()["detail"]
    finally:
        os.unlink(temp_f.name)

def test_index_github_invalid_urls():
    # Empty URL
    r = client.post("/index/github", json={"url": ""})
    assert r.status_code == 400
    assert "cannot be empty" in r.json()["detail"]

    # Invalid repository URL
    r = client.post("/index/github", json={"url": "https://invalid-non-existent-domain-xyz.com/fake/repo.git"})
    assert r.status_code == 400
    assert "Remote indexing failed" in r.json()["detail"]

def test_search_edge_cases():
    # Empty query string
    r = client.post("/search", json={"query": ""})
    assert r.status_code == 200
    assert r.json()["results"] == []

    # Whitespace only
    r = client.post("/search", json={"query": "    \t\n  "})
    assert r.status_code == 200
    assert r.json()["results"] == []

    # XSS injection string
    r = client.post("/search", json={"query": "<script>alert('xss')</script>"})
    assert r.status_code == 200
    assert isinstance(r.json()["results"], list)

    # SQL injection string
    r = client.post("/search", json={"query": "' OR '1'='1' --"})
    assert r.status_code == 200
    assert isinstance(r.json()["results"], list)

    # Large top_k bounding
    r = client.post("/search", json={"query": "test query", "top_k": 9999})
    assert r.status_code == 200

def test_focused_graph_edge_cases():
    # Empty function parameter
    r = client.get("/focused-graph", params={"function": ""})
    assert r.status_code == 400

    # Whitespace function parameter
    r = client.get("/focused-graph", params={"function": "   "})
    assert r.status_code == 400

    # Non-existent symbol
    r = client.get("/focused-graph", params={"function": "totally_non_existent_function_9999"})
    assert r.status_code == 404

def test_explain_edge_cases():
    # Empty code snippet
    r = client.post("/explain", json={"code_snippet": ""})
    assert r.status_code == 400
    assert "cannot be empty" in r.json()["detail"]

    # Whitespace only snippet
    r = client.post("/explain", json={"code_snippet": "   \n\t  "})
    assert r.status_code == 400

def test_navigation_edge_cases():
    # Empty name
    r = client.get("/navigation/definition", params={"name": ""})
    assert r.status_code == 200
    assert r.json()["definitions"] == []

    r = client.get("/navigation/usages", params={"name": ""})
    assert r.status_code == 200
    assert r.json()["usages"] == []

# ==================== 2. PARSER ROBUSTNESS & MALFORMED CODE ====================

def test_parsers_on_empty_and_corrupted_code():
    parsers = [PythonParser(), JavaScriptParser(), JavaParser(), CParser(), CPPParser()]
    
    for parser in parsers:
        # Empty string
        res = parser.parse_code("", "empty_file")
        assert res == []

        # Whitespace only
        res = parser.parse_code("   \n\n\t  ", "ws_file")
        assert res == []

        # Only comments
        res = parser.parse_code("# A single comment\n// Another comment\n/* Block comment */", "comments_file")
        assert isinstance(res, list)

        # Syntax errors / garbage input
        res = parser.parse_code("!@#$%^&*()}{][\x00\x01\x02", "garbage_file")
        assert isinstance(res, list)

def test_parser_orchestrator_nonexistent_and_unsupported():
    orchestrator = CodeParserOrchestrator()
    
    # Unsupported extension
    res = orchestrator.parse_file("some_file.xyz_unsupported")
    assert res == []

    # Non-existent file
    res = orchestrator.parse_file("completely_missing_file.py")
    assert res == []

# ==================== 3. VECTOR STORE RESET & RECOVERY ====================

def test_faiss_reset_and_recovery():
    vs = FaissIndex(dimension=4)
    embs = np.array([[1.0, 0.0, 0.0, 0.0]], dtype=np.float32)
    meta = [{"name": "test_fn", "file_path": "test.py", "type": "function", "code_snippet": "def test_fn(): pass"}]
    
    vs.add_embeddings(embs, meta)
    assert vs.index.ntotal == 1
    
    vs.reset()
    assert vs.index.ntotal == 0
    assert len(vs.metadata) == 0

    # Search on reset index returns empty
    q = np.array([[1.0, 0.0, 0.0, 0.0]], dtype=np.float32)
    assert vs.search(q) == []
