import streamlit as st

def render_empty_state(title: str, message: str, action_label: str = "", icon: str = "🔍"):
    """
    Renders a warm, high-craft empty state card matching the Reference Design Specification.
    Floating pure white card over warm alabaster canvas with subtle dashed border.
    """
    html = f"""
    <div style="
        background: #ffffff;
        border: 1px dashed #cbd5e1;
        border-radius: 16px;
        padding: 2.75rem 1.75rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02), 0 8px 24px -4px rgba(0, 0, 0, 0.04);
    ">
        <div style="font-size: 2.5rem; margin-bottom: 0.8rem;">{icon}</div>
        <h3 style="font-size: 1.15rem; font-weight: 700; color: #111827; margin-bottom: 0.4rem; letter-spacing: -0.015em;">{title}</h3>
        <p style="font-size: 0.85rem; color: #64748b; max-width: 460px; margin: 0 auto; line-height: 1.5;">{message}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
