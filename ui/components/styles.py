import streamlit as st

def inject_enterprise_styles():
    """
    Injects the complete Reference Design System stylesheet into Streamlit.
    Architecture: Warm Alabaster Canvas (#f1f3f7), Pure White Floating Bento Cards (#ffffff),
    Plus Jakarta Sans + JetBrains Mono typography, Organic Radii, Ambient Elevation,
    Sunset Tangerine (#f97316) Brand & Mint Emerald (#10b981) Status tokens.
    Includes Phase 8 state consistency, Phase 9 motion foundation, and Phase 10 responsive breakpoints.
    """
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root {
        /* Canvas & Surface Layers */
        --canvas-bg:           #f1f3f7;
        --card-surface:        #ffffff;
        --sidebar-bg:          #f8fafc;
        --surface-hover:       #f8fafc;
        --surface-subtle:      #f1f5f9;

        /* Typography Colors */
        --text-primary:        #111827;
        --text-secondary:      #475569;
        --text-muted:          #64748b;
        --text-dim:            #94a3b8;

        /* Brand & Semantic Palette */
        --brand-primary:       #f97316;
        --brand-primary-hover: #ea580c;
        --brand-tint:          #fff7ed;
        --brand-border:        rgba(249, 115, 22, 0.35);

        --status-success:      #10b981;
        --status-success-tint: #ecfdf5;
        --status-success-dark: #059669;

        --status-warning:      #f59e0b;
        --status-warning-tint: #fffbeb;

        --status-error:        #ef4444;
        --status-error-tint:   #fef2f2;

        --border-hairline:     rgba(0, 0, 0, 0.05);
        --border-subtle:       #e2e8f0;
        --border-default:      #cbd5e1;

        /* Ambient Diffused Shadows */
        --shadow-ambient:      0px 1px 3px rgba(0, 0, 0, 0.02), 0px 8px 24px -4px rgba(0, 0, 0, 0.05);
        --shadow-elevated:     0px 4px 6px -1px rgba(0, 0, 0, 0.03), 0px 14px 30px -4px rgba(0, 0, 0, 0.08);
        --shadow-focus:        0 0 0 3px rgba(249, 115, 22, 0.22);

        /* Radii Scale */
        --radius-sm:           6px;
        --radius-md:           10px;
        --radius-lg:           16px;
        --radius-xl:           20px;
        --radius-pill:         9999px;

        /* Motion Tokens (Phase 9) */
        --ease-fluid:          cubic-bezier(0.16, 1, 0.3, 1);
        --duration-fast:       180ms;
        --duration-medium:     350ms;
    }

    /* Global Reset & Canvas Foundation */
    header[data-testid="stHeader"], #MainMenu, footer {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: var(--canvas-bg) !important;
        color: var(--text-primary) !important;
    }

    .main .block-container {
        padding-top: 1.25rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1440px !important;
        animation: pageEntrance 400ms var(--ease-fluid) forwards;
    }

    @keyframes pageEntrance {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: var(--canvas-bg);
    }
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: var(--radius-sm);
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }

    /* Sidebar Foundation */
    section[data-testid="stSidebar"] {
        background-color: var(--sidebar-bg) !important;
        border-right: 1px solid var(--border-subtle) !important;
        box-shadow: 2px 0 16px rgba(0, 0, 0, 0.02) !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.25rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Sidebar Section Categorization */
    .sidebar-category-tag {
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: var(--text-muted);
        margin: 1.1rem 0 0.35rem 0.5rem;
    }

    /* Sidebar Navigation Items */
    div[data-testid="stRadio"] [role="radiogroup"] {
        gap: 3px !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label {
        background: transparent !important;
        border: 1px solid transparent !important;
        border-radius: var(--radius-md) !important;
        padding: 0.5rem 0.8rem !important;
        margin: 0 !important;
        transition: all var(--duration-fast) var(--ease-fluid) !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] [role="radiogroup"] label:hover {
        background: rgba(241, 245, 249, 0.9) !important;
        transform: translateX(2px) !important;
    }
    /* Eliminate radio circles */
    div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child,
    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
        visibility: hidden !important;
        width: 0px !important;
        height: 0px !important;
    }
    div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
        font-size: 0.86rem !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
        transition: color var(--duration-fast) ease !important;
        margin: 0 !important;
    }
    /* Active Navigation State */
    div[data-testid="stRadio"] label:has(input[type="radio"]:checked) {
        background: var(--brand-tint) !important;
        border: 1px solid rgba(249, 115, 22, 0.25) !important;
        border-left: 3.5px solid var(--brand-primary) !important;
        box-shadow: 0 2px 6px rgba(249, 115, 22, 0.08) !important;
    }
    div[data-testid="stRadio"] label:has(input[type="radio"]:checked) div[data-testid="stMarkdownContainer"] p {
        color: var(--brand-primary-hover) !important;
        font-weight: 600 !important;
    }

    /* Top Floating Utility Header */
    .brand-hero-card {
        background: var(--card-surface);
        border: 1px solid var(--border-hairline);
        border-radius: var(--radius-lg);
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: var(--shadow-ambient);
        transition: box-shadow var(--duration-fast) var(--ease-fluid);
    }
    .brand-hero-card:hover {
        box-shadow: var(--shadow-elevated);
    }
    .brand-hero-left {
        display: flex;
        align-items: center;
        gap: 0.9rem;
    }
    .brand-icon-pod {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        border-radius: var(--radius-md);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        color: white;
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.28);
    }
    .brand-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.025em;
        margin: 0;
        line-height: 1.2;
    }
    .brand-subtitle {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin: 0.15rem 0 0 0;
    }
    .status-capsule-online {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.75rem;
        background: var(--status-success-tint);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-radius: var(--radius-pill);
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--status-success-dark);
        font-family: 'JetBrains Mono', monospace;
    }
    .status-capsule-offline {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.75rem;
        background: var(--status-error-tint);
        border: 1px solid rgba(239, 68, 68, 0.25);
        border-radius: var(--radius-pill);
        font-size: 0.72rem;
        font-weight: 600;
        color: var(--status-error);
        font-family: 'JetBrains Mono', monospace;
    }
    .pulse-dot-online {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--status-success);
        box-shadow: 0 0 8px rgba(16, 185, 129, 0.6);
        animation: radarPulse 2s infinite ease-in-out;
    }
    .pulse-dot-offline {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--status-error);
    }
    @keyframes radarPulse {
        0%, 100% { opacity: 0.7; transform: scale(0.9); }
        50% { opacity: 1; transform: scale(1.15); box-shadow: 0 0 12px rgba(16, 185, 129, 0.8); }
    }

    /* Bento Grid Card Primitives */
    .bento-card {
        background: var(--card-surface);
        border: 1px solid var(--border-hairline);
        border-radius: var(--radius-lg);
        padding: 1.35rem 1.5rem;
        box-shadow: var(--shadow-ambient);
        transition: transform var(--duration-fast) var(--ease-fluid), box-shadow var(--duration-fast) var(--ease-fluid);
    }
    .bento-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-elevated);
    }
    .bento-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.85rem;
        padding-bottom: 0.65rem;
        border-bottom: 1px solid var(--surface-subtle);
    }
    .bento-card-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.015em;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Context Constrained Ingestion Container */
    .ingest-hero-box {
        background: var(--card-surface);
        border: 1px solid var(--border-hairline);
        border-radius: var(--radius-lg);
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: var(--shadow-ambient);
    }
    .language-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.75rem;
    }

    /* KPI Hero Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .kpi-pod {
        background: var(--card-surface);
        border: 1px solid var(--border-hairline);
        border-radius: var(--radius-lg);
        padding: 1.15rem 1.25rem;
        box-shadow: var(--shadow-ambient);
        position: relative;
        overflow: hidden;
        transition: transform var(--duration-fast) var(--ease-fluid), box-shadow var(--duration-fast) var(--ease-fluid);
    }
    .kpi-pod:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-elevated);
    }
    .kpi-pod::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #f97316, #f59e0b);
    }
    .kpi-overline {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: var(--text-muted);
        margin-bottom: 0.35rem;
    }
    .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: var(--text-primary);
        font-family: 'Plus Jakarta Sans', sans-serif;
        letter-spacing: -0.035em;
        line-height: 1;
    }
    .kpi-subtext {
        font-size: 0.74rem;
        color: var(--text-dim);
        margin-top: 0.4rem;
    }

    /* Badges & Pills */
    .pill-badge-brand {
        background: var(--brand-tint);
        color: var(--brand-primary-hover);
        border: 1px solid rgba(249, 115, 22, 0.2);
        padding: 0.2rem 0.55rem;
        border-radius: var(--radius-pill);
        font-size: 0.72rem;
        font-weight: 600;
    }
    .pill-badge-success {
        background: var(--status-success-tint);
        color: var(--status-success-dark);
        border: 1px solid rgba(16, 185, 129, 0.2);
        padding: 0.2rem 0.55rem;
        border-radius: var(--radius-pill);
        font-size: 0.72rem;
        font-weight: 600;
    }
    .pill-badge-lang {
        background: var(--surface-subtle);
        color: #334155;
        border: 1px solid var(--border-subtle);
        padding: 0.25rem 0.6rem;
        border-radius: var(--radius-pill);
        font-size: 0.72rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .pill-badge-neutral {
        background: var(--surface-subtle);
        color: var(--text-secondary);
        border: 1px solid var(--border-subtle);
        padding: 0.2rem 0.55rem;
        border-radius: var(--radius-pill);
        font-size: 0.72rem;
        font-weight: 500;
    }

    /* Buttons (Phase 9 tactile interaction) */
    .stButton > button {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow: 0 2px 8px rgba(249, 115, 22, 0.25) !important;
        transition: all var(--duration-fast) var(--ease-fluid) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.35) !important;
    }
    .stButton > button:active {
        transform: scale(0.98) !important;
    }

    /* Form Controls */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: var(--card-surface) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-default) !important;
        border-radius: var(--radius-md) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.88rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
        transition: border-color var(--duration-fast) ease, box-shadow var(--duration-fast) ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--brand-primary) !important;
        box-shadow: var(--shadow-focus) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--surface-subtle) !important;
        border-radius: var(--radius-md) !important;
        padding: 4px !important;
        border: 1px solid var(--border-subtle) !important;
        gap: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: var(--text-muted) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.45rem 1rem !important;
        font-weight: 500 !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--card-surface) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05) !important;
    }

    /* Dataframe Table Polish (Phase 8 Consistency) */
    div[data-testid="stDataFrame"] {
        background: var(--card-surface) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-lg) !important;
        box-shadow: var(--shadow-ambient) !important;
        overflow: hidden !important;
    }

    /* Plotly Visualizer Container */
    div.stPlotlyChart {
        background: var(--card-surface) !important;
        border: 1px solid var(--border-hairline) !important;
        border-radius: var(--radius-lg) !important;
        padding: 0.5rem !important;
        box-shadow: var(--shadow-ambient) !important;
        transition: box-shadow var(--duration-fast) var(--ease-fluid);
    }
    div.stPlotlyChart:hover {
        box-shadow: var(--shadow-elevated) !important;
    }

    /* Phase 10: Responsive Breakpoint Rules */
    @media (max-width: 1024px) {
        .main .block-container {
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
        }
        .brand-hero-card {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 0.75rem !important;
        }
        .kpi-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
    }

    @media (max-width: 640px) {
        .kpi-grid {
            grid-template-columns: 1fr !important;
        }
    }

    /* Accessibility: Reduced Motion */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation: none !important;
            transition: none !important;
            transform: none !important;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
