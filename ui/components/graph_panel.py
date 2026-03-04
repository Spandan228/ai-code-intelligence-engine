import streamlit as st

def render_graph_panel(title: str, fig, description: str = ""):
    """Renders a Plotly graph inside a styled container."""
    with st.container():
        st.subheader(title)
        if description:
            st.caption(description)
        
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No graph data available to visualize.")
