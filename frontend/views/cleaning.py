"""
Intelligent Analytics Platform
Cleaning view.

Shows the transformations applied during the cleaning stage
using only the information returned by the pipeline.
"""

import streamlit as st

from components.layout import render_page_header
from components.metrics import metric_card


# ============================================================
# HELPERS
# ============================================================

def _format_number(value, default="—") -> str:
    """Format numeric values for display."""
    if value is None:
        return default

    try:
        number = float(value)

        if number.is_integer():
            return f"{int(number):,}"

        return f"{number:,.2f}"

    except (TypeError, ValueError):
        return str(value)


def _format_percentage(value, default="—") -> str:
    """Format percentage values for display."""
    if value is None:
        return default

    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return str(value)


def _format_strategy(strategy) -> str:
    """Convert an internal strategy name into a readable label."""
    if not strategy:
        return "—"

    text = str(strategy).replace("_", " ")

    return text.strip().title()


def _get_outlier_map(outlier_result) -> dict:
    """Safely extract outliers by column."""
    if not isinstance(outlier_result, dict):
        return {}

    values = outlier_result.get(
        "outliers_by_column",
        {},
    )

    return values if isinstance(values, dict) else {}


def _build_action_rows(actions: list) -> list:
    """Build display rows from recorded cleaning actions."""
    rows = []

    for action in actions:
        if not isinstance(action, dict):
            continue

        rows.append(
            {
                "Column": action.get(
                    "column_name",
                    "—",
                ),
                "Strategy": _format_strategy(
                    action.get("strategy")
                ),
                "Values Replaced": _format_number(
                    action.get("values_replaced")
                ),
            }
        )

    return rows


def _get_affected_columns(actions: list) -> list:
    """
    Derive affected columns from cleaning actions.

    Dataset-level operations such as '__dataset__' are excluded
    from the column count.
    """
    columns = []

    for action in actions:
        if not isinstance(action, dict):
            continue

        column = action.get("column_name")

        if not column:
            continue

        if column == "__dataset__":
            continue

        if column not in columns:
            columns.append(column)

    return columns


def _get_dataset_operations(actions: list) -> list:
    """
    Extract dataset-level cleaning operations.

    The pipeline currently represents these using '__dataset__',
    but the implementation does not depend on a specific
    operation name.
    """
    operations = []

    for action in actions:
        if not isinstance(action, dict):
            continue

        column = action.get("column_name")

        if column != "__dataset__":
            continue

        operations.append(action)

    return operations


def _build_outlier_rows(outlier_map: dict) -> list:
    """Build sorted outlier table rows."""
    rows = []

    for column, count in outlier_map.items():
        try:
            numeric_count = int(count)
        except (TypeError, ValueError):
            numeric_count = 0

        if numeric_count <= 0:
            continue

        rows.append(
            {
                "Column": column,
                "Outliers": numeric_count,
            }
        )

    rows.sort(
        key=lambda row: row["Outliers"],
        reverse=True,
    )

    for row in rows:
        row["Outliers"] = _format_number(
            row["Outliers"]
        )

    return rows


# ============================================================
# MAIN VIEW
# ============================================================

def render(result: dict) -> None:
    """Render the Cleaning page."""

    cleaning = result.get("cleaning") or {}

    if not cleaning:
        render_page_header(
            title="Cleaning",
            subtitle=(
                "Review the transformations applied to "
                "the dataset."
            ),
        )

        st.warning(
            "Cleaning results are not available."
        )
        return

    # ========================================================
    # RAW CLEANING RESULT
    # ========================================================

    original_row_count = cleaning.get(
        "original_row_count",
        0,
    )

    cleaned_row_count = cleaning.get(
        "cleaned_row_count",
        0,
    )

    duplicates_removed = cleaning.get(
        "duplicates_removed",
        0,
    )

    missing_before = cleaning.get(
        "missing_values_before",
        0,
    )

    missing_after = cleaning.get(
        "missing_values_after",
        0,
    )

    duplicate_rows_after = cleaning.get(
        "duplicate_rows_after",
        0,
    )

    quality_before = cleaning.get(
        "quality_score_before"
    )

    quality_after = cleaning.get(
        "quality_score_after"
    )

    outliers_before = cleaning.get(
        "outliers_before",
        {},
    ) or {}

    outliers_after = cleaning.get(
        "outliers_after",
        {},
    ) or {}

    actions = cleaning.get(
        "actions",
        [],
    ) or []

    cleaned_dataset_path = cleaning.get(
        "cleaned_dataset_path"
    )

    # ========================================================
    # DERIVED INFORMATION
    # ========================================================

    affected_columns = _get_affected_columns(
        actions
    )

    dataset_operations = _get_dataset_operations(
        actions
    )

    action_rows = _build_action_rows(
        actions
    )

    before_outlier_map = _get_outlier_map(
        outliers_before
    )

    after_outlier_map = _get_outlier_map(
        outliers_after
    )

    before_outlier_rows = _build_outlier_rows(
        before_outlier_map
    )

    after_outlier_rows = _build_outlier_rows(
        after_outlier_map
    )

    outlier_total_before = outliers_before.get(
        "total_outliers",
        0,
    )

    outlier_total_after = outliers_after.get(
        "total_outliers",
        0,
    )

    # ========================================================
    # PAGE HEADER
    # ========================================================

    render_page_header(
        title="Cleaning",
        subtitle=(
            "Review what the platform changed to improve "
            "the quality and consistency of the dataset."
        ),
    )

    # ========================================================
    # CLEANING RESULT
    # ========================================================

    st.markdown("### Cleaning result")

    if (
        quality_before is not None
        and quality_after is not None
    ):
        quality_change = (
            float(quality_after)
            - float(quality_before)
        )

        quality_columns = st.columns(2)

        with quality_columns[0]:
            metric_card(
                label="Before Cleaning",
                value=_format_percentage(
                    quality_before
                ),
                description=(
                    "Overall dataset quality before "
                    "cleaning."
                ),
                accent="primary",
            )

        with quality_columns[1]:
            metric_card(
                label="After Cleaning",
                value=_format_percentage(
                    quality_after
                ),
                description=(
                    "Overall dataset quality after "
                    "cleaning."
                ),
                accent="success",
            )

        if quality_change > 0:
            st.success(
                f"Quality improved by "
                f"**{quality_change:.2f} percentage points**."
            )

        elif quality_change < 0:
            st.warning(
                f"Quality changed by "
                f"**{quality_change:.2f} percentage points**."
            )

        else:
            st.info(
                "The overall quality score did not change."
            )

    else:
        st.info(
            "Quality score comparison is unavailable."
        )

    # ========================================================
    # DATASET CHANGES
    # ========================================================

    st.markdown("### Dataset changes")

    row_columns = st.columns(3)

    with row_columns[0]:
        metric_card(
            label="Original Rows",
            value=_format_number(
                original_row_count
            ),
            description=(
                "Rows before the cleaning process."
            ),
            accent="primary",
        )

    with row_columns[1]:
        metric_card(
            label="Cleaned Rows",
            value=_format_number(
                cleaned_row_count
            ),
            description=(
                "Rows remaining after cleaning."
            ),
            accent="success",
        )

    with row_columns[2]:
        rows_removed = max(
            int(original_row_count or 0)
            - int(cleaned_row_count or 0),
            0,
        )

        metric_card(
            label="Rows Removed",
            value=_format_number(
                rows_removed
            ),
            description=(
                "Total rows removed during cleaning."
            ),
            accent="primary",
        )

    # ========================================================
    # QUALITY CHANGES
    # ========================================================

    st.markdown("### Quality changes")

    quality_columns = st.columns(3)

    with quality_columns[0]:
        metric_card(
            label="Missing Values",
            value=(
                f"{_format_number(missing_before)}"
                f" → "
                f"{_format_number(missing_after)}"
            ),
            description=(
                "Missing cells before and after cleaning."
            ),
            status=(
                "Resolved"
                if int(missing_after or 0) == 0
                else "Remaining"
            ),
            accent=(
                "success"
                if int(missing_after or 0) == 0
                else "primary"
            ),
        )

    with quality_columns[1]:
        metric_card(
            label="Duplicate Rows",
            value=(
                f"{_format_number(duplicates_removed)}"
                f" → "
                f"{_format_number(duplicate_rows_after)}"
            ),
            description=(
                "Duplicate rows before and after cleaning."
            ),
            status=(
                "Resolved"
                if int(duplicate_rows_after or 0) == 0
                else "Remaining"
            ),
            accent=(
                "success"
                if int(duplicate_rows_after or 0) == 0
                else "primary"
            ),
        )

    with quality_columns[2]:
        metric_card(
            label="Outliers",
            value=(
                f"{_format_number(outlier_total_before)}"
                f" → "
                f"{_format_number(outlier_total_after)}"
            ),
            description=(
                "Detected statistical outliers before "
                "and after cleaning."
            ),
            accent="primary",
        )

    # ========================================================
    # OUTLIER CHANGES
    # ========================================================

    if (
        before_outlier_rows
        or after_outlier_rows
    ):
        st.markdown("### Outlier changes")

        outlier_columns = st.columns(2)

        with outlier_columns[0]:
            st.markdown("**Before cleaning**")

            if before_outlier_rows:
                st.dataframe(
                    before_outlier_rows,
                    width="stretch",
                    hide_index=True,
                )
            else:
                st.info(
                    "No statistical outliers were detected."
                )

        with outlier_columns[1]:
            st.markdown("**After cleaning**")

            if after_outlier_rows:
                st.dataframe(
                    after_outlier_rows,
                    width="stretch",
                    hide_index=True,
                )
            else:
                st.success(
                    "No statistical outliers remain."
                )

        # ----------------------------------------------------
        # DATA-DRIVEN OUTLIER INTERPRETATION
        # ----------------------------------------------------

        changed_columns = []

        all_outlier_columns = set(
            before_outlier_map
        ) | set(
            after_outlier_map
        )

        for column in all_outlier_columns:
            before_count = int(
                before_outlier_map.get(
                    column,
                    0,
                )
                or 0
            )

            after_count = int(
                after_outlier_map.get(
                    column,
                    0,
                )
                or 0
            )

            if before_count != after_count:
                changed_columns.append(
                    (
                        column,
                        before_count,
                        after_count,
                    )
                )

        changed_columns.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        if changed_columns:
            st.markdown("**Outlier changes by column**")

            change_rows = []

            for (
                column,
                before_count,
                after_count,
            ) in changed_columns:
                change_rows.append(
                    {
                        "Column": column,
                        "Before": _format_number(
                            before_count
                        ),
                        "After": _format_number(
                            after_count
                        ),
                        "Change": _format_number(
                            after_count
                            - before_count
                        ),
                    }
                )

            st.dataframe(
                change_rows,
                width="stretch",
                hide_index=True,
            )

    # ========================================================
    # CLEANING ACTIONS
    # ========================================================

    st.markdown("### Cleaning actions")

    if action_rows:
        st.dataframe(
            action_rows,
            width="stretch",
            hide_index=True,
        )

        st.caption(
            "Each row represents a transformation recorded "
            "by the cleaning pipeline."
        )
    else:
        st.info(
            "No cleaning actions were recorded."
        )

    # ========================================================
    # AFFECTED COLUMNS
    # ========================================================

    if affected_columns:
        st.markdown("### Columns affected")

        st.info(
            f"The cleaning process applied transformations "
            f"to **{_format_number(len(affected_columns))} "
            f"columns**."
        )

        affected_rows = [
            {
                "Column": column
            }
            for column in affected_columns
        ]

        st.dataframe(
            affected_rows,
            width="stretch",
            hide_index=True,
        )

    # ========================================================
    # DATASET-LEVEL OPERATIONS
    # ========================================================

    if dataset_operations:
        st.markdown("### Dataset-level operations")

        operation_rows = []

        for operation in dataset_operations:
            operation_rows.append(
                {
                    "Operation": _format_strategy(
                        operation.get("strategy")
                    ),
                    "Rows Affected": _format_number(
                        operation.get(
                            "values_replaced"
                        )
                    ),
                }
            )

        st.dataframe(
            operation_rows,
            width="stretch",
            hide_index=True,
        )

        st.caption(
            "These operations affect the dataset as a whole "
            "rather than a specific column."
        )

    # ========================================================
    # CLEANING SUMMARY
    # ========================================================

    st.markdown("### Cleaning summary")

    summary_messages = []

    if int(missing_before or 0) > int(
        missing_after or 0
    ):
        summary_messages.append(
            f"Missing values were reduced from "
            f"**{_format_number(missing_before)}** "
            f"to **{_format_number(missing_after)}**."
        )

    if int(duplicates_removed or 0) > 0:
        summary_messages.append(
            f"**{_format_number(duplicates_removed)}** "
            f"duplicate rows were removed."
        )

    if int(outlier_total_before or 0) > int(
        outlier_total_after or 0
    ):
        outlier_reduction = (
            int(outlier_total_before or 0)
            - int(outlier_total_after or 0)
        )

        summary_messages.append(
            f"Detected outliers were reduced by "
            f"**{_format_number(outlier_reduction)}**."
        )

    if quality_before is not None and quality_after is not None:
        quality_change = (
            float(quality_after)
            - float(quality_before)
        )

        if quality_change > 0:
            summary_messages.append(
                f"Overall quality increased from "
                f"**{_format_percentage(quality_before)}** "
                f"to **{_format_percentage(quality_after)}**."
            )

    if summary_messages:
        summary_columns = st.columns(
            min(len(summary_messages), 3)
        )

        for index, message in enumerate(
            summary_messages
        ):
            with summary_columns[
                index % len(summary_columns)
            ]:
                st.info(message)
    else:
        st.info(
            "No measurable cleaning changes were recorded."
        )

    # ========================================================
    # CLEANED DATASET
    # ========================================================

    if cleaned_dataset_path:
        st.markdown("### Cleaned dataset")

        st.caption(
            "The platform generated this cleaned dataset "
            "for downstream analytics and machine learning."
        )

        st.code(
            cleaned_dataset_path,
            language="text",
        )

    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown("---")

    st.caption(
        "This page describes transformations performed by "
        "the cleaning pipeline. Analytics and Machine Learning "
        "use the resulting cleaned dataset."
    )