import streamlit as st
import requests

def render_enterprise_header(api_base: str):
    """
    Renders the floating top brand utility header matching the Reference Design Specification.
    White surface card over warm alabaster canvas with live engine status telemetry.
    """
    is_live = False
    stats = {}
    
    try:
        r = requests.get(f"{api_base}/stats", timeout=3.0)
        if r.status_code == 200:
            is_live = True
            stats = r.json()
    except Exception:
        is_live = False

    status_pill = (
        '<div class="status-capsule-online"><span class="pulse-dot-online"></span>ENGINE ONLINE (FAISS + MiniLM)</div>'
        if is_live else
        '<div class="status-capsule-offline"><span class="pulse-dot-offline"></span>ENGINE OFFLINE</div>'
    )

    header_html = f'''<div class="brand-hero-card"><div class="brand-hero-left"><div class="brand-icon-pod">🧠</div><div><h1 class="brand-title">AI Code Intelligence Engine</h1><p class="brand-subtitle">Multi-Language AST Parsing • FAISS Semantic Search • Topology Graphs • Quality Audit</p></div></div><div>{status_pill}</div></div>'''
    st.markdown(header_html, unsafe_allow_html=True)
    return is_live, stats
