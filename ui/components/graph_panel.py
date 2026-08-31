import streamlit as st
from ui.components.empty_state import render_empty_state

def render_graph_panel(title: str, fig, description: str = ""):
    """
    Renders a Plotly graph inside a pure white floating Bento card matching the Reference Design Specification.
    """
    if not fig:
        render_empty_state(
            title="Graph Topology Unavailable",
            message="No graph topology data exists for the selected scope. Please index your repository first.",
            icon="🕸️"
        )
        return

    st.markdown(f"""
    <div class="bento-card" style="margin-bottom: 0.75rem; padding: 1.15rem 1.4rem;">
        <div class="bento-card-header" style="margin-bottom: 0.4rem; padding-bottom: 0.4rem;">
            <h3 class="bento-card-title">{title}</h3>
            <span class="pill-badge-brand">Plotly Interactive Visualizer</span>
        </div>
        {f'<p style="font-size: 0.82rem; color: #64748b; margin: 0; line-height: 1.4;">{description}</p>' if description else ''}
    </div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
            "responsive": True,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "code_topology_graph",
                "height": 700,
                "width": 1200,
                "scale": 2
            }
        }
    )
