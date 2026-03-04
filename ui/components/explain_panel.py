import streamlit as st
import requests

def render_explain_panel(api_base: str):
    """Renders the AI code explanation interface."""
    st.subheader("🤖 AI Code Explanation")
    st.write("Paste a code snippet to receive a semantic explanation of its purpose and context.")
    
    snippet = st.text_area("Source Code", height=300, placeholder="def example_function(): ...")
    
    if st.button("🚀 Explain Code", use_container_width=True):
        if snippet:
            with st.spinner("Analyzing code semantic context..."):
                try:
                    res = requests.post(f"{api_base}/explain", json={"code_snippet": snippet})
                    explanation = res.json().get("explanation", "Could not generate explanation.")
                    
                    st.markdown("---")
                    with st.container():
                        st.markdown(explanation)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
        else:
            st.warning("Please paste a code snippet first.")
