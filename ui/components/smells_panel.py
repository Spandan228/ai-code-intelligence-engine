import streamlit as st
import requests
import pandas as pd
from ui.components.empty_state import render_empty_state

def render_smells_panel(api_base: str):
    """
    Renders the Quality Guard & Code Smells refactoring workspace matching the Reference Design Specification.
    - Top Quality Health KPI row (Total Smells, High Complexity, Large Blocks, Files Affected)
    - Severity Distribution summary
    - Prioritized Refactoring Candidates Table with severity pills
    - Direct Contextual AI Explainer integration
    - Polished pristine health empty state
    """
    st.markdown("""
    <div style="margin-bottom: 1.25rem;">
        <h2 style="font-size: 1.25rem; font-weight: 700; color: #111827; margin: 0; letter-spacing: -0.02em;">🛡️ Quality Guard & Static Anti-Pattern Audit</h2>
        <p style="font-size: 0.84rem; color: #64748b; margin: 0.2rem 0 0 0;">Static AST complexity analysis and maintainability smell detection across indexed source routines.</p>
    </div>
    """, unsafe_allow_html=True)

    # Audit Control Card
    st.markdown("""
    <div class="bento-card" style="margin-bottom: 1.25rem; padding: 1.15rem 1.4rem;">
        <div class="bento-card-header" style="margin-bottom: 0.6rem; padding-bottom: 0.4rem;">
            <h3 class="bento-card-title">Automated Code Health Inspection</h3>
            <span class="pill-badge-brand">Radon AST + Line Metrics</span>
        </div>
        <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.85rem;">
            Scans all indexed routines for cyclomatic complexity hotspots (CC > 10) and oversized functions (> 50 lines).
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        run_audit = st.button("Run Full Quality Audit", use_container_width=True)

    if run_audit or st.session_state.get("quality_audit_completed", False):
        st.session_state["quality_audit_completed"] = True
        with st.spinner("Analyzing cyclomatic complexity and routine length distributions..."):
            try:
                res = requests.get(f"{api_base}/refactoring/smells", timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    smells = data.get("smells", [])
                    
                    if not smells:
                        st.markdown("""
                        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 2.5rem; text-align: center; box-shadow: 0 8px 24px -4px rgba(0,0,0,0.04);">
                            <div style="font-size: 2.5rem; margin-bottom: 0.6rem;">💎</div>
                            <h3 style="color: #059669; font-weight: 700; font-size: 1.15rem; margin: 0;">Codebase Quality is Pristine</h3>
                            <p style="color: #64748b; font-size: 0.84rem; margin-top: 0.4rem; max-width: 480px; margin-left: auto; margin-right: auto;">
                                No routines with excessive cyclomatic complexity (CC > 10) or oversized code blocks (> 50 lines) were detected.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        return

                    # 1. Quality Health KPI Overview (Top Bento Row)
                    total_smells = len(smells)
                    high_cc = sum(1 for s in smells if s.get("type") == "High Complexity")
                    large_funcs = sum(1 for s in smells if "Large" in s.get("type", ""))
                    affected_files = len(set(s.get("file", "") for s in smells))

                    st.markdown(f"""
                    <div class="kpi-grid" style="margin-top: 1rem; margin-bottom: 1.25rem;">
                        <div class="kpi-pod">
                            <div class="kpi-overline">Total Code Smells</div>
                            <div class="kpi-value" style="color: #ea580c;">{total_smells}</div>
                            <div class="kpi-subtext">Flagged anti-patterns</div>
                        </div>
                        <div class="kpi-pod">
                            <div class="kpi-overline">High Complexity</div>
                            <div class="kpi-value" style="color: #f59e0b;">{high_cc}</div>
                            <div class="kpi-subtext">Routines with CC &gt; 10</div>
                        </div>
                        <div class="kpi-pod">
                            <div class="kpi-overline">Oversized Routines</div>
                            <div class="kpi-value" style="color: #6366f1;">{large_funcs}</div>
                            <div class="kpi-subtext">Blocks &gt; 50 lines</div>
                        </div>
                        <div class="kpi-pod">
                            <div class="kpi-overline">Files Affected</div>
                            <div class="kpi-value" style="color: #111827;">{affected_files}</div>
                            <div class="kpi-subtext">Refactoring scope</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # 2. Severity Classification & Distribution Split
                    def get_severity(val, smell_type):
                        if "Complexity" in smell_type:
                            if val >= 25: return "CRITICAL"
                            elif val >= 15: return "HIGH"
                            else: return "MEDIUM"
                        else:
                            if val >= 100: return "CRITICAL"
                            elif val >= 65: return "HIGH"
                            else: return "MEDIUM"

                    for s in smells:
                        s["severity"] = get_severity(s.get("value", 0), s.get("type", ""))

                    crit_count = sum(1 for s in smells if s["severity"] == "CRITICAL")
                    high_count = sum(1 for s in smells if s["severity"] == "HIGH")
                    med_count = sum(1 for s in smells if s["severity"] == "MEDIUM")

                    col_dist, col_info = st.columns([3, 2], gap="large")
                    with col_dist:
                        st.markdown(f"""
                        <div class="bento-card" style="margin-bottom: 1.25rem;">
                            <div class="bento-card-header">
                                <h3 class="bento-card-title">📊 Severity Distribution</h3>
                                <span class="pill-badge-brand">Static Risk Matrix</span>
                            </div>
                            <div style="display: flex; gap: 0.85rem; flex-wrap: wrap; margin-top: 0.5rem;">
                                <div style="flex: 1; min-width: 100px; background: #fef2f2; border: 1px solid rgba(239,68,68,0.2); border-radius: 10px; padding: 0.75rem; text-align: center;">
                                    <div style="font-size: 0.7rem; font-weight: 700; color: #ef4444; text-transform: uppercase;">Critical</div>
                                    <div style="font-size: 1.3rem; font-weight: 800; color: #b91c1c; font-family: 'JetBrains Mono', monospace;">{crit_count}</div>
                                </div>
                                <div style="flex: 1; min-width: 100px; background: #fffbeb; border: 1px solid rgba(245,158,11,0.2); border-radius: 10px; padding: 0.75rem; text-align: center;">
                                    <div style="font-size: 0.7rem; font-weight: 700; color: #f59e0b; text-transform: uppercase;">High</div>
                                    <div style="font-size: 1.3rem; font-weight: 800; color: #b45309; font-family: 'JetBrains Mono', monospace;">{high_count}</div>
                                </div>
                                <div style="flex: 1; min-width: 100px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 0.75rem; text-align: center;">
                                    <div style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase;">Medium</div>
                                    <div style="font-size: 1.3rem; font-weight: 800; color: #334155; font-family: 'JetBrains Mono', monospace;">{med_count}</div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with col_info:
                        st.markdown("""
                        <div class="bento-card" style="margin-bottom: 1.25rem;">
                            <div class="bento-card-header">
                                <h3 class="bento-card-title">💡 Remediation Protocol</h3>
                                <span class="pill-badge-success">Actionable</span>
                            </div>
                            <p style="font-size: 0.82rem; color: #64748b; line-height: 1.45; margin: 0;">
                                Priority is assigned by cyclomatic complexity and block line counts. High-complexity routines should be broken into smaller sub-methods with single responsibilities.
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                    # 3. Prioritized Refactoring Candidates Table
                    st.markdown("""
                    <div style="display: flex; align-items: center; justify-content: space-between; margin: 1.25rem 0 0.75rem 0;">
                        <span style="font-size: 0.95rem; font-weight: 700; color: #111827;">Prioritized Refactoring Candidates</span>
                        <span class="pill-badge-neutral">Sorted by Severity & Score</span>
                    </div>
                    """, unsafe_allow_html=True)

                    # Sort smells: Critical first, then High, then Medium, then by value descending
                    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
                    sorted_smells = sorted(smells, key=lambda s: (severity_order.get(s["severity"], 3), -s.get("value", 0)))

                    table_rows = []
                    for s in sorted_smells:
                        metric_label = f"CC: {s['value']}" if s.get("type") == "High Complexity" else f"{s['value']} lines"
                        table_rows.append({
                            "Severity": s["severity"],
                            "Symbol / Entity": s.get("name", "anonymous"),
                            "Smell Category": s.get("type", "Smell"),
                            "Metric Score": metric_label,
                            "File Path": s.get("file", ""),
                            "Recommended Action": s.get("suggestion", "")
                        })

                    smell_df = pd.DataFrame(table_rows)
                    st.dataframe(
                        smell_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Severity": st.column_config.TextColumn("Severity Tier", width="small"),
                            "Symbol / Entity": st.column_config.TextColumn("Symbol Name", width="medium"),
                            "Smell Category": st.column_config.TextColumn("Category", width="small"),
                            "Metric Score": st.column_config.TextColumn("Metric", width="small"),
                            "File Path": st.column_config.TextColumn("Source File", width="medium"),
                            "Recommended Action": st.column_config.TextColumn("Remediation Guidance", width="large")
                        }
                    )

                    # 4. Contextual AI Explainer Integration
                    st.markdown("""
                    <div class="bento-card" style="margin-top: 1.5rem; padding: 1.15rem 1.4rem;">
                        <div class="bento-card-header">
                            <h3 class="bento-card-title">🤖 Inspect Candidate in AI Code Explainer</h3>
                            <span class="pill-badge-brand">1-Click Context Retrieval</span>
                        </div>
                        <p style="font-size: 0.82rem; color: #64748b; margin-bottom: 0.85rem;">
                            Select any flagged symbol above to examine its architectural role, neighborhood call-sites, and refactoring options in the AI Explainer.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    flagged_names = [s.get("name", "") for s in sorted_smells if s.get("name")]
                    if flagged_names:
                        c_sel, c_go = st.columns([3, 1], gap="medium")
                        with c_sel:
                            selected_symbol = st.selectbox("Select Flagged Symbol", flagged_names, label_visibility="collapsed")
                        with c_go:
                            if st.button("Inspect in Explainer", use_container_width=True):
                                st.info(f"Navigate to '🤖 AI Code Explainer' in the sidebar to analyze '{selected_symbol}'.")
                else:
                    st.error(f"Quality audit failed with status {res.status_code}")
            except Exception as e:
                st.error(f"Error executing quality audit: {e}")
    else:
        render_empty_state(
            title="Quality Audit Ready",
            message="Click 'Run Full Quality Audit' above to scan all indexed snippets for cyclomatic complexity and maintainability anti-patterns.",
            icon="🛡️"
        )
