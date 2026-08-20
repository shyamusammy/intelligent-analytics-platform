"""
Intelligent Analytics Platform
Overview workspace.
"""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

from components.layout import render_page_header
from components.pipeline import render_pipeline
from components.metrics import (
    metric_grid,
    comparison_card,
)
from components.intelligence import render_insights


# ============================================================
# HELPERS
# ============================================================

def _get(data: Any, *keys: str, default=None):
    """
    Safely retrieve nested dictionary values.

    Example:
        _get(result, "cleaning", "original_row_count")
    """

    current = data

    for key in keys:

        if not isinstance(current, dict):
            return default

        current = current.get(key)

        if current is None:
            return default

    return current


def _first(data: Any, paths: list[tuple[str, ...]], default=None):
    """
    Return the first non-None value from multiple nested paths.
    """

    for path in paths:

        value = _get(
            data,
            *path,
            default=None,
        )

        if value is not None:
            return value

    return default


def _format_number(value: Any) -> str:
    """
    Format numbers for dashboard display.
    """

    if value is None:
        return "—"

    try:

        number = float(value)

        if number.is_integer():
            return f"{int(number):,}"

        return f"{number:,.2f}"

    except (TypeError, ValueError):

        return str(value)


def _format_score(value: Any) -> str:
    """
    Format a quality score as a percentage.

    Handles both:
        0.92  -> 92.0%
        92.0  -> 92.0%
    """

    if value is None:
        return "—"

    try:

        score = float(value)

        if abs(score) <= 1:
            score *= 100

        return f"{score:.1f}%"

    except (TypeError, ValueError):

        return str(value)


def _safe_text(value: Any) -> str:
    """
    Escape text used in HTML.
    """

    return html.escape(
        str(value)
    )


def _count_collection(value: Any) -> int:
    """
    Safely count list/dict based analytical results.

    Handles structures such as:

        []
        {}
        {"correlations": [...]}
        {"segments": [...]}
    """

    if value is None:
        return 0

    if isinstance(value, list):
        return len(value)

    if isinstance(value, dict):

        # Common nested collection names.
        for key in (
            "correlations",
            "segments",
            "results",
            "items",
            "data",
        ):

            nested = value.get(key)

            if isinstance(nested, list):
                return len(nested)

        # If there is no nested collection, don't count
        # metadata keys as analytical results.
        return 0

    return 0


# ============================================================
# DATA EXTRACTION
# ============================================================

def _extract_dataset_metrics(result: dict[str, Any]) -> dict[str, Any]:
    """
    Extract Overview metrics from the actual analysis response.

    Current API structure:

        etl
            schema_profile
                total_columns
            missing_values
                total_missing_values
            duplicates
                duplicate_rows

        cleaning
            original_row_count
            cleaned_row_count
            duplicates_removed
            missing_values_before
            missing_values_after
            quality_score_before
            quality_score_after

        analytics
            statistics
                dataset_summary
                    total_rows
                    total_columns

            correlations
                correlations

            segmentation
                segments

        ml
            best_model
                estimator
    """

    # ========================================================
    # RAW ROWS
    # ========================================================

    raw_rows = _first(
        result,
        [
            # PRIMARY CURRENT API
            ("cleaning", "original_row_count"),

            # Possible top-level structures
            ("raw_rows",),
            ("original_rows",),

            ("dataset", "raw_rows"),
            ("dataset", "original_rows"),

            # Analytics fallback
            (
                "analytics",
                "statistics",
                "dataset_summary",
                "total_rows",
            ),

            # ETL fallback
            ("etl", "raw_rows"),
            ("etl", "original_rows"),

            (
                "etl",
                "profile",
                "row_count",
            ),

            (
                "etl",
                "profiling",
                "row_count",
            ),

            (
                "profile",
                "row_count",
            ),

            (
                "profiling",
                "row_count",
            ),
        ],
    )

    # ========================================================
    # CLEANED ROWS
    # ========================================================

    cleaned_rows = _first(
        result,
        [
            # PRIMARY CURRENT API
            ("cleaning", "cleaned_row_count"),

            # Possible alternate structures
            ("cleaned_rows",),

            (
                "dataset",
                "cleaned_rows",
            ),

            (
                "cleaning",
                "row_count",
            ),

            (
                "etl",
                "cleaned_rows",
            ),

            (
                "etl",
                "cleaning",
                "cleaned_rows",
            ),

            (
                "etl",
                "cleaning",
                "row_count",
            ),

            (
                "cleaned_dataset",
                "row_count",
            ),

            # Analytics is generally calculated after cleaning.
            (
                "analytics",
                "statistics",
                "dataset_summary",
                "total_rows",
            ),
        ],
    )

    # ========================================================
    # COLUMNS
    # ========================================================

    columns = _first(
        result,
        [
            # PRIMARY CURRENT API
            (
                "etl",
                "schema_profile",
                "total_columns",
            ),

            (
                "analytics",
                "statistics",
                "dataset_summary",
                "total_columns",
            ),

            # Alternate structures
            ("columns",),
            ("column_count",),

            (
                "dataset",
                "columns",
            ),

            (
                "dataset",
                "column_count",
            ),

            (
                "etl",
                "columns",
            ),

            (
                "etl",
                "column_count",
            ),

            (
                "schema_profile",
                "total_columns",
            ),

            (
                "schema_profile",
                "column_count",
            ),

            (
                "profile",
                "column_count",
            ),
        ],
    )

    # ========================================================
    # DUPLICATES REMOVED
    # ========================================================

    duplicates_removed = _first(
        result,
        [
            # PRIMARY CURRENT API
            (
                "cleaning",
                "duplicates_removed",
            ),

            # Alternate structures
            ("duplicates_removed",),

            (
                "cleaning",
                "duplicates",
                "removed",
            ),

            (
                "cleaning",
                "summary",
                "duplicates_removed",
            ),

            (
                "etl",
                "duplicates_removed",
            ),

            (
                "etl",
                "duplicates",
                "removed",
            ),

            (
                "duplicates",
                "removed",
            ),

            (
                "etl",
                "duplicates",
                "duplicate_rows",
            ),

            (
                "duplicates",
                "duplicate_rows",
            ),
        ],
        default=0,
    )

    # ========================================================
    # MISSING VALUES BEFORE
    # ========================================================

    missing_before = _first(
        result,
        [
            # PRIMARY CURRENT API
            (
                "cleaning",
                "missing_values_before",
            ),

            # ETL profile fallback
            (
                "etl",
                "missing_values",
                "total_missing_values",
            ),

            # Alternate structures
            ("missing_before",),

            (
                "cleaning",
                "missing_before",
            ),

            (
                "cleaning",
                "summary",
                "missing_before",
            ),

            (
                "etl",
                "missing_before",
            ),

            (
                "missing_values",
                "total_missing_values",
            ),

            (
                "missing_values",
                "total",
            ),

            (
                "missing_values",
                "before",
            ),
        ],
        default=0,
    )

    # ========================================================
    # MISSING VALUES AFTER
    # ========================================================

    missing_after = _first(
        result,
        [
            # PRIMARY CURRENT API
            (
                "cleaning",
                "missing_values_after",
            ),

            # Alternate structures
            ("missing_after",),

            (
                "cleaning",
                "missing_after",
            ),

            (
                "cleaning",
                "summary",
                "missing_after",
            ),

            (
                "cleaning",
                "remaining_missing",
            ),

            (
                "cleaning",
                "missing_values_after",
            ),

            (
                "missing_values",
                "after",
            ),
        ],
        default=0,
    )

    # ========================================================
    # RAW QUALITY
    # ========================================================

    raw_quality = _first(
        result,
        [
            # PRIMARY CURRENT API
            (
                "cleaning",
                "quality_score_before",
            ),

            # ETL quality fallback
            (
                "etl",
                "quality",
                "quality_score",
            ),

            (
                "quality",
                "quality_score",
            ),

            # Alternate structures
            ("raw_quality_score",),

            (
                "quality",
                "raw_score",
            ),

            (
                "quality",
                "raw_quality_score",
            ),

            (
                "quality",
                "before",
            ),

            (
                "quality",
                "before_cleaning",
            ),

            (
                "etl",
                "quality",
                "raw_score",
            ),

            (
                "etl",
                "quality",
                "raw_quality_score",
            ),
        ],
    )

    # ========================================================
    # CLEANED QUALITY
    # ========================================================

    cleaned_quality = _first(
        result,
        [
            # PRIMARY CURRENT API
            (
                "cleaning",
                "quality_score_after",
            ),

            # Alternate structures
            ("cleaned_quality_score",),

            (
                "cleaning",
                "quality_score",
            ),

            (
                "cleaning",
                "cleaned_quality_score",
            ),

            (
                "quality",
                "cleaned_score",
            ),

            (
                "quality",
                "cleaned_quality_score",
            ),

            (
                "quality",
                "score",
            ),

            (
                "etl",
                "quality",
                "cleaned_score",
            ),

            (
                "etl",
                "quality",
                "cleaned_quality_score",
            ),

            (
                "etl",
                "quality",
                "score",
            ),

            (
                "quality",
                "after",
            ),

            (
                "quality",
                "after_cleaning",
            ),
        ],
    )

    # ========================================================
    # FINAL FALLBACK QUALITY OBJECT
    # ========================================================

    quality = result.get(
        "quality"
    )

    if isinstance(
        quality,
        dict,
    ):

        if raw_quality is None:

            raw_quality = (
                quality.get("raw_score")
                if quality.get("raw_score") is not None
                else quality.get("before")
            )

            if raw_quality is None:
                raw_quality = quality.get(
                    "before_cleaning"
                )

            if raw_quality is None:
                raw_quality = quality.get(
                    "quality_score"
                )

        if cleaned_quality is None:

            cleaned_quality = (
                quality.get("cleaned_score")
                if quality.get("cleaned_score") is not None
                else quality.get("score")
            )

            if cleaned_quality is None:
                cleaned_quality = quality.get(
                    "after"
                )

            if cleaned_quality is None:
                cleaned_quality = quality.get(
                    "after_cleaning"
                )

    # ========================================================
    # RETURN
    # ========================================================

    return {
        "raw_rows": raw_rows,
        "cleaned_rows": cleaned_rows,
        "columns": columns,
        "duplicates_removed": duplicates_removed,
        "missing_before": missing_before,
        "missing_after": missing_after,
        "raw_quality": raw_quality,
        "cleaned_quality": cleaned_quality,
    }


# ============================================================
# DATASET CONTEXT
# ============================================================

def _render_dataset_context() -> None:
    """
    Render active dataset context.
    """

    filename = (
        st.session_state.get(
            "uploaded_file_name"
        )
        or "Current dataset"
    )

    safe_filename = _safe_text(
        filename
    )

    dataset_html = f"""
<div style="
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:16px;
    padding:14px 16px;
    margin-bottom:24px;
    background:#F8FAFC;
    border:1px solid #E2E8F0;
    border-radius:12px;
    box-sizing:border-box;
">

    <div style="
        min-width:0;
        flex:1;
    ">

        <div style="
            color:#64748B;
            font-size:11px;
            font-weight:700;
            text-transform:uppercase;
            letter-spacing:0.06em;
        ">
            Active Dataset
        </div>

        <div style="
            color:#0F172A;
            font-size:14px;
            font-weight:650;
            margin-top:4px;
            white-space:nowrap;
            overflow:hidden;
            text-overflow:ellipsis;
        ">
            {safe_filename}
        </div>

    </div>

    <div style="
        flex-shrink:0;
        color:#64748B;
        background:#FFFFFF;
        border:1px solid #E2E8F0;
        border-radius:999px;
        padding:5px 10px;
        font-size:11px;
        font-weight:650;
    ">
        Analysis session
    </div>

</div>
"""

    st.html(
        dataset_html
    )


# ============================================================
# PAGE
# ============================================================

def render(result: dict[str, Any]) -> None:
    """
    Render the Overview workspace.
    """

    if not isinstance(
        result,
        dict,
    ):

        st.error(
            "No analysis result is available."
        )

        return

    # ========================================================
    # EXTRACT METRICS
    # ========================================================

    metrics = _extract_dataset_metrics(
        result
    )

    # ========================================================
    # DEBUG
    # ========================================================

    with st.expander(
        "DEBUG — API Result",
        expanded=False,
    ):

        st.json(
            result
        )

    # ========================================================
    # HEADER
    # ========================================================

    render_page_header(
        title="Overview",
        subtitle=(
            "A high-level view of dataset health, "
            "processing and analytical readiness."
        ),
    )

    # ========================================================
    # DATASET CONTEXT
    # ========================================================

    _render_dataset_context()

    # ========================================================
    # DATASET SNAPSHOT
    # ========================================================

    st.markdown(
        "#### Dataset Snapshot"
    )

    # --------------------------------------------------------
    # ROWS REMOVED
    # --------------------------------------------------------

    rows_removed = None

    if (
        metrics["raw_rows"] is not None
        and metrics["cleaned_rows"] is not None
    ):

        try:

            rows_removed = (
                float(metrics["raw_rows"])
                - float(metrics["cleaned_rows"])
            )

        except (
            TypeError,
            ValueError,
        ):

            rows_removed = None

    metric_grid(
        [
            {
                "label": "Raw Rows",
                "value": _format_number(
                    metrics["raw_rows"]
                ),
                "description": "Original records",
                "accent": "info",
            },
            {
                "label": "Cleaned Rows",
                "value": _format_number(
                    metrics["cleaned_rows"]
                ),
                "description": "Records after cleaning",
                "accent": "success",
            },
            {
                "label": "Columns",
                "value": _format_number(
                    metrics["columns"]
                ),
                "description": "Dataset fields",
                "accent": "primary",
            },
            {
                "label": "Rows Removed",
                "value": _format_number(
                    rows_removed
                ),
                "description": "Records removed during cleaning",
                "accent": "warning",
            },
        ],
        columns=4,
    )

    # ========================================================
    # DATASET HEALTH
    # ========================================================

    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "#### Dataset Health"
    )

    health_cols = st.columns(
        2
    )

    # ========================================================
    # QUALITY SCORE
    # ========================================================

    with health_cols[0]:

        quality_change = None

        if (
            metrics["raw_quality"] is not None
            and metrics["cleaned_quality"] is not None
        ):

            try:

                quality_change = (
                    float(metrics["cleaned_quality"])
                    - float(metrics["raw_quality"])
                )

            except (
                TypeError,
                ValueError,
            ):

                quality_change = None

        quality_description = None

        if quality_change is not None:

            if quality_change > 0:

                quality_description = (
                    f"Improved by "
                    f"{quality_change:.1f} percentage points"
                )

            elif quality_change < 0:

                quality_description = (
                    f"Changed by "
                    f"{quality_change:.1f} percentage points"
                )

            else:

                quality_description = (
                    "No change in quality score"
                )

        comparison_card(
            label="Quality Score",
            before_label="Raw Dataset",
            before_value=_format_score(
                metrics["raw_quality"]
            ),
            after_label="Cleaned Dataset",
            after_value=_format_score(
                metrics["cleaned_quality"]
            ),
            description=quality_description,
            accent="primary",
        )

    # ========================================================
    # MISSING VALUES
    # ========================================================

    with health_cols[1]:

        missing_reduction = None

        if (
            metrics["missing_before"] is not None
            and metrics["missing_after"] is not None
        ):

            try:

                missing_reduction = (
                    float(metrics["missing_before"])
                    - float(metrics["missing_after"])
                )

            except (
                TypeError,
                ValueError,
            ):

                missing_reduction = None

        missing_description = None

        if missing_reduction is not None:

            if missing_reduction > 0:

                missing_description = (
                    f"Reduced by "
                    f"{_format_number(missing_reduction)}"
                )

            elif missing_reduction == 0:

                missing_description = (
                    "No reduction in missing values"
                )

            else:

                missing_description = (
                    f"Increased by "
                    f"{_format_number(abs(missing_reduction))}"
                )

        comparison_card(
            label="Missing Values",
            before_label="Before Cleaning",
            before_value=_format_number(
                metrics["missing_before"]
            ),
            after_label="After Cleaning",
            after_value=_format_number(
                metrics["missing_after"]
            ),
            description=missing_description,
            accent="success",
        )

    # ========================================================
    # ANALYSIS PIPELINE
    # ========================================================

    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "#### Analysis Pipeline"
    )

    render_pipeline(
        current_step="intelligence",
        completed_steps=[
            "upload",
            "etl",
            "profile",
            "analytics",
            "ml",
            "intelligence",
        ],
    )

    # ========================================================
    # ANALYTICS
    # ========================================================

    analytics = result.get(
        "analytics",
        {},
    )

    if not isinstance(
        analytics,
        dict,
    ):

        analytics = {}

    # ========================================================
    # CORRELATIONS
    # ========================================================

    correlations = analytics.get(
        "correlations",
        [],
    )

    correlation_count = _count_collection(
        correlations
    )

    # ========================================================
    # SEGMENTATION
    # ========================================================

    segmentation = analytics.get(
        "segmentation",
        [],
    )

    segmentation_count = _count_collection(
        segmentation
    )

    # ========================================================
    # ML
    # ========================================================

    ml = result.get(
        "ml",
        {},
    )

    if not isinstance(
        ml,
        dict,
    ):

        ml = {}

    best_model = _first(
        ml,
        [
            (
                "best_model",
                "estimator",
            ),

            (
                "best_model",
                "name",
            ),

            (
                "selected_model",
            ),

            (
                "best_model_name",
            ),

            (
                "estimator",
            ),
        ],
    )

    if isinstance(
        best_model,
        dict,
    ):

        best_model = (
            best_model.get(
                "estimator"
            )
            or best_model.get(
                "name"
            )
            or "Available"
        )

    # ========================================================
    # ANALYTICAL SIGNALS
    # ========================================================

    st.markdown(
        "<div style='height:18px'></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "#### Analytical Signals"
    )

    metric_grid(
        [
            {
                "label": "Relationships",
                "value": _format_number(
                    correlation_count
                ),
                "description": "Correlation results",
                "accent": "info",
            },
            {
                "label": "Segments",
                "value": _format_number(
                    segmentation_count
                ),
                "description": "Segmentation results",
                "accent": "primary",
            },
            {
                "label": "Best Model",
                "value": (
                    str(best_model)
                    if best_model
                    else "Available"
                ),
                "description": "Selected ML model",
                "accent": "success",
            },
        ],
        columns=3,
    )

    # ========================================================
    # KEY FINDINGS
    # ========================================================

    insights = _first(
        result,
        [
            (
                "intelligence",
                "insights",
            ),

            (
                "business_insights",
            ),

            (
                "analytics",
                "insights",
            ),
        ],
        default=[],
    )

    if (
        isinstance(
            insights,
            list,
        )
        and insights
    ):

        st.markdown(
            "<div style='height:18px'></div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "#### Key Findings"
        )

        render_insights(
            insights,
            max_items=3,
        )