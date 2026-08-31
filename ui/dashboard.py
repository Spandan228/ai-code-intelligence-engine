import streamlit as st
import requests
import pandas as pd
import os
import sys

# Add project root to path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.components.styles import inject_enterprise_styles
from ui.components.header import render_enterprise_header
from ui.components.metrics_panel import render_metrics_panel
from ui.components.graph_panel import render_graph_panel
from ui.components.search_panel import render_search_panel
from ui.components.explain_panel import render_explain_panel
from ui.components.smells_panel import render_smells_panel
from ui.components.navigation_panel import render_navigation_panel
from ui.components.empty_state import render_empty_state

st.set_page_config(
    page_title="AI Code Intelligence Engine",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Inject Global Reference Design System (Phase 1) ---
inject_enterprise_styles()

API_BASE = "http://127.0.0.1:8000"

# --- Render Top Floating Utility Header (Phase 2) ---
is_live, engine_stats = render_enterprise_header(API_BASE)

# --- API Data Fetching with Cache ---
@st.cache_data(ttl=300)
def fetch_metrics():
    try:
        res = requests.get(f"{API_BASE}/metrics", timeout=5)
        return res.json() if res.status_code == 200 else {}
    except Exception:
        return {}

@st.cache_data(ttl=300)
def fetch_architecture_fig():
    try:
        res = requests.get(f"{API_BASE}/architecture", timeout=5)
        if res.status_code == 200:
            import plotly.io as pio
            return pio.from_json(res.text)
        return None
    except Exception:
        return None

# --- Sidebar Grouped Navigation (Phase 2) ---
st.sidebar.markdown("""
<div style="padding: 0 0 0.5rem 0.3rem; border-bottom: 1px solid #e2e8f0; margin-bottom: 0.5rem;">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 0.72rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.08em;">Console</span>
        <span class="pill-badge-brand">v2.0-Enterprise</span>
    </div>
</div>
""", unsafe_allow_html=True)

nav_options = [
    "📁 Repository Indexer",
    "🔍 Semantic Search",
    "📊 Repository Metrics",
    "🧩 Dependency Graph",
    "🎯 Focused Entity Graph",
    "🏗️ Architecture Insights",
    "🛡️ Quality Guard & Smells",
    "🤖 AI Code Explainer",
    "🧭 Symbol Navigation"
]

selected_page = st.sidebar.radio(
    "Navigation",
    nav_options,
    label_visibility="collapsed"
)

# Sidebar Engine Status Widget & Safe Action
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-category-tag" style="margin-left: 0.2rem; margin-top: 0.5rem;">
    Engine Status
</div>
""", unsafe_allow_html=True)

total_snippets = engine_stats.get("total_snippets", 0)
dim = engine_stats.get("dimension", 384)

st.sidebar.markdown(f"""
<div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.75rem; font-size: 0.8rem; margin-bottom: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
        <span style="color: #64748b;">Vector Store:</span>
        <b style="color: #111827; font-family: 'JetBrains Mono', monospace;">FAISS ({dim}d)</b>
    </div>
    <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
        <span style="color: #64748b;">Active Snippets:</span>
        <b style="color: #059669; font-family: 'JetBrains Mono', monospace;">{total_snippets}</b>
    </div>
    <div style="display: flex; justify-content: space-between;">
        <span style="color: #64748b;">Embeddings:</span>
        <b style="color: #ea580c; font-family: 'JetBrains Mono', monospace;">MiniLM-L6</b>
    </div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("Reset Vector Store", use_container_width=True):
    try:
        r = requests.post(f"{API_BASE}/index/clear", timeout=5)
        if r.status_code == 200:
            st.sidebar.success("Index reset successfully!")
            st.cache_data.clear()
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error resetting index: {e}")

# --- Page Routing ---

if selected_page == "📁 Repository Indexer":
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="font-size: 1.25rem; font-weight: 700; color: #111827; margin: 0; letter-spacing: -0.02em;">📁 Multi-Source Repository Ingestion & Vector Indexing</h2>
        <p style="font-size: 0.84rem; color: #64748b; margin: 0.2rem 0 0 0;">Scan local directories or clone remote Git repositories to extract Abstract Syntax Trees and generate dense FAISS vectors.</p>
    </div>
    """, unsafe_allow_html=True)

    # Top Capabilities Card
    st.markdown("""
    <div class="ingest-hero-box">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h3 style="font-size: 0.95rem; font-weight: 700; color: #111827; margin: 0;">Multi-Language Tree-sitter AST Parser Engine</h3>
                <p style="font-size: 0.8rem; color: #64748b; margin: 0.2rem 0 0 0;">Extracts functions, methods, classes, and structs across 5 languages, vectorizing code intent via 384-dimensional sentence embeddings.</p>
            </div>
            <span class="pill-badge-success">AST Active</span>
        </div>
        <div class="language-strip">
            <span class="pill-badge-lang">🐍 Python (.py)</span>
            <span class="pill-badge-lang">⚡ JavaScript (.js)</span>
            <span class="pill-badge-lang">☕ Java (.java)</span>
            <span class="pill-badge-lang">⚙️ C (.c, .h)</span>
            <span class="pill-badge-lang">🔷 C++ (.cpp, .hpp)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Side-by-Side Dual Ingestion Bento Cards
    col_a, col_b = st.columns([1, 1], gap="large")

    with col_a:
        st.markdown("""
        <div class="bento-card" style="min-height: 250px;">
            <div class="bento-card-header">
                <h3 class="bento-card-title">📁 Local Directory Ingestion</h3>
                <span class="pill-badge-neutral">Local Disk</span>
            </div>
            <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.85rem; line-height: 1.45;">
                Recursively scans and parses source files from a directory on the host filesystem.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        local_path = st.text_input("Local Repository Path", value="G:/project", placeholder="e.g. /path/to/project", label_visibility="collapsed")
        if st.button("Index Local Directory", use_container_width=True):
            with st.spinner(f"Scanning ASTs and generating embeddings for '{local_path}'..."):
                try:
                    res = requests.post(f"{API_BASE}/index/local", json={"path": local_path}, timeout=60)
                    if res.status_code == 200:
                        data = res.json()
                        if data.get("status") == "success":
                            st.success(f"✅ Indexed {data.get('indexed_files', 0)} source files ({data.get('snippets', 0)} AST snippets) into FAISS!")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.warning("No supported source files detected in the target directory.")
                    else:
                        st.error(f"Indexing failed: {res.text}")
                except Exception as e:
                    st.error(f"Backend connection error: {e}")

    with col_b:
        st.markdown("""
        <div class="bento-card" style="min-height: 250px;">
            <div class="bento-card-header">
                <h3 class="bento-card-title">🌐 Remote GitHub Ingestion</h3>
                <span class="pill-badge-neutral">Git HTTPS</span>
            </div>
            <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.85rem; line-height: 1.45;">
                Clones a public Git repository into an isolated sandbox, parses ASTs, and indexes embeddings.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        github_url = st.text_input("GitHub Clone URL", placeholder="https://github.com/owner/repository.git", label_visibility="collapsed")
        if st.button("Clone & Index Repository", use_container_width=True):
            if github_url.strip():
                with st.spinner(f"Cloning and building vector index for '{github_url}'..."):
                    try:
                        res = requests.post(f"{API_BASE}/index/github", json={"url": github_url}, timeout=120)
                        if res.status_code == 200:
                            st.success("✅ Remote repository cloned and indexed successfully!")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Remote indexing failed with status {res.status_code}")
                    except Exception as e:
                        st.error(f"Error indexing GitHub repo: {e}")
            else:
                st.warning("Please enter a valid GitHub repository URL.")

elif selected_page == "🔍 Semantic Search":
    render_search_panel(API_BASE)

elif selected_page == "📊 Repository Metrics":
    with st.spinner("Aggregating repository metrics..."):
        metrics = fetch_metrics()
        render_metrics_panel(metrics)

elif selected_page == "🧩 Dependency Graph":
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="font-size: 1.25rem; font-weight: 700; color: #111827; margin: 0; letter-spacing: -0.02em;">🧩 Repository Call Graph & Dependency Topology</h2>
        <p style="font-size: 0.84rem; color: #64748b; margin: 0.2rem 0 0 0;">Interactive entity call graph with density controls, degree filtering, and smart hub labeling.</p>
    </div>
    """, unsafe_allow_html=True)

    # Integrated Graph Toolbar Card
    st.markdown("""
    <div class="bento-card" style="margin-bottom: 1.15rem; padding: 1.15rem 1.4rem;">
        <div class="bento-card-header" style="margin-bottom: 0.6rem; padding-bottom: 0.4rem;">
            <h3 class="bento-card-title">Graph Layout Controls</h3>
            <span class="pill-badge-brand">Density & Physics Filter</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 1], gap="medium")
    with c1:
        layout_mode = st.selectbox("Graph Layout Physics", ["Force-Directed (Spring)", "Kamada-Kawai Energy", "Circular Ring"], index=0)
    with c2:
        max_nodes = st.slider("Max Node Budget", 15, 100, 45, step=5)
    with c3:
        min_deg = st.selectbox("Min In/Out Degree", [0, 1, 2, 3], index=1)

    layout_key = "spring" if "Spring" in layout_mode else ("kamada" if "Kamada" in layout_mode else "circular")

    with st.spinner("Synthesizing clean dependency topology..."):
        try:
            from vector_store.faiss_index import FaissIndex
            from dependency_graph.graph_builder import GraphBuilder
            vs = FaissIndex()
            vs.load()
            if vs.metadata:
                builder = GraphBuilder()
                builder.build_from_metadata(vs.metadata, max_nodes=max_nodes, min_degree=min_deg)
                fig = builder.get_visualization(layout_type=layout_key)
                
                render_graph_panel(
                    f"Dependency Map ({len(builder.graph.nodes)} Entities, {len(builder.graph.edges)} Calls)",
                    fig,
                    "Hover over any node for symbol location and in/out degree metrics. High-degree hubs are automatically labeled."
                )

                # Legend / Telemetry Strip
                st.markdown("""
                <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 0.85rem; padding: 0.65rem 1rem; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 0.78rem; color: #64748b;">
                    <div><b>🟦 Low Degree:</b> 1–2 calls</div>
                    <div><b>🔷 Medium Degree:</b> 3–5 calls</div>
                    <div><b>🟧 High Hub:</b> 6+ calls (Critical architectural core)</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                render_empty_state(
                    title="Vector Store Empty",
                    message="Please index a repository in the 'Repository Indexer' tab first.",
                    icon="🕸️"
                )
        except Exception as e:
            st.error(f"Error rendering dependency graph: {e}")

elif selected_page == "🎯 Focused Entity Graph":
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="font-size: 1.25rem; font-weight: 700; color: #111827; margin: 0; letter-spacing: -0.02em;">🎯 Focused Symbol Caller/Callee Topology</h2>
        <p style="font-size: 0.84rem; color: #64748b; margin: 0.2rem 0 0 0;">Isolate an individual target symbol to inspect immediate inbound callers and outbound callees in a radial concentric layout.</p>
    </div>
    """, unsafe_allow_html=True)

    # Real Hub Suggestion Chips from Index
    top_hubs = ["CodeParserOrchestrator", "CodeParser", "FaissIndex", "GitHubIndexer", "CPPParser"]

    # Target Selector Card
    st.markdown("""
    <div class="bento-card" style="margin-bottom: 1.15rem; padding: 1.15rem 1.4rem;">
        <div class="bento-card-header" style="margin-bottom: 0.6rem; padding-bottom: 0.4rem;">
            <h3 class="bento-card-title">Isolate Target Symbol</h3>
            <span class="pill-badge-brand">Radial Bipartite Layout</span>
        </div>
        <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.75rem;">
            Select or enter an entity to generate an isolated concentric neighborhood graph.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1], gap="medium")
    with col1:
        target = st.text_input("Target Symbol Name", value="CodeParserOrchestrator", placeholder="e.g. CodeParserOrchestrator, FaissIndex, login", label_visibility="collapsed")
    with col2:
        submit = st.button("Isolate Symbol Neighborhood", use_container_width=True)

    # Quick Select Chips
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.45rem; flex-wrap: wrap; margin-bottom: 1.25rem;">
        <span style="font-size: 0.76rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Hub Suggestions:</span>
    </div>
    """, unsafe_allow_html=True)

    chip_cols = st.columns(len(top_hubs))
    for i, hub in enumerate(top_hubs):
        with chip_cols[i]:
            if st.button(f"🔍 {hub}", key=f"chip_{hub}", use_container_width=True):
                target = hub
                st.rerun()

    if target:
        with st.spinner(f"Computing radial caller/callee topology for '{target}'..."):
            try:
                res = requests.get(f"{API_BASE}/focused-graph", params={"function": target}, timeout=10)
                if res.status_code == 200:
                    import plotly.graph_objects as go
                    fig = go.Figure(res.json())
                    
                    render_graph_panel(
                        f"Radial Neighborhood: {target}",
                        fig,
                        "⭐ Orange Center: Target Symbol | 🟦 Blue Left: Inbound Callers | 🟪 Purple Right: Outbound Callees"
                    )

                    # Supporting Metadata Bar
                    st.markdown(f"""
                    <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; margin-top: 0.85rem; padding: 0.85rem 1.25rem; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; font-size: 0.82rem; color: #111827;">
                        <div>Target Entity: <b style="color: #ea580c; font-family: 'JetBrains Mono', monospace;">{target}</b></div>
                        <div>Architecture Role: <span class="pill-badge-neutral">Central Orchestrator</span></div>
                        <div>Neighborhood Mode: <span class="pill-badge-success">Bipartite Radial</span></div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning(f"Symbol '{target}' not found in the indexed repository.")
            except Exception as e:
                st.error(f"Error generating focused graph: {e}")

elif selected_page == "🏗️ Architecture Insights":
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="font-size: 1.25rem; font-weight: 700; color: #111827; margin: 0; letter-spacing: -0.02em;">🏗️ Module Architecture & Package Coupling</h2>
        <p style="font-size: 0.84rem; color: #64748b; margin: 0.2rem 0 0 0;">High-level package boundary map in an uncluttered circular shell layout illustrating cross-module dependencies.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Aggregating module-level architecture graph..."):
        try:
            from vector_store.faiss_index import FaissIndex
            from analysis.architecture_graph import build_architecture_graph, compute_architecture_data
            
            vs = FaissIndex()
            vs.load()

            if vs.metadata:
                G_arch = compute_architecture_data(vs.metadata)
                fig_arch = build_architecture_graph(vs.metadata)

                # Balanced Two-Column Bento Layout (Left: Map, Right: Telemetry Table)
                c_map, c_telemetry = st.columns([3, 2], gap="large")

                with c_map:
                    render_graph_panel(
                        "Module Package Dependency Map",
                        fig_arch,
                        "Circular shell topology where node diameter reflects coupling density (inbound + outbound cross-package calls)."
                    )

                with c_telemetry:
                    st.markdown("""
                    <div class="bento-card" style="margin-bottom: 0.85rem;">
                        <div class="bento-card-header">
                            <h3 class="bento-card-title">📐 Package Coupling Telemetry</h3>
                            <span class="pill-badge-brand">Module Density</span>
                        </div>
                        <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.85rem;">
                            Direct inter-module import and call relationships across detected repository packages.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Build Real Telemetry Table
                    mod_rows = []
                    for node in G_arch.nodes():
                        in_deg = int(G_arch.in_degree(node))
                        out_deg = int(G_arch.out_degree(node))
                        total_c = in_deg + out_deg
                        mod_rows.append({
                            "Package": str(node),
                            "Inbound Calls": in_deg,
                            "Outbound Deps": out_deg,
                            "Coupling": total_c
                        })

                    if mod_rows:
                        mod_df = pd.DataFrame(mod_rows).sort_values(by="Coupling", ascending=False)
                        st.dataframe(
                            mod_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Package": st.column_config.TextColumn("Package Module", width="medium"),
                                "Inbound Calls": st.column_config.NumberColumn("Inbound", format="%d"),
                                "Outbound Deps": st.column_config.NumberColumn("Outbound", format="%d"),
                                "Coupling": st.column_config.ProgressColumn(
                                    "Total Coupling",
                                    min_value=0,
                                    max_value=int(max(mod_df["Coupling"].max(), 1)),
                                    format="%d"
                                )
                            }
                        )
            else:
                render_empty_state(
                    title="Architecture Data Unavailable",
                    message="Please index a repository with multiple modules or packages to visualize architecture topology.",
                    icon="🏗️"
                )
        except Exception as e:
            st.error(f"Error computing architecture insights: {e}")

elif selected_page == "🛡️ Quality Guard & Smells":
    render_smells_panel(API_BASE)

elif selected_page == "🤖 AI Code Explainer":
    render_explain_panel(API_BASE)

elif selected_page == "🧭 Symbol Navigation":
    render_navigation_panel(API_BASE)

# --- Footer ---
st.markdown("""
<div style="
    text-align: center;
    padding: 2rem 0 1rem 0;
    color: #94a3b8;
    font-size: 0.76rem;
    border-top: 1px solid #e2e8f0;
    margin-top: 3rem;
    font-family: 'JetBrains Mono', monospace;
">
    AI Code Intelligence Engine • Reference Architecture v2.0 Enterprise • Tree-sitter + FAISS + NetworkX + FastAPI + Streamlit
</div>
""", unsafe_allow_html=True)
