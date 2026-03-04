import streamlit as st
import pandas as pd

def render_metrics_panel(metrics):
    """Renders the repository metrics in a professional card layout."""
    if not metrics:
        st.warning("No metrics available. Please index a repository first.")
        return

    st.subheader("📊 Repository Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Functions", metrics.get("number_of_functions", 0))
    with col2:
        st.metric("Classes", metrics.get("number_of_classes", 0))
    with col3:
        st.metric("Files", metrics.get("number_of_files", 0))
    with col4:
        st.metric("Modules", metrics.get("number_of_modules", 0))
    with col5:
        st.metric("Dependencies", metrics.get("total_dependencies", 0))

    st.markdown("---")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("🔗 Connectivity Analysis")
        st.write(f"This repository contains approximately **{metrics.get('total_dependencies', 0)}** internal references between entities.")
        
    with col_b:
        st.subheader("🔥 Hotspots (Most Connected)")
        most_connected = metrics.get("most_connected_nodes", [])
        if most_connected:
            conn_df = pd.DataFrame(most_connected, columns=["Entity", "Connections"])
            st.bar_chart(conn_df.set_index("Entity"))
        else:
            st.info("Not enough data for hotspot analysis.")
