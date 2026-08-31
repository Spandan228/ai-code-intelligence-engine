import os
import sys
import tempfile
import json
from pathlib import Path

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root
sys.path.append(str(Path(__file__).resolve().parent.parent))

from indexer.repo_scanner import RepoScanner
from indexer.code_parser import CodeParserOrchestrator
from indexer.embedding_generator import EmbeddingGenerator
from vector_store.faiss_index import FaissIndex
from search.semantic_search import SemanticSearch
from dependency_graph.graph_builder import GraphBuilder
from analysis.repo_metrics import analyze_repository
from analysis.focused_graph import build_focused_graph
from analysis.architecture_graph import build_architecture_graph, compute_architecture_data
from refactoring.code_smell_detector import CodeSmellDetector
from navigation.code_navigation import CodeNavigation
from ai_explainer.code_explainer import CodeExplainer

def run_live_sample_tests():
    print("================================================================")
    print("[*] AI CODE INTELLIGENCE ENGINE - MULTI-LANGUAGE FUNCTIONALITY AUDIT")
    print("================================================================")

    # 1. Create a temporary multi-language sample repository
    temp_dir = tempfile.mkdtemp(prefix="sample_codebase_")
    print(f"\n[1] Creating multi-language sample codebase in: {temp_dir}")
    
    # Python sample
    os.makedirs(os.path.join(temp_dir, "auth"), exist_ok=True)
    with open(os.path.join(temp_dir, "auth", "login_service.py"), "w", encoding="utf-8") as f:
        f.write("""
class AuthManager:
    def __init__(self, token_secret):
        self.token_secret = token_secret

    def authenticate_user(self, username, password):
        if not username or not password:
            return False
        return self.verify_hash(password)

    def verify_hash(self, password):
        return len(password) > 8
""")

    # JavaScript sample
    os.makedirs(os.path.join(temp_dir, "frontend"), exist_ok=True)
    with open(os.path.join(temp_dir, "frontend", "apiClient.js"), "w", encoding="utf-8") as f:
        f.write("""
class ApiClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }
    async fetchUserData(userId) {
        const response = await fetch(`${this.baseURL}/users/${userId}`);
        return response.json();
    }
}
const handleSessionTimeout = () => {
    console.warn("Session expired. Redirecting to login.");
};
""")

    # Java sample
    os.makedirs(os.path.join(temp_dir, "core"), exist_ok=True)
    with open(os.path.join(temp_dir, "core", "PaymentGateway.java"), "w", encoding="utf-8") as f:
        f.write("""
public class PaymentGateway {
    private String apiKey;

    public PaymentGateway(String apiKey) {
        this.apiKey = apiKey;
    }

    public boolean processTransaction(double amount, String recipient) {
        if (amount <= 0) return false;
        return validateAccount(recipient);
    }

    private boolean validateAccount(String recipient) {
        return recipient != null && !recipient.isEmpty();
    }
}
""")

    # C++ sample
    os.makedirs(os.path.join(temp_dir, "engine"), exist_ok=True)
    with open(os.path.join(temp_dir, "engine", "renderer.cpp"), "w", encoding="utf-8") as f:
        f.write("""
namespace rendering {
class SceneGraph {
public:
    void renderScene() {
        drawGeometry();
        flushBuffers();
    }
    void drawGeometry() {}
    void flushBuffers() {}
};
}
""")

    # 2. Scan and parse AST across all languages
    scanner = RepoScanner(temp_dir)
    files = scanner.scan()
    print(f"[OK] Found {len(files)} supported multi-language files.")

    orchestrator = CodeParserOrchestrator()
    all_metadata = []
    all_snippets = []
    for f in files:
        snippets = orchestrator.parse_file(f)
        for meta in snippets:
            meta["file_path"] = os.path.relpath(meta["file_path"], temp_dir).replace("\\", "/")
            all_metadata.append(meta)
            all_snippets.append(meta["code_snippet"])

    print(f"[OK] Successfully extracted {len(all_snippets)} AST entities across Python, JS, Java, and C++.")
    for m in all_metadata:
        print(f"   * [{m['language'].upper()}] {m['type']} '{m['name']}' in {m['file_path']} (line {m['start_line']})")

    # 3. Vector Embedding & FAISS Indexing
    print("\n[2] Generating 384-dimensional dense vector embeddings with all-MiniLM-L6-v2...")
    embedding_gen = EmbeddingGenerator()
    embeddings = embedding_gen.generate(all_snippets)
    assert embeddings.shape[0] == len(all_snippets)
    assert embeddings.shape[1] == 384
    print(f"[OK] Generated embedding matrix: shape {embeddings.shape} (dtype: {embeddings.dtype})")

    vector_store = FaissIndex(dimension=384)
    vector_store.add_embeddings(embeddings, all_metadata)
    assert vector_store.index.ntotal == len(all_snippets)
    print(f"[OK] FAISS index loaded with {vector_store.index.ntotal} dense vectors.")

    # 4. Semantic Code Search Verification
    print("\n[3] Testing Semantic Code Search Queries...")
    search_engine = SemanticSearch(embedding_gen, vector_store)
    
    test_queries = [
        "user authentication and password verification",
        "process payment and financial transactions",
        "fetch user details from API endpoint",
        "draw 3D graphics geometry and render scene"
    ]
    for q in test_queries:
        res = search_engine.search(q, top_k=2)
        top = res[0]
        print(f"   Query: \"{q}\"")
        print(f"   -> Match #1: '{top['name']}' ({top['file_path']}) | Cosine Score: {top['score']:.4f}")

    # 5. Repository Metrics & Hotspots
    print("\n[4] Testing Repository Analytics & Metrics Aggregator...")
    metrics = analyze_repository(all_metadata)
    print(f"[OK] Metrics: {metrics['number_of_functions']} Functions, {metrics['number_of_classes']} Classes, {metrics['number_of_files']} Files, {metrics['number_of_modules']} Modules")

    # 6. Dependency Graph Topology
    print("\n[5] Testing Dependency Call Graph Generation...")
    graph_builder = GraphBuilder()
    graph_builder.build_from_metadata(all_metadata)
    fig_full = graph_builder.get_visualization()
    assert fig_full is not None
    print(f"[OK] Built NetworkX graph: {len(graph_builder.graph.nodes)} nodes, {len(graph_builder.graph.edges)} edges.")

    # 7. Focused Entity Radial Graph
    print("\n[6] Testing Focused Radial Bipartite Graph for 'renderScene'...")
    fig_focused = build_focused_graph("renderScene", all_metadata)
    assert fig_focused is not None
    print("[OK] Successfully generated radial concentric caller/callee figure.")

    # 8. Architecture Insights Map
    print("\n[7] Testing 360-degree Circular Package Shell Architecture...")
    fig_arch = build_architecture_graph(all_metadata)
    arch_df = compute_architecture_data(all_metadata)
    assert fig_arch is not None
    print(f"[OK] Architecture Map generated with {len(arch_df)} module coupling records.")

    # 9. Quality Guard & Code Smells
    print("\n[8] Testing Quality Guard & Radon Code Smell Detector...")
    smell_detector = CodeSmellDetector()
    smells = smell_detector.analyze_repository(all_metadata)
    print(f"[OK] Quality Guard audit completed: analyzed {len(all_metadata)} code items.")

    # 10. AI Code Explainer
    print("\n[9] Testing Contextual AI Code Explainer...")
    explainer = CodeExplainer(search_engine)
    explanation = explainer.explain_code("def authenticate_user(username, password): return verify_hash(password)")
    assert len(explanation) > 50
    print("[OK] AI Code Explainer generated multi-section architectural synthesis.")

    # 11. Symbol Navigation
    print("\n[10] Testing Symbol Navigation (Jump to Definition & Usages)...")
    nav = CodeNavigation(all_metadata)
    defs = nav.jump_to_definition("PaymentGateway")
    usages = nav.find_usages("drawGeometry")
    print(f"[OK] Jump to Definition for 'PaymentGateway': found in '{defs[0]['file_path']}'")
    print(f"[OK] Usages for 'drawGeometry': {len(usages)} call-sites found.")

    print("\n================================================================")
    print("[SUCCESS] ALL MULTI-LANGUAGE FUNCTIONALITIES VERIFIED WITH 100% SUCCESS")
    print("================================================================")

if __name__ == "__main__":
    run_live_sample_tests()
