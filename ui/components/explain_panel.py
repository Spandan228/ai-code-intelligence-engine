import streamlit as st
import requests
from ui.components.empty_state import render_empty_state

def render_explain_panel(api_base: str):
    """
    Renders the AI Code Explainer and Context Synthesis workspace matching the Reference Design Specification.
    - Code input analysis container
    - Real semantic neighborhood retrieval
    - Structured, multi-section explanation cards
    """
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="font-size: 1.25rem; font-weight: 700; color: #111827; margin: 0; letter-spacing: -0.02em;">🤖 AI Code Explainer & Architectural Synthesis</h2>
        <p style="font-size: 0.84rem; color: #64748b; margin: 0.2rem 0 0 0;">Automated semantic neighborhood analysis, architectural role classification, and contextual intent breakdown.</p>
    </div>
    """, unsafe_allow_html=True)

    default_snippet = """def authenticate_user(username: str, password_hash: str) -> bool:
    \"\"\"Validates user credentials against encrypted store.\"\"\"
    if not username or not password_hash:
        return False
    user = query_user_by_name(username)
    return verify_hash(password_hash, user.hash)"""

    # Analysis Input Card
    st.markdown("""
    <div class="bento-card" style="margin-bottom: 1rem;">
        <div class="bento-card-header">
            <h3 class="bento-card-title">Code Analysis Input</h3>
            <span class="pill-badge-brand">Context Retrieval</span>
        </div>
        <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.75rem;">
            Paste a function, class, or code block to retrieve neighboring context and synthesize an architectural explanation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    snippet = st.text_area(
        "Source Code Block",
        value=default_snippet,
        height=160,
        placeholder="Paste function, class, or code block here...",
        label_visibility="collapsed"
    )

    if st.button("Generate Contextual Explanation", use_container_width=True):
        if snippet.strip():
            with st.spinner("Analyzing semantic neighborhood & synthesizing architectural context..."):
                try:
                    res = requests.post(f"{api_base}/explain", json={"code_snippet": snippet}, timeout=10)
                    if res.status_code == 200:
                        explanation = res.json().get("explanation", "Could not generate explanation.")
                        
                        st.markdown("""
                        <div style="display: flex; align-items: center; justify-content: space-between; margin: 1.5rem 0 0.85rem 0;">
                            <span style="font-size: 0.95rem; font-weight: 700; color: #111827;">Architectural Synthesis Result</span>
                            <span class="pill-badge-success">🟢 Context Synthesized</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                        <div class="bento-card" style="border-left: 4px solid #f97316; margin-bottom: 1rem;">
                            <div style="font-size: 0.88rem; line-height: 1.6; color: #334155;">
                                {explanation}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"API returned status {res.status_code}")
                except Exception as e:
                    st.error(f"Failed to generate explanation: {e}")
        else:
            st.warning("Please enter a code snippet to analyze.")
