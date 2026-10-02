"""
Intelligent Analytics Platform
Analytics view.

Focuses on interpreting patterns discovered in the cleaned
dataset rather than repeating Data Quality or Cleaning results.
"""

import streamlit as st

from components.layout import render_page_header
from components.metrics import metric_card


# ============================================================
# HELPERS
# ============================================================

def _format_number(value, decimals=0) -> str:
    """Format a numeric value for display."""
    if value is None:
        return "—"

    try:
        number = float(value)

        if decimals == 0:
            return f"{int(number):,}"

        return f"{number:,.{decimals}f}"

    except (TypeError, ValueError):
        return str(value)


def _format_percentage(value, decimals=1) -> str:
    """Format a percentage value."""
    if value is None:
        return "—"

    try:
        return f"{float(value):.{decimals}f}%"
    except (TypeError, ValueError):
        return str(value)


def _safe_list(value) -> list:
    """Return a list when the value is a list."""
    return value if isinstance(value, list) else []


def _safe_dict(value) -> dict:
    """Return a dictionary when the value is a dictionary."""
    return value if isinstance(value, dict) else {}


def _get_statistics(analytics: dict) -> dict:
    """Extract statistical results."""
    return _safe_dict(
        analytics.get("statistics")
    )


def _get_numeric_statistics(analytics: dict) -> list:
    """Extract numeric statistics."""
    statistics = _get_statistics(analytics)

    return _safe_list(
        statistics.get("numeric_statistics")
    )


def _get_categorical_statistics(analytics: dict) -> list:
    """Extract categorical statistics."""
    statistics = _get_statistics(analytics)

    for key in (
        "categorical_statistics",
        "categorical",
    ):
        value = statistics.get(key)

        if isinstance(value, list):
            return value

    return []


def _get_correlations(analytics: dict) -> list:
    """
    Extract correlation records.

    Supports both:
        {"correlations": [...]}

    and:
        [...]

    Also handles alternative wrapper names defensively.
    """
    correlations = analytics.get("correlations")

    if isinstance(correlations, list):
        return correlations

    if not isinstance(correlations, dict):
        return []

    for key in (
        "correlations",
        "results",
        "items",
        "data",
    ):
        value = correlations.get(key)

        if isinstance(value, list):
            return value

    return []


def _get_segments(analytics: dict) -> list:
    """Extract segmentation/category distribution records."""
    segmentation = analytics.get("segmentation")

    if isinstance(segmentation, list):
        return segmentation

    if not isinstance(segmentation, dict):
        return []

    for key in (
        "segments",
        "results",
        "items",
        "data",
    ):
        value = segmentation.get(key)

        if isinstance(value, list):
            return value

    return []


def _get_trends(analytics: dict) -> tuple:
    """Extract trend metadata and trend records."""
    trends = analytics.get("trends")

    if isinstance(trends, list):
        return None, trends

    if not isinstance(trends, dict):
        return None, []

    datetime_column = (
        trends.get("datetime_column")
        or trends.get("date_column")
        or trends.get("time_column")
    )

    trend_records = []

    for key in (
        "trends",
        "results",
        "items",
        "data",
    ):
        value = trends.get(key)

        if isinstance(value, list):
            trend_records = value
            break

    return datetime_column, trend_records


def _get_insights(analytics: dict) -> list:
    """Extract generated analytical insights."""
    insights = analytics.get("insights")

    if isinstance(insights, list):
        return insights

    if not isinstance(insights, dict):
        return []

    for key in (
        "insights",
        "results",
        "items",
        "data",
    ):
        value = insights.get(key)

        if isinstance(value, list):
            return value

    return []


def _get_column_name(item: dict) -> str | None:
    """Extract a column name from a record."""
    return (
        item.get("column_name")
        or item.get("column")
        or item.get("feature")
        or item.get("name")
    )


# ============================================================
# CORRELATION HELPERS
# ============================================================

def _get_correlation_columns(
    item: dict,
) -> tuple[str | None, str | None]:
    """
    Extract the two columns involved in a correlation.

    Supports several possible backend naming conventions.
    """

    column_1 = (
        item.get("column_1")
        or item.get("column_a")
        or item.get("feature_1")
        or item.get("feature_a")
        or item.get("column1")
        or item.get("first_column")
        or item.get("first")
    )

    column_2 = (
        item.get("column_2")
        or item.get("column_b")
        or item.get("feature_2")
        or item.get("feature_b")
        or item.get("column2")
        or item.get("second_column")
        or item.get("second")
    )

    # Support a nested pair such as:
    # {"columns": ["engine", "power"], ...}
    if (
        column_1 is None
        or column_2 is None
    ):
        columns = item.get("columns")

        if isinstance(columns, (list, tuple)):
            if len(columns) >= 2:
                column_1 = column_1 or columns[0]
                column_2 = column_2 or columns[1]

    # Support a nested features pair.
    if (
        column_1 is None
        or column_2 is None
    ):
        features = item.get("features")

        if isinstance(features, (list, tuple)):
            if len(features) >= 2:
                column_1 = column_1 or features[0]
                column_2 = column_2 or features[1]

    return column_1, column_2


def _get_correlation_value(
    item: dict,
):
    """Extract a correlation coefficient."""
    for key in (
        "correlation",
        "coefficient",
        "corr",
        "value",
        "score",
        "r",
    ):
        if key in item:
            return item.get(key)

    return None


def _build_correlation_findings(
    correlations: list,
) -> list:
    """
    Convert raw correlation records into meaningful
    relationship findings.
    """
    findings = []

    for item in correlations:
        if not isinstance(item, dict):
            continue

        column_1, column_2 = (
            _get_correlation_columns(item)
        )

        value = _get_correlation_value(item)

        if (
            column_1 is None
            or column_2 is None
            or value is None
        ):
            continue

        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            continue

        if numeric_value != numeric_value:
            continue

        findings.append(
            {
                "column_1": str(column_1),
                "column_2": str(column_2),
                "value": numeric_value,
            }
        )

    findings.sort(
        key=lambda item: abs(
            item["value"]
        ),
        reverse=True,
    )

    return findings


def _correlation_strength(
    value: float,
) -> str:
    """Classify correlation strength."""
    absolute_value = abs(value)

    if absolute_value >= 0.8:
        return "Very strong"

    if absolute_value >= 0.6:
        return "Strong"

    if absolute_value >= 0.4:
        return "Moderate"

    if absolute_value >= 0.2:
        return "Weak"

    return "Very weak"


def _correlation_direction(
    value: float,
) -> str:
    """Describe correlation direction."""
    if value > 0:
        return "positive"

    if value < 0:
        return "negative"

    return "neutral"


# ============================================================
# STATISTICAL PATTERN HELPERS
# ============================================================

def _build_distribution_findings(
    numeric_statistics: list,
) -> list:
    """
    Identify the strongest distribution patterns.

    Results are sorted by absolute skewness so the UI
    prioritizes the most meaningful patterns.
    """
    findings = []

    for item in numeric_statistics:
        if not isinstance(item, dict):
            continue

        column = _get_column_name(item)

        if not column:
            continue

        skewness = item.get("skewness")

        if skewness is None:
            continue

        try:
            skewness_value = float(skewness)
        except (TypeError, ValueError):
            continue

        if abs(skewness_value) < 0.5:
            continue

        if skewness_value >= 1:
            pattern = "Strong right-skew"

        elif skewness_value >= 0.5:
            pattern = "Moderate right-skew"

        elif skewness_value <= -1:
            pattern = "Strong left-skew"

        else:
            pattern = "Moderate left-skew"

        findings.append(
            {
                "column": str(column),
                "pattern": pattern,
                "skewness": skewness_value,
            }
        )

    findings.sort(
        key=lambda item: abs(
            item["skewness"]
        ),
        reverse=True,
    )

    return findings


# ============================================================
# CATEGORY HELPERS
# ============================================================

def _get_segment_fields(
    item: dict,
) -> tuple:
    """Extract common category distribution fields."""

    column = (
        item.get("column_name")
        or item.get("column")
        or item.get("feature")
    )

    value = (
        item.get("value")
        if item.get("value") is not None
        else item.get("segment")
    )

    if value is None:
        value = item.get("category")

    if value is None:
        value = item.get("label")

    count = None

    for key in (
        "count",
        "frequency",
        "records",
        "record_count",
    ):
        if key in item:
            count = item.get(key)
            break

    percentage = None

    for key in (
        "percentage",
        "share",
        "percent",
        "proportion",
    ):
        if key in item:
            percentage = item.get(key)
            break

    return (
        column,
        value,
        count,
        percentage,
    )


def _get_category_leaders(
    segments: list,
) -> dict:
    """
    Find the dominant category for every categorical
    column.
    """
    grouped = {}

    for item in segments:
        if not isinstance(item, dict):
            continue

        (
            column,
            value,
            count,
            percentage,
        ) = _get_segment_fields(item)

        if column is None or value is None:
            continue

        try:
            if percentage is not None:
                ranking_value = float(
                    percentage
                )
            elif count is not None:
                ranking_value = float(
                    count
                )
            else:
                ranking_value = 0
        except (TypeError, ValueError):
            ranking_value = 0

        current = grouped.get(column)

        if (
            current is None
            or ranking_value > current["ranking_value"]
        ):
            grouped[column] = {
                "value": value,
                "count": count,
                "percentage": percentage,
                "ranking_value": ranking_value,
            }

    return grouped


# ============================================================
# INSIGHT HELPERS
# ============================================================

def _extract_insight_text(
    item,
) -> str | None:
    """Extract readable text from an insight record."""

    if isinstance(item, str):
        return item.strip()

    if not isinstance(item, dict):
        return None

    for key in (
        "insight",
        "text",
        "description",
        "message",
        "finding",
        "summary",
    ):
        value = item.get(key)

        if value:
            return str(value).strip()

    return None


def _is_duplicate_insight(
    text: str,
    existing: list[str],
) -> bool:
    """
    Basic duplicate detection.

    This helps prevent backend-generated statistical
    findings from repeating findings already presented
    elsewhere on the page.
    """
    normalized = (
        text.lower()
        .replace(" ", "")
        .replace(".", "")
    )

    for existing_text in existing:
        existing_normalized = (
            existing_text.lower()
            .replace(" ", "")
            .replace(".", "")
        )

        if normalized == existing_normalized:
            return True

    return False


# ============================================================
# MAIN VIEW
# ============================================================

def render(result: dict) -> None:
    """Render the Analytics page."""

    analytics = _safe_dict(
        result.get("analytics")
    )

    render_page_header(
        title="Analytics",
        subtitle=(
            "Discover meaningful patterns, relationships, "
            "and distributions in the cleaned dataset."
        ),
    )

    if not analytics:
        st.warning(
            "Analytics results are not available."
        )
        return

    # ========================================================
    # EXTRACT RESULTS
    # ========================================================

    statistics = _get_statistics(
        analytics
    )

    numeric_statistics = (
        _get_numeric_statistics(
            analytics
        )
    )

    categorical_statistics = (
        _get_categorical_statistics(
            analytics
        )
    )

    correlations = _get_correlations(
        analytics
    )

    segments = _get_segments(
        analytics
    )

    datetime_column, trends = (
        _get_trends(analytics)
    )

    insights = _get_insights(
        analytics
    )

    dataset_summary = _safe_dict(
        statistics.get(
            "dataset_summary"
        )
    )

    # ========================================================
    # DATASET CONTEXT
    # ========================================================

    total_rows = dataset_summary.get(
        "total_rows"
    )

    total_columns = dataset_summary.get(
        "total_columns"
    )

    numeric_columns = dataset_summary.get(
        "numeric_columns"
    )

    categorical_columns = dataset_summary.get(
        "categorical_columns"
    )

    context_parts = []

    if total_rows is not None:
        context_parts.append(
            f"**{_format_number(total_rows)} rows**"
        )

    if total_columns is not None:
        context_parts.append(
            f"**{_format_number(total_columns)} columns**"
        )

    if numeric_columns is not None:
        context_parts.append(
            f"**{_format_number(numeric_columns)} numeric**"
        )

    if categorical_columns is not None:
        context_parts.append(
            f"**{_format_number(categorical_columns)} categorical**"
        )

    if context_parts:
        st.info(
            "Analysis is based on the cleaned dataset: "
            + " · ".join(context_parts)
            + "."
        )

    # ========================================================
    # STATISTICAL PATTERNS
    # ========================================================

    st.markdown("### Statistical patterns")

    distribution_findings = (
        _build_distribution_findings(
            numeric_statistics
        )
    )

    if distribution_findings:
        # Show only the strongest patterns in the main view.
        visible_patterns = (
            distribution_findings[:4]
        )

        columns = st.columns(
            min(
                len(visible_patterns),
                4,
            )
        )

        for index, finding in enumerate(
            visible_patterns
        ):
            with columns[index]:
                metric_card(
                    label=finding["column"],
                    value=finding["pattern"],
                    description=(
                        f"Skewness: "
                        f"{finding['skewness']:.2f}"
                    ),
                    accent="primary",
                )

        if len(distribution_findings) > 4:
            with st.expander(
                "View additional statistical patterns"
            ):
                additional_rows = []

                for finding in distribution_findings[4:]:
                    additional_rows.append(
                        {
                            "Column": finding[
                                "column"
                            ],
                            "Pattern": finding[
                                "pattern"
                            ],
                            "Skewness": (
                                f"{finding['skewness']:.2f}"
                            ),
                        }
                    )

                st.dataframe(
                    additional_rows,
                    width="stretch",
                    hide_index=True,
                )

    elif numeric_statistics:
        st.info(
            "Numeric columns were analyzed, but no "
            "significant distribution asymmetry was detected."
        )

    else:
        st.info(
            "No numeric statistical patterns are available."
        )

    # ========================================================
    # CATEGORY DISTRIBUTION
    # ========================================================

    st.markdown("### Category distribution")

    category_leaders = (
        _get_category_leaders(
            segments
        )
    )

    if category_leaders:
        category_rows = []

        for column, item in category_leaders.items():
            category_rows.append(
                {
                    "Category": str(column),
                    "Leading Value": str(
                        item["value"]
                    ),
                    "Records": (
                        _format_number(
                            item["count"]
                        )
                        if item["count"] is not None
                        else "—"
                    ),
                    "Share": (
                        _format_percentage(
                            item["percentage"]
                        )
                        if item["percentage"] is not None
                        else "—"
                    ),
                }
            )

        st.dataframe(
            category_rows,
            width="stretch",
            hide_index=True,
        )

        st.caption(
            "The leading value for each categorical column "
            "is shown to highlight category concentration."
        )

        with st.expander(
            "View detailed category distribution"
        ):
            detail_rows = []

            for item in segments:
                if not isinstance(item, dict):
                    continue

                (
                    column,
                    value,
                    count,
                    percentage,
                ) = _get_segment_fields(item)

                if column is None or value is None:
                    continue

                detail_rows.append(
                    {
                        "Category": str(column),
                        "Value": str(value),
                        "Records": (
                            _format_number(
                                count
                            )
                            if count is not None
                            else "—"
                        ),
                        "Share": (
                            _format_percentage(
                                percentage
                            )
                            if percentage is not None
                            else "—"
                        ),
                    }
                )

            if detail_rows:
                st.dataframe(
                    detail_rows,
                    width="stretch",
                    hide_index=True,
                )
            else:
                st.info(
                    "Detailed category distribution "
                    "is unavailable."
                )

    elif categorical_statistics:
        st.info(
            "Categorical columns were identified, but "
            "category distribution results are unavailable."
        )

    else:
        st.info(
            "No categorical distribution results are available."
        )

    # ========================================================
    # KEY RELATIONSHIPS
    # ========================================================

    st.markdown("### Key relationships")

    correlation_findings = (
        _build_correlation_findings(
            correlations
        )
    )

    if correlation_findings:
        visible_relationships = (
            correlation_findings[:5]
        )

        relationship_rows = []

        for item in visible_relationships:
            value = item["value"]

            relationship_rows.append(
                {
                    "Columns": (
                        f"{item['column_1']} ↔ "
                        f"{item['column_2']}"
                    ),
                    "Relationship": (
                        f"{_correlation_strength(value)} "
                        f"{_correlation_direction(value)}"
                    ),
                    "Correlation": (
                        f"{value:.2f}"
                    ),
                }
            )

        st.dataframe(
            relationship_rows,
            width="stretch",
            hide_index=True,
        )

        strongest = (
            correlation_findings[0]
        )

        strongest_value = strongest[
            "value"
        ]

        st.info(
            f"**Strongest relationship:** "
            f"{strongest['column_1']} and "
            f"{strongest['column_2']} show a "
            f"{_correlation_strength(strongest_value).lower()} "
            f"{_correlation_direction(strongest_value)} "
            f"relationship "
            f"(r = {strongest_value:.2f})."
        )

        if len(correlation_findings) > 5:
            with st.expander(
                "View all detected relationships"
            ):
                all_rows = []

                for item in correlation_findings:
                    value = item["value"]

                    all_rows.append(
                        {
                            "Column 1": item[
                                "column_1"
                            ],
                            "Column 2": item[
                                "column_2"
                            ],
                            "Correlation": (
                                f"{value:.2f}"
                            ),
                            "Strength": (
                                _correlation_strength(
                                    value
                                )
                            ),
                            "Direction": (
                                _correlation_direction(
                                    value
                                )
                            ),
                        }
                    )

                st.dataframe(
                    all_rows,
                    width="stretch",
                    hide_index=True,
                )

    else:
        st.info(
            "No meaningful correlation relationships "
            "are available."
        )

    # ========================================================
    # TRENDS
    # ========================================================

    st.markdown("### Trends")

    if trends:
        trend_rows = []

        for trend in trends:
            if isinstance(trend, dict):
                trend_rows.append(trend)

        if trend_rows:
            st.dataframe(
                trend_rows,
                width="stretch",
                hide_index=True,
            )
        else:
            st.info(
                "Trend analysis did not produce any "
                "interpretable observations."
            )

    elif datetime_column:
        st.info(
            f"A datetime column (`{datetime_column}`) "
            "was detected, but no trend observations "
            "were generated."
        )

    else:
        st.info(
            "No datetime column was detected. "
            "Time-based trend analysis is unavailable "
            "for this dataset."
        )

    # ========================================================
    # KEY ANALYTICAL FINDINGS
    # ========================================================

    st.markdown("### Key analytical findings")

    final_findings = []

    # --------------------------------------------------------
    # Strongest relationship
    # --------------------------------------------------------

    if correlation_findings:
        strongest = correlation_findings[0]
        value = strongest["value"]

        final_findings.append(
            (
                f"**Relationship:** "
                f"{strongest['column_1']} and "
                f"{strongest['column_2']} show a "
                f"{_correlation_strength(value).lower()} "
                f"{_correlation_direction(value)} relationship "
                f"(r = {value:.2f})."
            )
        )

    # --------------------------------------------------------
    # Second strongest relationship
    # --------------------------------------------------------

    if len(correlation_findings) > 1:
        second = correlation_findings[1]
        value = second["value"]

        final_findings.append(
            (
                f"**Relationship:** "
                f"{second['column_1']} and "
                f"{second['column_2']} show a "
                f"{_correlation_strength(value).lower()} "
                f"{_correlation_direction(value)} relationship "
                f"(r = {value:.2f})."
            )
        )

    # --------------------------------------------------------
    # Strongest distribution
    # --------------------------------------------------------

    if distribution_findings:
        strongest_distribution = (
            distribution_findings[0]
        )

        column = strongest_distribution[
            "column"
        ]

        pattern = strongest_distribution[
            "pattern"
        ]

        skewness = strongest_distribution[
            "skewness"
        ]

        final_findings.append(
            (
                f"**Distribution:** "
                f"`{column}` has the strongest detected "
                f"distribution asymmetry, showing "
                f"{pattern.lower()} "
                f"(skewness {skewness:.2f})."
            )
        )

    # --------------------------------------------------------
    # Category concentration
    # --------------------------------------------------------

    if category_leaders:
        dominant_category = max(
            category_leaders.items(),
            key=lambda item: item[1][
                "ranking_value"
            ],
        )

        category_name, category_data = (
            dominant_category
        )

        category_value = category_data[
            "value"
        ]

        category_percentage = (
            category_data["percentage"]
        )

        if category_percentage is not None:
            final_findings.append(
                (
                    f"**Category concentration:** "
                    f"`{category_value}` is the leading "
                    f"value in `{category_name}`, representing "
                    f"{_format_percentage(category_percentage)} "
                    f"of records."
                )
            )

    # --------------------------------------------------------
    # Backend-generated insights
    #
    # Only include insights that are not already represented
    # by the sections above.
    # --------------------------------------------------------

    for insight in insights:
        text = _extract_insight_text(
            insight
        )

        if not text:
            continue

        if _is_duplicate_insight(
            text,
            final_findings,
        ):
            continue

        # Avoid repeating generic dataset-size statements
        # already shown in the dataset context.
        lower_text = text.lower()

        if (
            "32,005" in text
            and "14 columns" in lower_text
        ):
            continue

        final_findings.append(text)

    # --------------------------------------------------------
    # Render only the strongest findings.
    # --------------------------------------------------------

    unique_findings = []

    for finding in final_findings:
        if finding not in unique_findings:
            unique_findings.append(
                finding
            )

    if unique_findings:
        for finding in unique_findings[:6]:
            st.info(finding)
    else:
        st.info(
            "No key analytical findings were generated."
        )

    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown("---")

    st.caption(
        "Analytics focuses on patterns, distributions, "
        "relationships, and trends discovered in the "
        "cleaned dataset. Data quality issues and cleaning "
        "transformations are covered in their respective "
        "workspaces."
    )