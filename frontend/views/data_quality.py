"""
Intelligent Analytics Platform
Data Quality view.

Focuses exclusively on the quality of the raw dataset:
- Overall quality score
- Quality status
- Quality issues
- Quality score breakdown
- Missing values by column
- Outliers by column
- Key findings

Cleaning results and before/after comparisons belong
to the Cleaning workspace.
"""

import streamlit as st

from components.layout import render_page_header
from components.metrics import metric_card


def _format_number(value) -> str:
    """Format numeric values for display."""
    if value is None:
        return "0"

    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def _format_percentage(value) -> str:
    """Format a percentage value."""
    if value is None:
        return "0.0%"

    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return str(value)


def _quality_status(score: float) -> str:
    """Return a human-readable quality status."""
    if score >= 90:
        return "Excellent"
    if score >= 75:
        return "Good"
    if score >= 60:
        return "Fair"
    return "Poor"


def _build_key_findings(
    missing_penalty: float,
    duplicate_penalty: float,
    outlier_penalty: float,
) -> list[str]:
    """
    Build data-driven quality findings.

    Findings are ranked by the actual penalty values returned
    by the ETL quality assessment.
    """

    penalties = {
        "Missing values": float(missing_penalty),
        "Duplicate rows": float(duplicate_penalty),
        "Outliers": float(outlier_penalty),
    }

    active_penalties = [
        (factor, penalty)
        for factor, penalty in penalties.items()
        if penalty > 0
    ]

    if not active_penalties:
        return [
            "No measurable quality penalties were detected "
            "in the raw dataset."
        ]

    ranked = sorted(
        active_penalties,
        key=lambda item: item[1],
        reverse=True,
    )

    findings = []

    total_issues = len(ranked)

    for index, (factor, penalty) in enumerate(ranked):
        if total_issues == 1:
            wording = "has the only measurable quality impact"

        elif index == 0:
            wording = "has the largest impact"

        elif index == 1:
            wording = "has the next-largest impact"

        elif index == 2:
            wording = "has the third-largest impact"

        else:
            wording = f"ranks {index + 1}th by quality impact"

        findings.append(
            f"**{factor} {wording}**, contributing a "
            f"**{penalty:.2f}-point penalty** to the raw quality score."
        )

    return findings


def render(result: dict) -> None:
    """Render the Data Quality page."""

    etl = result.get("etl") or {}

    quality = etl.get("quality") or {}
    missing_values = etl.get("missing_values") or {}
    duplicates = etl.get("duplicates") or {}
    outliers = etl.get("outliers") or {}

    quality_score = float(
        quality.get("quality_score", 0)
    )

    quality_status = _quality_status(
        quality_score
    )

    render_page_header(
        title="Data Quality",
        subtitle=(
            "Assess the quality of the raw dataset and "
            "identify issues that may affect downstream analysis."
        ),
    )

    # ============================================================
    # QUALITY OVERVIEW
    # ============================================================

    st.markdown("### Quality overview")

    quality_col1, quality_col2 = st.columns(2)

    with quality_col1:
        metric_card(
            label="Raw Dataset Quality",
            value=_format_percentage(
                quality_score
            ),
            description=(
                "Overall quality score calculated "
                "from detected data quality issues."
            ),
            status=quality_status,
            accent="primary",
        )

    with quality_col2:
        st.markdown(
            "#### Quality assessment"
        )

        if quality_status == "Excellent":
            st.success(
                f"**{quality_status}**\n\n"
                "The raw dataset has a strong overall "
                "quality level with relatively few detected issues."
            )

        elif quality_status == "Good":
            st.success(
                f"**{quality_status}**\n\n"
                "The raw dataset is generally usable, "
                "although some quality issues should be addressed."
            )

        elif quality_status == "Fair":
            st.warning(
                f"**{quality_status}**\n\n"
                "The raw dataset contains measurable quality "
                "issues that should be addressed before "
                "downstream analysis."
            )

        else:
            st.error(
                f"**{quality_status}**\n\n"
                "The raw dataset contains significant quality "
                "issues that should be addressed before "
                "downstream analysis."
            )

    # ============================================================
    # QUALITY ISSUES
    # ============================================================

    st.markdown("### Quality issues")

    total_missing = missing_values.get(
        "total_missing_values",
        0,
    )

    columns_with_missing = missing_values.get(
        "columns_with_missing_values",
        0,
    )

    duplicate_rows = duplicates.get(
        "duplicate_rows",
        0,
    )

    duplicate_percentage = duplicates.get(
        "duplicate_percentage",
        0,
    )

    total_outliers = outliers.get(
        "total_outliers",
        0,
    )

    affected_rows = outliers.get(
        "affected_rows",
        0,
    )

    issue_col1, issue_col2, issue_col3 = st.columns(3)

    with issue_col1:
        metric_card(
            label="Missing Values",
            value=_format_number(
                total_missing
            ),
            description=(
                f"Missing cells across "
                f"{_format_number(columns_with_missing)} "
                f"columns."
            ),
            status=(
                "Issue"
                if total_missing > 0
                else "Clean"
            ),
            accent=(
                "primary"
                if total_missing > 0
                else "success"
            ),
        )

    with issue_col2:
        metric_card(
            label="Duplicate Rows",
            value=_format_number(
                duplicate_rows
            ),
            description=(
                f"{float(duplicate_percentage):.2f}% "
                "of the raw dataset."
            ),
            status=(
                "Issue"
                if duplicate_rows > 0
                else "Clean"
            ),
            accent=(
                "primary"
                if duplicate_rows > 0
                else "success"
            ),
        )

    with issue_col3:
        metric_card(
            label="Outliers",
            value=_format_number(
                total_outliers
            ),
            description=(
                f"Affecting "
                f"{_format_number(affected_rows)} "
                "rows."
            ),
            status=(
                "Issue"
                if total_outliers > 0
                else "Clean"
            ),
            accent=(
                "primary"
                if total_outliers > 0
                else "success"
            ),
        )

    # ============================================================
    # QUALITY SCORE BREAKDOWN
    # ============================================================

    st.markdown("### Quality score breakdown")

    missing_penalty = float(
        quality.get(
            "missing_penalty",
            0,
        )
    )

    duplicate_penalty = float(
        quality.get(
            "duplicate_penalty",
            0,
        )
    )

    outlier_penalty = float(
        quality.get(
            "outlier_penalty",
            0,
        )
    )

    breakdown_rows = [
        {
            "Quality Factor": "Missing values",
            "Penalty": f"{missing_penalty:.2f}",
        },
        {
            "Quality Factor": "Duplicate rows",
            "Penalty": f"{duplicate_penalty:.2f}",
        },
        {
            "Quality Factor": "Outliers",
            "Penalty": f"{outlier_penalty:.2f}",
        },
    ]

    st.dataframe(
        breakdown_rows,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "The raw quality score reflects the penalties "
        "identified during the initial ETL quality assessment."
    )

    # ============================================================
    # MISSING VALUES BY COLUMN
    # ============================================================

    st.markdown("### Missing values by column")

    missing_by_column = missing_values.get(
        "missing_by_column",
        {},
    )

    missing_rows = [
        {
            "Column": column,
            "Missing Values": count,
        }
        for column, count in missing_by_column.items()
        if count > 0
    ]

    missing_rows.sort(
        key=lambda row: row["Missing Values"],
        reverse=True,
    )

    if missing_rows:
        st.dataframe(
            missing_rows,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Columns are ordered by the number of "
            "missing cells detected in the raw dataset."
        )

    else:
        st.success(
            "No missing values were detected in the raw dataset."
        )

    # ============================================================
    # OUTLIERS BY COLUMN
    # ============================================================

    st.markdown("### Outliers by column")

    outliers_by_column = outliers.get(
        "outliers_by_column",
        {},
    )

    outlier_rows = [
        {
            "Column": column,
            "Outliers": count,
        }
        for column, count in outliers_by_column.items()
        if count > 0
    ]

    outlier_rows.sort(
        key=lambda row: row["Outliers"],
        reverse=True,
    )

    if outlier_rows:
        st.dataframe(
            outlier_rows,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "Outliers are statistical observations identified "
            "during the initial raw-data quality assessment."
        )

    else:
        st.success(
            "No statistical outliers were detected."
        )

    # ============================================================
    # KEY FINDINGS
    # ============================================================

    st.markdown("### Key findings")

    findings = _build_key_findings(
        missing_penalty=missing_penalty,
        duplicate_penalty=duplicate_penalty,
        outlier_penalty=outlier_penalty,
    )

    for finding in findings:
        st.info(finding)

    # ============================================================
    # FOOTER
    # ============================================================

    st.markdown("---")

    st.caption(
        "This page evaluates the raw dataset. "
        "Cleaning actions and before/after improvements "
        "are shown in the Cleaning workspace."
    )