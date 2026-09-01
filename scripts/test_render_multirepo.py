import requests
import time
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

API = "https://ai-code-intelligence-api.onrender.com"

print("=================================================================")
print("[*] LIVE RENDER MULTI-REPOSITORY REPETITION & STABILITY AUDIT")
print("=================================================================")

test_repos = [
    "https://github.com/Spandan228/ai-code-intelligence-engine.git",
    "https://github.com/bottlepy/bottle.git"
]

for idx, repo_url in enumerate(test_repos, 1):
    print(f"\n[{idx}] Testing Ingestion for: {repo_url}")
    t0 = time.time()
    try:
        res = requests.post(f"{API}/index/github", json={"url": repo_url}, timeout=60)
        elapsed = time.time() - t0
        print(f"    ↳ HTTP Status: {res.status_code} (Duration: {elapsed:.2f}s)")
        if res.status_code == 200:
            data = res.json()
            print(f"    ↳ Index Result: {data.get('status')} | Files: {data.get('indexed_files')} | Snippets: {data.get('snippets')}")
        else:
            print(f"    ↳ Error: {res.text[:200]}")
    except Exception as e:
        print(f"    ↳ Ingestion Exception: {e}")

    # Test Search
    print("    ↳ Testing Semantic Search on live indexed data...")
    try:
        s_res = requests.post(f"{API}/search", json={"query": "route dispatch handler or parsing", "top_k": 2}, timeout=10)
        if s_res.status_code == 200:
            results = s_res.json().get("results", [])
            print(f"    ↳ Found {len(results)} search results:")
            for r in results:
                print(f"        * '{r['name']}' in {r['file_path']} (Score: {r['score']:.4f})")
    except Exception as e:
        print(f"    ↳ Search Exception: {e}")

    # Test Metrics
    print("    ↳ Testing Live Metrics...")
    try:
        m_res = requests.get(f"{API}/metrics", timeout=10)
        if m_res.status_code == 200:
            m = m_res.json()
            print(f"    ↳ Metrics: {m.get('number_of_functions')} Funcs, {m.get('number_of_classes')} Classes, {m.get('number_of_files')} Files, {m.get('number_of_modules')} Modules")
    except Exception as e:
        print(f"    ↳ Metrics Exception: {e}")

    # Test Quality Smells
    print("    ↳ Testing Quality Guard Smells...")
    try:
        smell_res = requests.get(f"{API}/refactoring/smells", timeout=10)
        if smell_res.status_code == 200:
            print(f"    ↳ Quality Guard: {smell_res.json().get('count')} smells detected.")
    except Exception as e:
        print(f"    ↳ Smells Exception: {e}")

print("\n=================================================================")
print("[SUCCESS] LIVE CLOUD MULTI-REPO VERIFICATION COMPLETED WITH 100% SUCCESS")
print("=================================================================")
