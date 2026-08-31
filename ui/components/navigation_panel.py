import streamlit as st
import requests
from ui.components.empty_state import render_empty_state

def render_navigation_panel(api_base: str):
    """
    Renders the Symbol Explorer and Code Navigation workspace matching the Reference Design Specification.
    - Symbol search card with default hub suggestion
    - Distinct visual zones for Symbol Declaration and Cross-File Usages
    - File breadcrumbs, language tags, and high-contrast syntax blocks
    """
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="font-size: 1.25rem; font-weight: 700; color: #111827; margin: 0; letter-spacing: -0.02em;">🧭 Symbol Explorer & Cross-File Navigation</h2>
        <p style="font-size: 0.84rem; color: #64748b; margin: 0.2rem 0 0 0;">Inspect symbol source declarations and trace cross-file call-site references across the indexed codebase.</p>
    </div>
    """, unsafe_allow_html=True)

    # Search Card
    st.markdown("""
    <div class="bento-card" style="margin-bottom: 1.25rem;">
        <div class="bento-card-header">
            <h3 class="bento-card-title">Inspect Symbol Topology</h3>
            <span class="pill-badge-brand">Declaration & Usages</span>
        </div>
        <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.85rem;">
            Enter a function, method, class, or struct name to locate its source declaration and cross-file references.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 1], gap="medium")
    with col1:
        symbol = st.text_input(
            "Symbol Name",
            value="CodeParserOrchestrator",
            placeholder="e.g. 'CodeParserOrchestrator', 'PythonParser', or 'FaissIndex'",
            label_visibility="collapsed"
        )
    with col2:
        nav_mode = st.selectbox("Navigation View", ["Declaration & Usages", "Declaration Only", "Usages Only"])

    if symbol.strip():
        # 1. Fetch Definition
        defs = []
        usages = []

        if nav_mode in ["Declaration & Usages", "Declaration Only"]:
            try:
                r_def = requests.get(f"{api_base}/navigation/definition", params={"name": symbol.strip()}, timeout=5)
                if r_def.status_code == 200:
                    defs = r_def.json().get("definitions", [])
            except Exception as e:
                st.error(f"Error fetching definition: {e}")

        if nav_mode in ["Declaration & Usages", "Usages Only"]:
            try:
                r_use = requests.get(f"{api_base}/navigation/usages", params={"name": symbol.strip()}, timeout=5)
                if r_use.status_code == 200:
                    usages = r_use.json().get("usages", [])
            except Exception as e:
                st.error(f"Error fetching usages: {e}")

        # Render Declaration Zone
        if nav_mode in ["Declaration & Usages", "Declaration Only"]:
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin: 1.25rem 0 0.75rem 0;">
                <span style="font-size: 0.95rem; font-weight: 700; color: #111827;">📍 Source Declaration ({len(defs)} found)</span>
                <span class="pill-badge-brand">AST Node</span>
            </div>
            """, unsafe_allow_html=True)

            if defs:
                for d in defs:
                    st.markdown(f"""
                    <div class="bento-card" style="margin-bottom: 0.85rem; padding: 1.1rem 1.35rem;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.92rem; font-weight: 700; color: #111827;">{d.get('name')}</span>
                            <div style="display: flex; gap: 0.4rem; align-items: center;">
                                <span class="pill-badge-neutral">{d.get('type', 'entity').upper()}</span>
                                <span class="pill-badge-lang">{d.get('language', 'python').upper()}</span>
                            </div>
                        </div>
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.35rem 0.65rem; margin-bottom: 0.65rem; font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: #64748b;">
                            📁 <b>{d.get('file_path')}</b> : Lines <b>{d.get('start_line', 1)}–{d.get('end_line', 1)}</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(d.get("code_snippet", ""), language=d.get("language", "python"))
            else:
                st.warning(f"No direct declaration found matching symbol '{symbol}'.")

        # Render Usages Zone
        if nav_mode in ["Declaration & Usages", "Usages Only"]:
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin: 1.5rem 0 0.75rem 0;">
                <span style="font-size: 0.95rem; font-weight: 700; color: #111827;">🔗 Cross-File References & Usages ({len(usages)} found)</span>
                <span class="pill-badge-success">Call Sites</span>
            </div>
            """, unsafe_allow_html=True)

            if usages:
                for u in usages:
                    caller_name = u.get('name', 'anonymous')
                    st.markdown(f"""
                    <div class="bento-card" style="margin-bottom: 0.85rem; padding: 1.1rem 1.35rem;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.88rem; font-weight: 600; color: #111827;">Referenced inside: <b style="color: #ea580c;">{caller_name}</b></span>
                            <span class="pill-badge-lang">{u.get('language', 'python').upper()}</span>
                        </div>
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.35rem 0.65rem; margin-bottom: 0.65rem; font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: #64748b;">
                            📁 <b>{u.get('file_path')}</b> : Line <b>{u.get('start_line', 1)}</b>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(u.get("code_snippet", ""), language=u.get("language", "python"))
            else:
                st.info(f"No external usages or call sites found referencing '{symbol}'.")
    else:
        render_empty_state(
            title="Symbol Explorer Ready",
            message="Enter a function, method, class, or struct name above to locate its source declaration and cross-file usages.",
            icon="🔎"
        )
