import streamlit as st
import pandas as pd
from ui.components.empty_state import render_empty_state

def render_metrics_panel(metrics):
    """
    Renders the flagship Repository Analytics dashboard using ONLY real backend metrics.
    Follows the Reference Design Specification:
    - 5 Floating Hero KPI Cards with top gradient borders
    - Dual Bento Split: Connectivity Hotspots Progress Bars + Entity Composition Card
    """
    if not metrics or metrics.get("number_of_files", 0) == 0:
        render_empty_state(
            title="No Repository Analytics Available",
            message="Please index a local directory or GitHub repository to compute codebase analytics and hotspots.",
            icon="📊"
        )
        return

    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="font-size: 1.25rem; font-weight: 700; color: #111827; margin: 0; letter-spacing: -0.02em;">📊 Repository Analytics & Architecture Metrics</h2>
        <p style="font-size: 0.84rem; color: #64748b; margin: 0.2rem 0 0 0;">Real-time AST entity density, module boundaries, and in-degree connectivity hotspots.</p>
    </div>
    """, unsafe_allow_html=True)

    funcs = int(metrics.get("number_of_functions", 0))
    classes = int(metrics.get("number_of_classes", 0))
    files = int(metrics.get("number_of_files", 0))
    modules = int(metrics.get("number_of_modules", 0))
    deps = int(metrics.get("total_dependencies", 0))

    # 1. Flagship Hero KPI Row (Pure real data)
    kpi_html = f"""
    <div class="kpi-grid">
        <div class="kpi-pod">
            <div class="kpi-overline">Functions & Methods</div>
            <div class="kpi-value">{funcs}</div>
            <div class="kpi-subtext">Extracted across ASTs</div>
        </div>
        <div class="kpi-pod">
            <div class="kpi-overline">Classes & Structs</div>
            <div class="kpi-value">{classes}</div>
            <div class="kpi-subtext">Object abstractions</div>
        </div>
        <div class="kpi-pod">
            <div class="kpi-overline">Parsed Files</div>
            <div class="kpi-value">{files}</div>
            <div class="kpi-subtext">Source code files</div>
        </div>
        <div class="kpi-pod">
            <div class="kpi-overline">Project Modules</div>
            <div class="kpi-value">{modules}</div>
            <div class="kpi-subtext">Package boundaries</div>
        </div>
        <div class="kpi-pod">
            <div class="kpi-overline">Dependencies</div>
            <div class="kpi-value">{deps}</div>
            <div class="kpi-subtext">Cross-entity calls</div>
        </div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)

    # 2. Dual Bento Grid Split (Hotspots on Left, Composition on Right)
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown("""
        <div class="bento-card" style="margin-bottom: 0;">
            <div class="bento-card-header">
                <h3 class="bento-card-title">🔥 Connectivity Hotspots</h3>
                <span class="pill-badge-brand">Top In-Degree References</span>
            </div>
            <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 1rem; line-height: 1.45;">
                Entities with the highest number of direct references across the codebase. High hotspot counts indicate critical architectural hubs.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        most_connected = metrics.get("most_connected_nodes", [])
        if most_connected:
            conn_df = pd.DataFrame(most_connected, columns=["Entity Symbol", "Reference Count"])
            conn_df["Reference Count"] = conn_df["Reference Count"].astype(int)
            max_ref = int(max(conn_df["Reference Count"].max(), 1))
            st.dataframe(
                conn_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Entity Symbol": st.column_config.TextColumn("Symbol Name", width="medium"),
                    "Reference Count": st.column_config.ProgressColumn(
                        "Dependencies",
                        min_value=0,
                        max_value=max_ref,
                        format="%d"
                    )
                }
            )
        else:
            st.info("Not enough data for hotspot analysis.")

    with col2:
        st.markdown("""
        <div class="bento-card" style="margin-bottom: 0;">
            <div class="bento-card-header">
                <h3 class="bento-card-title">📐 Entity Composition Breakdown</h3>
                <span class="pill-badge-success">Density Ratio</span>
            </div>
            <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 1rem; line-height: 1.45;">
                Relative distribution of functional routines versus class structures across the indexed repository.
            </p>
        </div>
        """, unsafe_allow_html=True)

        total_entities = max(funcs + classes, 1)
        func_pct = f"{(funcs / total_entities) * 100:.1f}%"
        class_pct = f"{(classes / total_entities) * 100:.1f}%"

        dist_data = {
            "Entity Category": ["Functions & Methods", "Classes & Structs", "Cross-Module Calls"],
            "Count": [funcs, classes, deps],
            "Share": [func_pct, class_pct, "—"]
        }
        dist_df = pd.DataFrame(dist_data)
        dist_df["Count"] = dist_df["Count"].astype(int)
        st.dataframe(
            dist_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Entity Category": st.column_config.TextColumn("Category", width="medium"),
                "Count": st.column_config.NumberColumn("Total Count", format="%d"),
                "Share": st.column_config.TextColumn("Entity Ratio", width="small")
            }
        )
