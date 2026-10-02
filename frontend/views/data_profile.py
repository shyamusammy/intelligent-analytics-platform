"""
Intelligent Analytics Platform
Data Profile view.

Focuses on understanding the raw dataset:
- Dataset structure
- Column data types
- Column-level profile
- Numeric statistics
- Numeric distribution details
- Categorical statistics
- Profile summary

Data Quality diagnostics belong to Data Quality.
Cleaning actions and before/after results belong to Cleaning.
"""

import streamlit as st

from components.layout import render_page_header
from components.metrics import metric_card


# ============================================================
# FORMATTING HELPERS
# ============================================================


def _format_number(value) -> str:
    """Format numeric values for display."""
    if value is None:
        return "0"

    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def _format_decimal(value, decimals: int = 2) -> str:
    """Format numeric values with a controlled number of decimals."""
    if value is None:
        return "-"

    try:
        return f"{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return str(value)


# ============================================================
# RENDER
# ============================================================


def render(result: dict) -> None:
    """Render the Data Profile page."""

    etl = result.get("etl") or {}
    analytics = result.get("analytics") or {}

    schema_profile = etl.get("schema_profile") or {}
    columns = schema_profile.get("columns") or []

    # --------------------------------------------------------
    # Raw dataset row count
    # --------------------------------------------------------
    #
    # Data Profile represents the raw dataset, so the row count
    # must come from the ETL/raw stage rather than analytics,
    # which represents the cleaned dataset.
    #
    raw_row_count = (
        etl.get("row_count")
        or etl.get("total_rows")
        or schema_profile.get("row_count")
        or schema_profile.get("total_rows")
    )

    if raw_row_count is None:
        cleaning = result.get("cleaning") or {}

        original_row_count = cleaning.get(
            "original_row_count"
        )

        raw_row_count = (
            original_row_count
            if original_row_count is not None
            else 0
        )

    raw_row_count = int(raw_row_count or 0)

    total_columns = schema_profile.get(
        "total_columns",
        len(columns),
    )

    # --------------------------------------------------------
    # Determine column types from ETL schema
    # --------------------------------------------------------

    numeric_columns = sum(
        1
        for column in columns
        if str(
            column.get("detected_type", "")
        ).lower()
        in {
            "int",
            "integer",
            "float",
            "numeric",
            "number",
        }
    )

    categorical_columns = sum(
        1
        for column in columns
        if str(
            column.get("detected_type", "")
        ).lower()
        == "categorical"
    )

    text_columns = sum(
        1
        for column in columns
        if str(
            column.get("detected_type", "")
        ).lower()
        == "text"
    )

    datetime_columns = sum(
        1
        for column in columns
        if str(
            column.get("detected_type", "")
        ).lower()
        in {
            "datetime",
            "date",
        }
    )

    # ============================================================
    # ANALYTICS STATISTICS
    # ============================================================

    analytics_statistics = analytics.get(
        "statistics"
    ) or {}

    numeric_statistics = analytics_statistics.get(
        "numeric_statistics"
    ) or []

    categorical_statistics = analytics_statistics.get(
        "categorical_statistics"
    ) or []

    # Support alternate backend naming if introduced later.
    if not categorical_statistics:
        categorical_statistics = analytics_statistics.get(
            "categorical"
        ) or []

    # ============================================================
    # PAGE HEADER
    # ============================================================

    render_page_header(
        title="Data Profile",
        subtitle=(
            "Understand the structure, data types, and "
            "statistical characteristics of the raw dataset."
        ),
    )

    # ============================================================
    # DATASET STRUCTURE
    # ============================================================

    st.markdown("### Dataset structure")

    structure_col1, structure_col2, structure_col3 = st.columns(3)

    with structure_col1:
        metric_card(
            label="Total Columns",
            value=_format_number(total_columns),
            description="Columns identified in the raw dataset.",
            accent="primary",
        )

    with structure_col2:
        metric_card(
            label="Numeric",
            value=_format_number(numeric_columns),
            description="Columns identified as numeric.",
            accent="primary",
        )

    with structure_col3:
        metric_card(
            label="Categorical",
            value=_format_number(categorical_columns),
            description="Columns identified as categorical.",
            accent="primary",
        )

    structure_col4, structure_col5, structure_col6 = st.columns(3)

    with structure_col4:
        metric_card(
            label="Text",
            value=_format_number(text_columns),
            description="Columns identified as text.",
            accent="primary",
        )

    with structure_col5:
        metric_card(
            label="Datetime",
            value=_format_number(datetime_columns),
            description="Columns identified as date or time.",
            accent="primary",
        )

    with structure_col6:
        metric_card(
            label="Rows",
            value=_format_number(raw_row_count),
            description="Rows in the raw dataset.",
            accent="primary",
        )

    # ============================================================
    # COLUMN PROFILE
    # ============================================================

    st.markdown("### Column profile")

    if columns:
        profile_rows = []

        for column in columns:
            name = column.get(
                "name",
                "-",
            )

            pandas_dtype = column.get(
                "pandas_dtype",
                "-",
            )

            detected_type = column.get(
                "detected_type",
                "-",
            )

            null_count = column.get(
                "null_count",
                0,
            )

            nullable = column.get(
                "nullable"
            )

            profile_rows.append(
                {
                    "Column": name,
                    "Pandas Type": pandas_dtype,
                    "Detected Type": detected_type,
                    "Missing": _format_number(
                        null_count
                    ),
                    "Nullable": (
                        "Yes"
                        if nullable is True
                        else "No"
                        if nullable is False
                        else "-"
                    ),
                }
            )

        st.dataframe(
            profile_rows,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Detected types are assigned during ETL profiling "
            "and describe how each column is interpreted."
        )

    else:
        st.info(
            "No column-level profile information is available."
        )

    # ============================================================
    # NUMERIC STATISTICS
    # ============================================================

    st.markdown("### Numeric statistics")

    if numeric_statistics:
        numeric_rows = []

        for item in numeric_statistics:
            numeric_rows.append(
                {
                    "Column": item.get(
                        "column_name",
                        "-",
                    ),
                    "Mean": _format_decimal(
                        item.get("mean")
                    ),
                    "Median": _format_decimal(
                        item.get("median")
                    ),
                    "Minimum": _format_decimal(
                        item.get("minimum")
                    ),
                    "Maximum": _format_decimal(
                        item.get("maximum")
                    ),
                    "Std. Dev.": _format_decimal(
                        item.get("std_dev")
                    ),
                }
            )

        st.dataframe(
            numeric_rows,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Summary statistics describe the distribution "
            "of numeric columns."
        )

    else:
        st.info(
            "No numeric statistics are available."
        )

    # ============================================================
    # NUMERIC DISTRIBUTION DETAILS
    # ============================================================

    numeric_detail_rows = []

    for item in numeric_statistics:
        numeric_detail_rows.append(
            {
                "Column": item.get(
                    "column_name",
                    "-",
                ),
                "Skewness": _format_decimal(
                    item.get("skewness")
                ),
                "Kurtosis": _format_decimal(
                    item.get("kurtosis")
                ),
                "Variance": _format_decimal(
                    item.get("variance")
                ),
            }
        )

    if numeric_detail_rows:
        with st.expander(
            "View distribution details"
        ):
            st.dataframe(
                numeric_detail_rows,
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Skewness, kurtosis, and variance provide "
                "additional information about numeric distributions."
            )

    # ============================================================
    # CATEGORICAL STATISTICS
    # ============================================================

    st.markdown("### Categorical statistics")

    if categorical_statistics:
        categorical_rows = []

        for item in categorical_statistics:
            column_name = (
                item.get("column_name")
                or item.get("column")
                or "-"
            )

            unique_count = (
                item.get("unique_count")
                or item.get("unique_values")
                or item.get("nunique")
            )

            top_value = (
                item.get("top_value")
                or item.get("mode")
                or item.get("most_frequent")
            )

            categorical_rows.append(
                {
                    "Column": column_name,
                    "Unique Values": (
                        _format_number(unique_count)
                        if unique_count is not None
                        else "-"
                    ),
                    "Most Frequent": (
                        str(top_value)
                        if top_value is not None
                        else "-"
                    ),
                }
            )

        st.dataframe(
            categorical_rows,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Categorical statistics summarize the number of "
            "distinct values and the most frequent value "
            "for each categorical column."
        )

    else:
        st.info(
            "Categorical statistics are not available "
            "in the current analytics response."
        )

    # ============================================================
    # PROFILE SUMMARY
    # ============================================================

    st.markdown("### Profile summary")

    summary_items = []

    summary_items.append(
        f"The raw dataset contains **{_format_number(raw_row_count)} "
        f"rows** across **{_format_number(total_columns)} columns**."
    )

    type_parts = []

    if numeric_columns:
        type_parts.append(
            f"{_format_number(numeric_columns)} numeric"
        )

    if categorical_columns:
        type_parts.append(
            f"{_format_number(categorical_columns)} categorical"
        )

    if text_columns:
        type_parts.append(
            f"{_format_number(text_columns)} text"
        )

    if datetime_columns:
        type_parts.append(
            f"{_format_number(datetime_columns)} datetime"
        )

    if type_parts:
        summary_items.append(
            "Column types include "
            + ", ".join(type_parts)
            + "."
        )

    for item in summary_items:
        st.info(item)

    # ============================================================
    # FOOTER
    # ============================================================

    st.markdown("---")

    st.caption(
        "This page describes the raw dataset structure and "
        "statistical profile. Detailed quality issues are "
        "shown in Data Quality, while remediation actions "
        "are shown in Cleaning."
    )