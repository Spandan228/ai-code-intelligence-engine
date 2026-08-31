import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)

def test_live_api_lifecycle():
    # 1. Index local repo
    resp_index = client.post("/index/local", json={"path": "tests"})
    assert resp_index.status_code == 200
    assert resp_index.json()["status"] == "success"

    # 2. Stats
    resp_stats = client.get("/stats")
    assert resp_stats.status_code == 200
    assert resp_stats.json()["total_snippets"] > 0

    # 3. Search
    resp_search = client.post("/search", json={"query": "AST parsing and tree-sitter", "top_k": 3})
    assert resp_search.status_code == 200
    assert "results" in resp_search.json()

    # 4. Dependency graph
    resp_dep = client.get("/dependency-graph")
    assert resp_dep.status_code == 200
    assert "nodes" in resp_dep.json()

    # 5. Architecture
    resp_arch = client.get("/architecture")
    assert resp_arch.status_code == 200

    # 6. Metrics
    resp_metrics = client.get("/metrics")
    assert resp_metrics.status_code == 200
    assert "number_of_functions" in resp_metrics.json()

    # 7. Focused Graph
    resp_focused = client.get("/focused-graph", params={"function": "PythonParser"})
    assert resp_focused.status_code in [200, 404]

    # 8. Explain
    resp_explain = client.post("/explain", json={"code_snippet": "def login(user, pass):\n    if user == 'admin':\n        return True\n    return False"})
    assert resp_explain.status_code == 200
    assert len(resp_explain.json().get("explanation", "")) > 0

    # 9. Clean up
    client.post("/index/local", json={"path": "G:/project"})
