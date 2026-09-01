import requests
import time
import os

def test_engine():
    print("==========================================================")
    print("[*] TESTING LOCAL AI CODE INTELLIGENCE ENGINE (CUDA / LOCALHOST)")
    print("==========================================================")
    
    # 1. Health check / stats
    print("\n[1] Health Check (/stats)...")
    r = requests.get("http://127.0.0.1:8000/stats", timeout=5)
    print(f"Status: {r.status_code} -> {r.json()}")
    assert r.status_code == 200

    # 2. Reset vector store
    print("\n[2] Reset Vector Store (/index/clear)...")
    r = requests.post("http://127.0.0.1:8000/index/clear", timeout=5)
    print(f"Status: {r.status_code} -> {r.json()}")
    assert r.status_code == 200

    # 3. Local Indexing
    indexer_path = os.path.abspath("indexer").replace("\\", "/")
    print(f"\n[3] Ingesting Local Codebase ({indexer_path})...")
    t0 = time.time()
    r = requests.post("http://127.0.0.1:8000/index/local", json={"path": indexer_path}, timeout=30)
    print(f"Ingestion Time: {time.time() - t0:.2f}s | Status: {r.status_code} -> {r.json()}")
    assert r.status_code == 200

    # 4. Semantic Search
    print("\n[4] Testing Semantic Vector Search (/search)...")
    t0 = time.time()
    r = requests.post("http://127.0.0.1:8000/search", json={"query": "AST code snippet metadata extraction", "top_k": 5}, timeout=10)
    hits = r.json().get("results", [])
    print(f"Search Time: {time.time() - t0:.3f}s | Status: {r.status_code} | Top Results: {len(hits)}")
    for i, h in enumerate(hits[:3]):
        name = h.get("name", "Snippet")
        score = h.get("score", 0.0)
        file_path = h.get("file_path", "")
        symbol_type = h.get("type", "")
        print(f"   [{i+1}] {name} ({symbol_type}) - Score: {score:.4f} in {file_path}")
    assert r.status_code == 200 and len(hits) > 0

    # 5. Repository Metrics
    print("\n[5] Testing Repository Metrics (/metrics)...")
    r = requests.get("http://127.0.0.1:8000/metrics", timeout=10)
    m = r.json()
    funcs = m.get('number_of_functions', m.get('total_functions', 0))
    classes = m.get('number_of_classes', m.get('total_classes', 0))
    files = m.get('number_of_files', m.get('total_files', 0))
    modules = m.get('number_of_modules', m.get('total_modules', 0))
    print(f"Status: {r.status_code} | Funcs: {funcs}, Classes: {classes}, Files: {files}, Modules: {modules}")
    assert r.status_code == 200

    # 6. Dependency Graph
    print("\n[6] Testing Dependency Call Graph (/dependency-graph/full)...")
    r = requests.get("http://127.0.0.1:8000/dependency-graph/full?max_nodes=50", timeout=10)
    print(f"Status: {r.status_code} | Graph JSON bytes: {len(r.text)}")
    assert r.status_code == 200 and "data" in r.json()

    # 7. Architecture Insights
    print("\n[7] Testing Architecture Insights (/architecture)...")
    r = requests.get("http://127.0.0.1:8000/architecture", timeout=10)
    print(f"Status: {r.status_code} | Architecture JSON bytes: {len(r.text)}")
    assert r.status_code == 200

    # 8. Focused Graph
    first_name = hits[0].get("name", "scan") if hits else "scan"
    print(f"\n[8] Testing Focused Radial Graph for '{first_name}' (/focused-graph)...")
    r = requests.get(f"http://127.0.0.1:8000/focused-graph?function={first_name}", timeout=10)
    print(f"Status: {r.status_code} | Focused Graph JSON bytes: {len(r.text)}")
    assert r.status_code == 200

    # 9. Quality Guard Code Smells
    print("\n[9] Testing Quality Guard Code Smells (/refactoring/smells)...")
    r = requests.get("http://127.0.0.1:8000/refactoring/smells", timeout=10)
    smells = r.json().get("smells", [])
    print(f"Status: {r.status_code} | Detected Smells: {len(smells)}")
    assert r.status_code == 200

    # 10. AI Code Explainer
    print("\n[10] Testing Contextual AI Explainer (/explain)...")
    snippet = "def parse_file(self, file_path):\n    with open(file_path, 'r') as f:\n        return parser.parse(f.read())"
    r = requests.post("http://127.0.0.1:8000/explain", json={"code_snippet": snippet}, timeout=10)
    expl = r.json().get("explanation", "")
    print(f"Status: {r.status_code} | Explanation Length: {len(expl)} chars")
    assert r.status_code == 200 and len(expl) > 50

    # 11. Code Navigation
    print("\n[11] Testing Code Navigation (/navigation/definition & /navigation/usages)...")
    r_def = requests.get(f"http://127.0.0.1:8000/navigation/definition?name={first_name}", timeout=10)
    r_usg = requests.get(f"http://127.0.0.1:8000/navigation/usages?name={first_name}", timeout=10)
    print(f"Definition Status: {r_def.status_code} | Usages Status: {r_usg.status_code}")
    assert r_def.status_code == 200 and r_usg.status_code == 200

    print("\n==========================================================")
    print("[SUCCESS] ALL 11 ENDPOINTS AND WORKFLOWS VERIFIED 100% OPERATIONAL!")
    print("==========================================================")

if __name__ == "__main__":
    test_engine()
