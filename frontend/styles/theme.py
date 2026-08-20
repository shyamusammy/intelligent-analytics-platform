"""
Intelligent Analytics Platform
Global Streamlit theme and styling.
"""

import streamlit as st


# ============================================================
# DESIGN TOKENS
# ============================================================

COLORS = {
    "background": "#F8FAFC",
    "surface": "#FFFFFF",
    "surface_alt": "#F1F5F9",

    "primary": "#2563EB",
    "primary_hover": "#1D4ED8",
    "primary_soft": "#EFF6FF",

    "text": "#0F172A",
    "text_secondary": "#475569",
    "text_muted": "#64748B",

    "border": "#E2E8F0",
    "border_strong": "#CBD5E1",

    "success": "#16A34A",
    "success_soft": "#F0FDF4",

    "warning": "#D97706",
    "warning_soft": "#FFFBEB",

    "danger": "#DC2626",
    "danger_soft": "#FEF2F2",

    "info": "#0284C7",
    "info_soft": "#F0F9FF",

    "sidebar": "#FFFFFF",
}


SPACING = {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px",
    "xxl": "48px",
}


# ============================================================
# GLOBAL CSS
# ============================================================

GLOBAL_CSS = f"""
<style>

    /* ========================================================
       APP
    ======================================================== */

    .stApp {{
        background: {COLORS["background"]};
        color: {COLORS["text"]};
    }}

    .main .block-container {{
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }}


    /* ========================================================
       TYPOGRAPHY
    ======================================================== */

    html,
    body,
    [class*="css"] {{
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }}

    h1,
    h2,
    h3,
    h4 {{
        color: {COLORS["text"]};
        letter-spacing: -0.02em;
    }}

    h1 {{
        font-size: 2rem;
        font-weight: 700;
    }}

    h2 {{
        font-size: 1.35rem;
        font-weight: 650;
    }}

    h3 {{
        font-size: 1.05rem;
        font-weight: 650;
    }}


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {{
        background: {COLORS["sidebar"]};
        border-right: 1px solid {COLORS["border"]};
    }}

    section[data-testid="stSidebar"] > div {{
        padding-top: 1.5rem;
    }}


    /* ========================================================
       BUTTONS
    ======================================================== */

    .stButton > button {{
        border-radius: 8px;
        border: 1px solid {COLORS["border_strong"]};
        background: {COLORS["surface"]};
        color: {COLORS["text"]};
        font-weight: 600;
        min-height: 40px;

        transition:
            background 0.15s ease,
            border-color 0.15s ease,
            transform 0.15s ease;
    }}

    .stButton > button:hover {{
        border-color: {COLORS["primary"]};
        color: {COLORS["primary"]};
        background: {COLORS["primary_soft"]};
    }}

    .stButton > button[kind="primary"] {{
        background: {COLORS["primary"]};
        border-color: {COLORS["primary"]};
        color: white;
    }}

    .stButton > button[kind="primary"]:hover {{
        background: {COLORS["primary_hover"]};
        border-color: {COLORS["primary_hover"]};
        color: white;
    }}


    /* ========================================================
       FILE UPLOADER
    ======================================================== */

    [data-testid="stFileUploader"] {{
        background: {COLORS["surface"]};
        border: 1px dashed {COLORS["border_strong"]};
        border-radius: 12px;
        padding: 0.5rem;
    }}


    /* ========================================================
       METRIC WIDGET
    ======================================================== */

    [data-testid="stMetric"] {{
        background: {COLORS["surface"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 12px;
        padding: 1rem 1.1rem;
    }}

    [data-testid="stMetricLabel"] {{
        color: {COLORS["text_muted"]};
        font-weight: 500;
    }}

    [data-testid="stMetricValue"] {{
        color: {COLORS["text"]};
        font-weight: 700;
    }}


    /* ========================================================
       DATAFRAMES
    ======================================================== */

    [data-testid="stDataFrame"] {{
        border: 1px solid {COLORS["border"]};
        border-radius: 10px;
        overflow: hidden;
    }}


    /* ========================================================
       EXPANDERS
    ======================================================== */

    [data-testid="stExpander"] {{
        border: 1px solid {COLORS["border"]};
        border-radius: 10px;
        background: {COLORS["surface"]};
    }}


    /* ========================================================
       ALERTS
    ======================================================== */

    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}


    /* ========================================================
       DIVIDERS
    ======================================================== */

    hr {{
        border: none;
        border-top: 1px solid {COLORS["border"]};
        margin: 1.5rem 0;
    }}


    /* ========================================================
       CUSTOM CARDS
    ======================================================== */

    .ia-card {{
        background: {COLORS["surface"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 14px;
        padding: 1.25rem;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
    }}

    .ia-card-title {{
        color: {COLORS["text"]};
        font-size: 0.95rem;
        font-weight: 650;
        margin-bottom: 0.35rem;
    }}

    .ia-card-subtitle {{
        color: {COLORS["text_muted"]};
        font-size: 0.82rem;
    }}


    /* ========================================================
       PAGE HEADER
    ======================================================== */

    .ia-page-header {{
        margin-bottom: 1.75rem;
    }}

    .ia-page-title {{
        color: {COLORS["text"]};
        font-size: 2rem;
        font-weight: 750;
        line-height: 1.15;
        margin-bottom: 0.35rem;
    }}

    .ia-page-description {{
        color: {COLORS["text_secondary"]};
        font-size: 0.95rem;
        line-height: 1.5;
    }}


    /* ========================================================
       STATUS BADGES
    ======================================================== */

    .ia-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 9px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 650;
    }}

    .ia-badge-success {{
        color: {COLORS["success"]};
        background: {COLORS["success_soft"]};
    }}

    .ia-badge-warning {{
        color: {COLORS["warning"]};
        background: {COLORS["warning_soft"]};
    }}

    .ia-badge-danger {{
        color: {COLORS["danger"]};
        background: {COLORS["danger_soft"]};
    }}

    .ia-badge-info {{
        color: {COLORS["info"]};
        background: {COLORS["info_soft"]};
    }}


    /* ========================================================
       INSIGHT CARDS
    ======================================================== */

    .ia-insight {{
        background: {COLORS["surface"]};
        border: 1px solid {COLORS["border"]};
        border-left: 4px solid {COLORS["primary"]};
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
    }}

    .ia-insight-warning {{
        border-left-color: {COLORS["warning"]};
    }}

    .ia-insight-danger {{
        border-left-color: {COLORS["danger"]};
    }}

    .ia-insight-success {{
        border-left-color: {COLORS["success"]};
    }}

    .ia-insight-title {{
        color: {COLORS["text"]};
        font-weight: 650;
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }}

    .ia-insight-description {{
        color: {COLORS["text_secondary"]};
        font-size: 0.86rem;
        line-height: 1.5;
    }}


    /* ========================================================
       PIPELINE
    ======================================================== */

    .ia-pipeline {{
        background: {COLORS["surface"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 14px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
    }}

    .ia-pipeline-step {{
        text-align: center;
        color: {COLORS["text_muted"]};
        font-size: 0.78rem;
        font-weight: 600;
    }}

    .ia-pipeline-step-active {{
        color: {COLORS["primary"]};
    }}

    .ia-pipeline-step-complete {{
        color: {COLORS["success"]};
    }}


    /* ========================================================
       SCROLLBAR
    ======================================================== */

    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: transparent;
    }}

    ::-webkit-scrollbar-thumb {{
        background: {COLORS["border_strong"]};
        border-radius: 10px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS["text_muted"]};
    }}

</style>
"""


# ============================================================
# APPLY THEME
# ============================================================

def apply_theme() -> None:
    """Apply the global Intelligent Analytics visual theme."""

    st.markdown(
        GLOBAL_CSS,
        unsafe_allow_html=True,
    )