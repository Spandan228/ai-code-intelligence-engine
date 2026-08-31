import streamlit as st
import requests
from ui.components.empty_state import render_empty_state

def render_search_panel(api_base: str):
    """
    Renders the Semantic Code Search workspace matching the Reference Design Specification.
    - Context-aware search control card
    - Real FAISS cosine similarity scoring and rank badges
    - Clean breadcrumbs, language tags, and high-contrast code snippet blocks
    """
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="font-size: 1.25rem; font-weight: 700; color: #111827; margin: 0; letter-spacing: -0.02em;">🔍 Semantic Code Search Workspace</h2>
        <p style="font-size: 0.84rem; color: #64748b; margin: 0.2rem 0 0 0;">Retrieve logic and implementation intent across AST snippets via 384-dimensional FAISS vector similarity.</p>
    </div>
    """, unsafe_allow_html=True)

    # Search Input Card
    with st.container():
        st.markdown("""
        <div class="bento-card" style="margin-bottom: 1.25rem;">
            <div class="bento-card-header">
                <h3 class="bento-card-title">Search Logic & Implementation</h3>
                <span class="pill-badge-brand">FAISS Vector Search</span>
            </div>
            <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.85rem;">
                Enter a natural language description of the code behavior, algorithm, or component you want to locate.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([4, 1], gap="medium")
        with col1:
            query = st.text_input(
                "Natural Language Code Query",
                value="AST parsing and language detector",
                placeholder="e.g. 'AST parsing and tree-sitter orchestrator' or 'database connection pool logic'",
                label_visibility="collapsed"
            )
        with col2:
            top_k = st.selectbox("Max Results", [3, 5, 10, 15], index=1)

        search_clicked = st.button("Execute Semantic Search", use_container_width=True)

    if query and (search_clicked or True):
        with st.spinner("Querying FAISS vector store and ranking AST candidates..."):
            try:
                res = requests.post(f"{api_base}/search", json={"query": query, "top_k": top_k}, timeout=10)
                if res.status_code == 200:
                    results = res.json().get("results", [])
                    
                    if not results:
                        render_empty_state(
                            title="No Matching Code Snippets Found",
                            message=f"No AST snippets matched the query '{query}'. Try broader terms or ensure your repository is indexed.",
                            icon="🔎"
                        )
                        return

                    # Result Summary Bar
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; margin: 1.25rem 0 0.85rem 0; padding: 0 0.2rem;">
                        <span style="font-size: 0.88rem; font-weight: 700; color: #111827;">Ranked Results ({len(results)} matches)</span>
                        <span class="pill-badge-neutral">IndexFlatIP • Cosine Metric</span>
                    </div>
                    """, unsafe_allow_html=True)

                    for idx, r in enumerate(results):
                        score_val = f"{r['score']:.3f}" if r.get('score') is not None else "N/A"
                        symbol_name = r.get('name', 'anonymous')
                        file_path = r.get('file_path', 'unknown')
                        start_line = r.get('start_line', 1)
                        lang = r.get('language', 'python').upper()
                        snip_type = r.get('type', 'code').upper()

                        st.markdown(f"""
                        <div class="bento-card" style="margin-bottom: 1rem; padding: 1.15rem 1.35rem;">
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem; flex-wrap: wrap; gap: 0.5rem;">
                                <div style="display: flex; align-items: center; gap: 0.5rem;">
                                    <span class="pill-badge-neutral">#{idx + 1}</span>
                                    <span class="pill-badge-brand">{snip_type}</span>
                                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.92rem; font-weight: 700; color: #111827;">{symbol_name}</span>
                                </div>
                                <div style="display: flex; align-items: center; gap: 0.45rem;">
                                    <span class="pill-badge-success">Similarity: {score_val}</span>
                                    <span class="pill-badge-lang">{lang}</span>
                                </div>
                            </div>
                            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.4rem 0.75rem; margin-bottom: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: #64748b;">
                                📁 <b>{file_path}</b> : Line <b>{start_line}</b>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.code(r.get("code_snippet", ""), language=r.get("language", "python"))
                else:
                    st.error(f"Search endpoint returned status {res.status_code}")
            except Exception as e:
                st.error(f"Failed to execute semantic search: {e}")
    else:
        render_empty_state(
            title="Semantic Search Ready",
            message="Enter natural language terms above to explore functions, classes, and logic across the indexed codebase.",
            icon="💡"
        )
