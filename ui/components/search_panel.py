import streamlit as st
import requests

def render_search_panel(api_base: str):
    """Renders the semantic search interface."""
    st.subheader("🔍 Semantic Code Search")
    st.write("Find logic, functions, and classes using natural language queries.")
    
    query = st.text_input("What are you looking for?", placeholder="e.g., 'auth login logic' or 'database connector class'")
    top_k = st.slider("Results to show", 1, 10, 5)
    
    if query:
        with st.spinner("Searching semantic index..."):
            try:
                res = requests.post(f"{api_base}/search", json={"query": query, "top_k": top_k})
                results = res.json().get("results", [])
                
                if not results:
                    st.warning("No matches found in the index.")
                
                for r in results:
                    with st.expander(f"📁 {r['file_path']} > 🧩 {r['name']} (Score: {r['score']:.2f})"):
                        st.code(r["code_snippet"], language=r["language"])
            except Exception as e:
                st.error(f"Search failed: {e}")
