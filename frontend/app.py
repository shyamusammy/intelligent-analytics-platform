"""
Intelligent Analytics Platform

Streamlit application shell.
"""

import os

import requests
import streamlit as st

from components.layout import render_page_header
from components.pipeline import render_pipeline
from styles.theme import apply_theme


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Intelligent Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# API CONFIGURATION
# ============================================================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None


# ============================================================
# APPLICATION HEADER
# ============================================================

render_page_header(
    title="Intelligent Analytics Platform",
    subtitle=(
        "Turn a business dataset into analysis, "
        "models, insights, and decisions."
    ),
)


# ============================================================
# UPLOAD SECTION
# ============================================================

st.markdown("### Start with your dataset")

st.caption(
    "Upload a CSV or Excel file. "
    "The platform will automatically process the dataset."
)

uploaded_file = st.file_uploader(
    "Dataset",
    type=[
        "csv",
        "xlsx",
        "xls",
    ],
    label_visibility="collapsed",
)


# ============================================================
# FILE STATUS
# ============================================================

if uploaded_file:
    st.session_state.uploaded_file_name = uploaded_file.name

    st.success(
        f"Dataset ready: **{uploaded_file.name}**"
    )


# ============================================================
# RUN ANALYSIS
# ============================================================

run_analysis = st.button(
    "Run Complete Analysis",
    type="primary",
    disabled=uploaded_file is None,
    use_container_width=False,
)


if run_analysis:
    with st.status(
        "Running intelligent analysis...",
        expanded=True,
    ) as status:
        try:
            st.write("Uploading dataset...")

            response = requests.post(
                f"{API_URL}/analysis/run",
                data={},
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                        or "application/octet-stream",
                    )
                },
                timeout=300,
            )

            response.raise_for_status()

            st.write(
                "Processing ETL, cleaning, analytics, ML "
                "and business intelligence..."
            )

            st.session_state.result = response.json()

            status.update(
                label="Analysis completed",
                state="complete",
            )

            st.rerun()

        except requests.RequestException as exc:
            status.update(
                label="Analysis failed",
                state="error",
            )

            st.error(
                f"Unable to complete analysis: {exc}"
            )


# ============================================================
# WAITING STATE
# ============================================================

result = st.session_state.result

if not result:
    st.markdown("---")

    render_pipeline(
        current_step="upload",
        completed_steps=[],
    )

    st.info(
        "Upload a dataset and run the complete analysis "
        "to explore your results."
    )

    st.stop()


# ============================================================
# RESULT NAVIGATION
# ============================================================
#
# Product workflow:
#
#   Overview
#       ↓
#   Data Profile
#       ↓
#   Cleaning
#       ↓
#   Data Quality
#       ↓
#   Analytics
#       ↓
#   Machine Learning
#       ↓
#   Business Insights
#
# Data Profile describes the dataset structure and
# characteristics before cleaning.
#
# Cleaning describes the transformations applied.
#
# Data Quality compares the dataset before and after
# cleaning.
#
# ============================================================

pages = {
    "Overview": "overview",
    "Data Profile": "data_profile",
    "Cleaning": "cleaning",
    "Data Quality": "data_quality",
    "Analytics": "analytics",
    "Machine Learning": "machine_learning",
    "Business Insights": "intelligence",
}


selected_page = st.sidebar.radio(
    "Workspace",
    list(pages.keys()),
)


# ============================================================
# DATASET CONTEXT
# ============================================================

st.sidebar.markdown("---")

st.sidebar.caption("CURRENT DATASET")

st.sidebar.markdown(
    f"**{st.session_state.uploaded_file_name or 'Dataset'}**"
)

st.sidebar.caption(
    "Analysis results are stored for this session."
)


# ============================================================
# VIEW ROUTING
# ============================================================

if selected_page == "Overview":
    from views.overview import render

    render(result)


elif selected_page == "Data Profile":
    from views.data_profile import render

    render(result)


elif selected_page == "Cleaning":
    from views.cleaning import render

    render(result)


elif selected_page == "Data Quality":
    from views.data_quality import render

    render(result)


elif selected_page == "Analytics":
    from views.analytics import render

    render(result)


elif selected_page == "Machine Learning":
    from views.machine_learning import render

    render(result)


elif selected_page == "Business Insights":
    from views.intelligence import render

    render(result)