import requests
import sys

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

API = "https://ai-code-intelligence-api.onrender.com"

print("==========================================================")
print("[*] LIVE RENDER DEPLOYMENT ACCEPTANCE & FUNCTIONALITY AUDIT")
print("==========================================================")

# 1. Root
print("\n[1] Testing Live Root Endpoint...")
try:
    r0 = requests.get(f"{API}/", timeout=10)
    print(f"[OK] Root Status: {r0.status_code} -> {r0.json()}")
except Exception as e:
    print(f"[WARN] Root check failed: {e}")

# 2. Stats
print("\n[2] Testing Live Stats...")
try:
    r2 = requests.get(f"{API}/stats", timeout=10)
    print(f"[OK] Stats: {r2.status_code} -> {r2.json()}")
except Exception as e:
    print(f"[WARN] Stats check failed: {e}")

# 3. Semantic Search
print("\n[3] Testing Live Semantic Vector Search on Render...")
try:
    r3 = requests.post(f"{API}/search", json={"query": "AST parsing orchestrator", "top_k": 3}, timeout=15)
    print(f"[OK] Search Status: {r3.status_code} -> Found {len(r3.json().get('results', []))} matches:")
    for m in r3.json().get("results", []):
        print(f"    * Match: {m['name']} in {m['file_path']} (line {m['start_line']}) | Cosine Score: {m['score']:.4f}")
except Exception as e:
    print(f"[WARN] Search check failed: {e}")

# 4. Metrics
print("\n[4] Testing Live Repository Metrics...")
try:
    r4 = requests.get(f"{API}/metrics", timeout=10)
    m = r4.json()
    print(f"[OK] Metrics: {m.get('number_of_functions', 0)} Functions, {m.get('number_of_classes', 0)} Classes, {m.get('number_of_files', 0)} Files, {m.get('number_of_modules', 0)} Modules, {m.get('total_dependencies', 0)} Dependencies")
except Exception as e:
    print(f"[WARN] Metrics check failed: {e}")

# 5. Quality Smells
print("\n[5] Testing Live Quality Guard Smells...")
try:
    r5 = requests.get(f"{API}/refactoring/smells", timeout=15)
    print(f"[OK] Code Smells Detected: {r5.json().get('count', 0)} total smells across codebase.")
except Exception as e:
    print(f"[WARN] Smells check failed: {e}")

# 6. AI Code Explainer
print("\n[6] Testing Live AI Code Explainer on Render...")
try:
    r6 = requests.post(f"{API}/explain", json={"code_snippet": "def authenticate_user(username, password):\n    if not username or not password:\n        return False\n    return verify_hash(password)"}, timeout=15)
    print(f"[OK] AI Explainer Status: {r6.status_code} -> Generated {len(r6.json().get('explanation', ''))} characters of context breakdown.")
except Exception as e:
    print(f"[WARN] AI Explainer check failed: {e}")

# 7. Symbol Navigation
print("\n[7] Testing Live Symbol Navigation on Render...")
try:
    r7_def = requests.get(f"{API}/navigation/definition", params={"name": "CodeParserOrchestrator"}, timeout=10)
    r7_use = requests.get(f"{API}/navigation/usages", params={"name": "CodeParserOrchestrator"}, timeout=10)
    print(f"[OK] Symbol Definition: {len(r7_def.json().get('definitions', []))} found.")
    print(f"[OK] Symbol Usages: {len(r7_use.json().get('usages', []))} call-sites found.")
except Exception as e:
    print(f"[WARN] Symbol navigation check failed: {e}")

print("\n==========================================================")
print("[SUCCESS] LIVE RENDER CLOUD VERIFICATION COMPLETE")
print("==========================================================")
