import streamlit as st
import requests
import pandas as pd
import os
import sys

# Add project root to path for local imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.components.metrics_panel import render_metrics_panel
from ui.components.graph_panel import render_graph_panel
from ui.components.search_panel import render_search_panel
from ui.components.explain_panel import render_explain_panel

st.set_page_config(
    page_title="AI Code Intelligence Engine",
    page_icon="🧠",
    layout="wide"
)

# --- Styling ---
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #888;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #eee;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("<h1 style='text-align: center;'>🧠 AI Code Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 1.2rem;'>AI-powered developer intelligence platform for exploring codebases.</p>", unsafe_allow_html=True)
st.markdown("---")

API_BASE = "http://localhost:8000"

# --- API Data Fetching with Caching ---
@st.cache_data(ttl=600)
def get_metrics():
    try:
        res = requests.get(f"{API_BASE}/metrics")
        return res.json()
    except: return {}

@st.cache_data(ttl=600)
def get_architecture_fig():
    try:
        res = requests.get(f"{API_BASE}/architecture")
        import plotly.io as pio
        return pio.from_json(res.text)
    except: return None

# --- Sidebar Navigation ---
st.sidebar.header("🧭 Navigation")
selected_page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "🔍 Semantic Search", "🧩 Dependency Graph", "🎯 Focused Graph", "🏗️ Architecture Insights", "📈 Repository Metrics", "🤖 AI Code Explanation"]
)

# --- Page Routing ---
if selected_page == "🏠 Home":
    st.header("📂 Repository Indexing")
    st.info("Start by indexing a local directory or a GitHub repository to enable intelligence features.")
    
    tab1, tab2 = st.tabs(["Local Directory", "GitHub Repository"])
    
    with tab1:
        local_path = st.text_input("Local repository path:", placeholder="/path/to/repo")
        if st.button("Index Local Repo", use_container_width=True):
            with st.spinner("Analyzing and indexing local repository..."):
                try:
                    res = requests.post(f"{API_BASE}/index/local", json={"path": local_path})
                    data = res.json()
                    if data.get("status") == "success":
                        st.success(f"Successfully indexed {data.get('snippets', 0)} snippets!")
                        st.cache_data.clear()
                    else:
                        st.warning("No code snippets found to index.")
                except Exception as e:
                    st.error(f"Error during indexing: {e}")
                    
    with tab2:
        github_url = st.text_input("GitHub URL:", placeholder="https://github.com/user/repo")
        if st.button("Index GitHub Repo", use_container_width=True):
            with st.spinner("Cloning and building semantic index..."):
                try:
                    res = requests.post(f"{API_BASE}/index/github", json={"url": github_url})
                    st.success("GitHub Repository indexed successfully!")
                    st.cache_data.clear()
                except Exception as e:
                    st.error(f"Error during remote indexing: {e}")

elif selected_page == "🔍 Semantic Search":
    render_search_panel(API_BASE)

elif selected_page == "🧩 Dependency Graph":
    st.header("🕸️ Repository Dependency Graph")
    if st.button("Generate Visualization", use_container_width=True):
        with st.spinner("Tracing dependencies..."):
            try:
                # Backend currently returns node/edge counts, for demo we load local data
                from vector_store.faiss_index import FaissIndex
                from dependency_graph.graph_builder import GraphBuilder
                vs = FaissIndex()
                vs.load()
                if vs.metadata:
                    builder = GraphBuilder()
                    builder.build_from_metadata(vs.metadata)
                    fig = builder.get_visualization()
                    render_graph_panel("Full Dependency Map", fig, "Interactive visualization of all code entities and their connections.")
                else:
                    st.warning("Index is empty. Please index a repository first.")
            except Exception as e:
                st.error(f"Failed to build graph: {e}")

elif selected_page == "🎯 Focused Graph":
    st.header("🎯 Focused Entity Graph")
    target = st.text_input("Enter function or class name:", placeholder="e.g. login_user")
    if st.button("Analyze Connections", use_container_width=True):
        if target:
            with st.spinner(f"Filtering graph for '{target}'..."):
                try:
                    res = requests.get(f"{API_BASE}/focused-graph", params={"function": target})
                    if res.status_code == 200:
                        fig_data = res.json()
                        import plotly.graph_objects as go
                        fig = go.Figure(fig_data)
                        render_graph_panel(f"Connections for '{target}'", fig)
                    else:
                        st.error("Entity not found in the current index.")
                except Exception as e:
                    st.error(f"Error: {e}")

elif selected_page == "🏗️ Architecture Insights":
    st.header("🏗️ Architecture Overview")
    if st.button("Show Architecture Graph", use_container_width=True):
        with st.spinner("Aggregating module dependencies..."):
            fig = get_architecture_fig()
            if fig:
                render_graph_panel("Module-Level Architecture", fig, "High-level overview showing dependencies between project modules.")
            else:
                st.error("Architecture data unavailable.")
    
    st.markdown("---")
    st.subheader("🚩 Code Smells & Refactoring")
    if st.button("Analyze Code Quality", use_container_width=True):
        with st.spinner("Detecting code smells..."):
            try:
                from vector_store.faiss_index import FaissIndex
                from refactoring.code_smell_detector import CodeSmellDetector
                vs = FaissIndex()
                vs.load()
                if vs.metadata:
                    detector = CodeSmellDetector()
                    smells = detector.analyze_repository(vs.metadata)
                    if smells:
                        st.table(pd.DataFrame(smells))
                    else:
                        st.success("Codebase looks healthy! No major smells detected. 💎")
            except Exception as e:
                st.error(f"Analysis failed: {e}")

elif selected_page == "📈 Repository Metrics":
    with st.spinner("Calculating metrics..."):
        metrics = get_metrics()
        render_metrics_panel(metrics)

elif selected_page == "🤖 AI Code Explanation":
    render_explain_panel(API_BASE)

# --- Footer ---
st.markdown("<div class='footer'>Built with Python, FastAPI, FAISS, Tree-sitter, and Streamlit.</div>", unsafe_allow_html=True)
