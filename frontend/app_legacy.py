"""Product-oriented Streamlit interface for automated analysis."""

import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Intelligent Analytics Platform",
    layout="wide",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>
    .metric-card {
        padding: 12px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        background-color: rgba(128, 128, 128, 0.05);
    }

    .insight-card {
        padding: 18px;
        margin-bottom: 14px;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        background-color: rgba(128, 128, 128, 0.05);
    }

    .insight-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .insight-description {
        font-size: 15px;
        line-height: 1.5;
    }

    .insight-meta {
        font-size: 12px;
        opacity: 0.75;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def render_kpi(label: str, value) -> None:
    """Render a KPI metric."""
    st.metric(
        label=label,
        value=value,
    )


def render_section_title(title: str) -> None:
    """Render a consistent section title."""
    st.markdown(
        f"### {title}"
    )


def render_quality_gauge(score: float) -> None:
    """Render the overall data quality score."""
    fig = px.pie(
        values=[
            max(score, 0),
            max(100 - score, 0),
        ],
        names=[
            "Quality",
            "Remaining",
        ],
        hole=0.72,
    )

    fig.update_traces(
        textinfo="none",
    )

    fig.update_layout(
        height=300,
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        annotations=[
            dict(
                text=f"{score:.1f}",
                x=0.5,
                y=0.5,
                font=dict(
                    size=32,
                ),
                showarrow=False,
            )
        ],
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


def create_dashboard_chart(chart: dict) -> None:
    """Render dashboard charts using the dashboard payload."""

    data = chart.get(
        "data",
        {},
    )

    chart_type = chart.get(
        "chart_type",
        "bar",
    )

    x = data.get(
        "x",
        [],
    )

    y = data.get(
        "y",
        [],
    )

    x_axis = data.get(
        "x_axis",
        "Category",
    )

    y_axis = data.get(
        "y_axis",
        "Value",
    )

    title = chart.get(
        "title",
        "Chart",
    )

    chart_df = pd.DataFrame(
        {
            x_axis: x,
            y_axis: y,
        }
    )

    if chart_df.empty:
        st.info(
            f"No data available for {title}."
        )
        return

    if chart_type == "line":

        fig = px.line(
            chart_df,
            x=x_axis,
            y=y_axis,
            title=title,
            labels={
                x_axis: x_axis,
                y_axis: y_axis,
            },
            markers=True,
        )

    elif chart_type == "scatter":

        fig = px.scatter(
            chart_df,
            x=x_axis,
            y=y_axis,
            title=title,
            labels={
                x_axis: x_axis,
                y_axis: y_axis,
            },
        )

    else:

        fig = px.bar(
            chart_df,
            x=x_axis,
            y=y_axis,
            title=title,
            labels={
                x_axis: x_axis,
                y_axis: y_axis,
            },
        )

    fig.update_layout(
        height=420,
        margin=dict(
            l=40,
            r=40,
            t=70,
            b=80,
        ),
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "Intelligent Analytics Platform"
)

st.write(
    "Upload a business dataset and let the platform "
    "automatically clean, analyze, model, and explain it."
)


# ============================================================
# API CONFIGURATION
# ============================================================

api_url = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


# ============================================================
# FILE UPLOAD
# ============================================================

file = st.file_uploader(
    "Upload CSV or Excel dataset",
    type=[
        "csv",
        "xlsx",
        "xls",
    ],
)


# ============================================================
# RUN COMPLETE ANALYSIS
# ============================================================

if st.button(
    "Run Complete Analysis",
    type="primary",
    disabled=file is None,
):

    with st.status(
        "Running complete analysis...",
        expanded=True,
    ) as status:

        st.write(
            "Uploading dataset and assessing data quality"
        )

        try:

            response = requests.post(
                f"{api_url}/analysis/run",
                data={},
                files={
                    "file": (
                        file.name,
                        file.getvalue(),
                        file.type
                        or "application/octet-stream",
                    )
                },
                timeout=300,
            )

            response.raise_for_status()

            st.session_state.result = (
                response.json()
            )

            status.update(
                label="Analysis completed",
                state="complete",
            )

        except requests.RequestException as exc:

            status.update(
                label="Analysis failed",
                state="error",
            )

            st.error(
                str(exc)
            )


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.get(
    "result"
)


if result:

    # ========================================================
    # TOP-LEVEL DATA
    # ========================================================

    quality = result[
        "etl"
    ][
        "quality"
    ]

    summary = result[
        "analytics"
    ][
        "statistics"
    ][
        "dataset_summary"
    ]


    # ========================================================
    # TOP KPI CARDS
    # ========================================================

    cols = st.columns(4)

    cols[0].metric(
        "Quality score",
        f"{quality['quality_score']:.1f}",
    )

    cols[1].metric(
        "Rows",
        summary["total_rows"],
    )

    cols[2].metric(
        "Columns",
        summary["total_columns"],
    )

    cols[3].metric(
        "Missing values",
        result[
            "etl"
        ][
            "missing_values"
        ][
            "total_missing_values"
        ],
    )


    # ========================================================
    # TABS
    # ========================================================

    tabs = st.tabs(
        [
            "Dashboard",
            "Data Quality",
            "Data Profile",
            "Cleaning",
            "Analytics",
            "Machine Learning",
            "Business Insights",
        ]
    )


    # ========================================================
    # DASHBOARD
    # ========================================================

    with tabs[0]:

        render_section_title(
            "Business Dashboard"
        )

        dashboard = result.get(
            "dashboard",
            {},
        )

        charts = dashboard.get(
            "charts",
            [],
        )

        if charts:

            for chart in charts:

                create_dashboard_chart(
                    chart
                )

        else:

            st.info(
                "No dashboard charts are available."
            )


    # ========================================================
    # DATA QUALITY
    # ========================================================

    with tabs[1]:

        render_section_title(
            "Overall Data Quality"
        )

        quality_columns = st.columns(
            2
        )

        with quality_columns[0]:

            render_quality_gauge(
                float(
                    quality[
                        "quality_score"
                    ]
                )
            )

        with quality_columns[1]:

            render_kpi(
                "Quality Score",
                f"{quality['quality_score']:.2f}",
            )

            render_kpi(
                "Missing Value Penalty",
                f"{quality['missing_penalty']:.2f}",
            )

            render_kpi(
                "Duplicate Penalty",
                f"{quality['duplicate_penalty']:.2f}",
            )

            render_kpi(
                "Outlier Penalty",
                f"{quality['outlier_penalty']:.2f}",
            )


        st.divider()


        render_section_title(
            "Missing Values"
        )

        missing_values = result[
            "etl"
        ][
            "missing_values"
        ]

        missing_by_column = missing_values.get(
            "missing_by_column",
            {},
        )

        if missing_by_column:

            missing_df = pd.DataFrame(
                list(
                    missing_by_column.items()
                ),
                columns=[
                    "Column",
                    "Missing Values",
                ],
            )

            st.dataframe(
                missing_df,
                width="stretch",
                hide_index=True,
            )

        else:

            st.success(
                "No missing values detected."
            )


        st.divider()


        render_section_title(
            "Duplicates"
        )

        duplicates = result[
            "etl"
        ][
            "duplicates"
        ]

        duplicate_cols = st.columns(
            2
        )

        duplicate_cols[0].metric(
            "Duplicate Rows",
            duplicates.get(
                "duplicate_rows",
                0,
            ),
        )

        duplicate_cols[1].metric(
            "Duplicate Percentage",
            f"{duplicates.get('duplicate_percentage', 0):.2f}%",
        )


        st.divider()


        render_section_title(
            "Outliers"
        )

        outliers = result[
            "etl"
        ][
            "outliers"
        ]

        outlier_cols = st.columns(
            2
        )

        outlier_cols[0].metric(
            "Total Outliers",
            outliers.get(
                "total_outliers",
                0,
            ),
        )

        outlier_cols[1].metric(
            "Columns With Outliers",
            len(
                outliers.get(
                    "outliers_by_column",
                    {},
                )
            ),
        )

        outlier_by_column = outliers.get(
            "outliers_by_column",
            {},
        )

        if outlier_by_column:

            outlier_df = pd.DataFrame(
                list(
                    outlier_by_column.items()
                ),
                columns=[
                    "Column",
                    "Outliers",
                ],
            )

            st.dataframe(
                outlier_df,
                width="stretch",
                hide_index=True,
            )


    # ========================================================
    # DATA PROFILE
    # ========================================================

    with tabs[2]:

        render_section_title(
            "Schema Profile"
        )

        schema_columns = result[
            "etl"
        ][
            "schema_profile"
        ][
            "columns"
        ]

        schema_df = pd.DataFrame(
            schema_columns
        )

        st.dataframe(
            schema_df,
            width="stretch",
            hide_index=True,
        )


        st.divider()


        render_section_title(
            "Dataset Summary"
        )

        profile_cols = st.columns(
            5
        )

        profile_cols[0].metric(
            "Rows",
            summary[
                "total_rows"
            ],
        )

        profile_cols[1].metric(
            "Columns",
            summary[
                "total_columns"
            ],
        )

        profile_cols[2].metric(
            "Numeric",
            summary[
                "numeric_columns"
            ],
        )

        profile_cols[3].metric(
            "Categorical",
            summary[
                "categorical_columns"
            ],
        )

        profile_cols[4].metric(
            "Datetime",
            summary[
                "datetime_columns"
            ],
        )


    # ========================================================
    # CLEANING
    # ========================================================

    with tabs[3]:

        cleaning = result.get(
            "cleaning"
        )

        if cleaning:

            render_section_title(
                "Cleaning Summary"
            )

            cleaning_cols = st.columns(
                4
            )

            cleaning_cols[0].metric(
                "Original Rows",
                cleaning.get(
                    "original_row_count",
                    0,
                ),
            )

            cleaning_cols[1].metric(
                "Cleaned Rows",
                cleaning.get(
                    "cleaned_row_count",
                    0,
                ),
            )

            cleaning_cols[2].metric(
                "Missing Before",
                cleaning.get(
                    "missing_values_before",
                    0,
                ),
            )

            cleaning_cols[3].metric(
                "Missing After",
                cleaning.get(
                    "missing_values_after",
                    0,
                ),
            )


            st.divider()


            render_section_title(
                "Cleaning Actions"
            )

            actions = cleaning.get(
                "actions",
                [],
            )

            if actions:

                actions_df = pd.DataFrame(
                    actions
                )

                st.dataframe(
                    actions_df,
                    width="stretch",
                    hide_index=True,
                )

            else:

                st.success(
                    "No cleaning actions were required."
                )


            st.divider()


            render_section_title(
                "Cleaning Details"
            )

            st.write(
                f"Duplicates removed: "
                f"**{cleaning.get('duplicates_removed', 0):,}**"
            )

            st.write(
                f"Duplicate rows after cleaning: "
                f"**{cleaning.get('duplicate_rows_after', 0):,}**"
            )

            st.write(
                f"Quality score after cleaning: "
                f"**{cleaning.get('quality_score_after', 0):.2f}**"
            )

            st.write(
                f"Columns affected: "
                f"**{len(cleaning.get('columns_affected', []))}**"
            )

        else:

            st.info(
                "Cleaning information is not available."
            )


    # ========================================================
    # ANALYTICS
    # ========================================================

    with tabs[4]:

        analytics = result[
            "analytics"
        ]


        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        statistics = analytics.get(
            "statistics",
            {},
        )

        dataset_summary = statistics.get(
            "dataset_summary",
            {},
        )

        render_section_title(
            "Dataset Summary"
        )

        summary_cols = st.columns(
            5
        )

        summary_cols[0].metric(
            "Rows",
            dataset_summary.get(
                "total_rows",
                0,
            ),
        )

        summary_cols[1].metric(
            "Columns",
            dataset_summary.get(
                "total_columns",
                0,
            ),
        )

        summary_cols[2].metric(
            "Numerical",
            dataset_summary.get(
                "numeric_columns",
                0,
            ),
        )

        summary_cols[3].metric(
            "Categorical",
            dataset_summary.get(
                "categorical_columns",
                0,
            ),
        )

        summary_cols[4].metric(
            "Datetime",
            dataset_summary.get(
                "datetime_columns",
                0,
            ),
        )


        # ----------------------------------------------------
        # NUMERICAL STATISTICS
        # ----------------------------------------------------

        numeric_statistics = statistics.get(
            "numeric_statistics",
            [],
        )

        if numeric_statistics:

            render_section_title(
                "Numerical Statistics"
            )

            numeric_df = pd.DataFrame(
                numeric_statistics
            )

            st.dataframe(
                numeric_df,
                width="stretch",
                hide_index=True,
            )


        # ----------------------------------------------------
        # CATEGORICAL STATISTICS
        # ----------------------------------------------------

        categorical_statistics = statistics.get(
            "categorical_statistics",
            [],
        )

        if categorical_statistics:

            render_section_title(
                "Categorical Statistics"
            )

            categorical_df = pd.DataFrame(
                categorical_statistics
            )

            st.dataframe(
                categorical_df,
                width="stretch",
                hide_index=True,
            )


        # ----------------------------------------------------
        # CORRELATIONS
        # ----------------------------------------------------

        correlations = analytics.get(
            "correlations",
            {},
        ).get(
            "correlations",
            [],
        )

        if correlations:

            render_section_title(
                "Correlations"
            )

            correlation_df = pd.DataFrame(
                correlations
            )

            st.dataframe(
                correlation_df,
                width="stretch",
                hide_index=True,
            )


        # ----------------------------------------------------
        # TRENDS
        # ----------------------------------------------------

        trends = analytics.get(
            "trends",
            {},
        ).get(
            "trends",
            [],
        )

        if trends:

            render_section_title(
                "Trends"
            )

            trend_df = pd.DataFrame(
                trends
            )

            st.dataframe(
                trend_df,
                width="stretch",
                hide_index=True,
            )


        # ----------------------------------------------------
        # SEGMENTATION
        # ----------------------------------------------------

        segments = analytics.get(
            "segmentation",
            {},
        ).get(
            "segments",
            [],
        )

        if segments:

            render_section_title(
                "Segmentation"
            )

            st.caption(
                "Distribution of records across categorical values."
            )

            segment_df = pd.DataFrame(
                segments
            )

            # ------------------------------------------------
            # SEGMENTATION SUMMARY
            # ------------------------------------------------

            segmentation_columns = (
                segment_df[
                    "column_name"
                ]
                .nunique()
            )

            total_segments = len(
                segment_df
            )

            segmentation_cols = st.columns(
                2
            )

            segmentation_cols[0].metric(
                "Categorical Columns",
                segmentation_columns,
            )

            segmentation_cols[1].metric(
                "Segments Analyzed",
                total_segments,
            )

            st.divider()

            # ------------------------------------------------
            # DISPLAY EACH CATEGORICAL COLUMN
            # ------------------------------------------------

            for column_name in (
                segment_df[
                    "column_name"
                ]
                .dropna()
                .drop_duplicates()
            ):

                column_segments = (
                    segment_df[
                        segment_df[
                            "column_name"
                        ]
                        == column_name
                    ]
                    .copy()
                    .sort_values(
                        "count",
                        ascending=False,
                    )
                )

                if column_segments.empty:
                    continue

                st.markdown(
                    f"#### {column_name.title()}"
                )

                # --------------------------------------------
                # TOP CATEGORY INSIGHT
                # --------------------------------------------

                top_segment = (
                    column_segments.iloc[0]
                )

                top_category = (
                    top_segment[
                        "category"
                    ]
                )

                top_count = int(
                    top_segment[
                        "count"
                    ]
                )

                top_percentage = float(
                    top_segment[
                        "percentage"
                    ]
                )

                st.info(
                    f"**{top_category}** is the largest "
                    f"category, representing "
                    f"**{top_percentage:.2f}%** of records "
                    f"({top_count:,} records)."
                )

                # --------------------------------------------
                # TOP 10 CATEGORY TABLE
                # --------------------------------------------

                display_df = (
                    column_segments[
                        [
                            "category",
                            "count",
                            "percentage",
                        ]
                    ]
                    .head(10)
                    .copy()
                )

                display_df.columns = [
                    "Category",
                    "Records",
                    "Percentage",
                ]

                display_df[
                    "Records"
                ] = display_df[
                    "Records"
                ].astype(int)

                display_df[
                    "Records"
                ] = display_df[
                    "Records"
                ].map(
                    lambda value: f"{value:,}"
                )

                display_df[
                    "Percentage"
                ] = display_df[
                    "Percentage"
                ].map(
                    lambda value: f"{float(value):.2f}%"
                )

                st.dataframe(
                    display_df,
                    width="stretch",
                    hide_index=True,
                )

                # --------------------------------------------
                # TOP 10 CATEGORY CHART
                # --------------------------------------------

                chart_df = (
                    column_segments[
                        [
                            "category",
                            "count",
                        ]
                    ]
                    .head(10)
                    .copy()
                )

                fig = px.bar(
                    chart_df,
                    x="category",
                    y="count",
                    title=(
                        f"Top Categories in "
                        f"{column_name.title()}"
                    ),
                    labels={
                        "category": "Category",
                        "count": "Records",
                    },
                )

                fig.update_layout(
                    height=400,
                    showlegend=False,
                    margin=dict(
                        l=40,
                        r=40,
                        t=70,
                        b=80,
                    ),
                )

                st.plotly_chart(
                    fig,
                    width="stretch",
                )

                st.divider()

        else:

            st.info(
                "No categorical segmentation results are available."
            )


    # ========================================================
    # MACHINE LEARNING
    # ========================================================

    with tabs[5]:

        ml = result.get(
            "ml"
        )

        if not ml:

            st.info(
                "ML was not run."
            )

        else:

            render_section_title(
                "Machine Learning Summary"
            )

            ml_cols = st.columns(
                4
            )

            ml_cols[0].metric(
                "Task Type",
                ml.get(
                    "task_type"
                )
                or "N/A",
            )

            ml_cols[1].metric(
                "Models Trained",
                ml.get(
                    "models_trained",
                    0,
                ),
            )

            ml_cols[2].metric(
                "Training Rows",
                ml.get(
                    "training_rows",
                    0,
                ),
            )

            ml_cols[3].metric(
                "Testing Rows",
                ml.get(
                    "testing_rows",
                    0,
                ),
            )


            evaluations = ml.get(
                "evaluations",
                [],
            )

            if evaluations:

                st.divider()

                render_section_title(
                    "Model Comparison"
                )

                evaluation_rows = []

                for evaluation in evaluations:

                    row = {
                        "Model": evaluation.get(
                            "estimator",
                            "Unknown",
                        ),
                        "Training Time": evaluation.get(
                            "training_time",
                            0,
                        ),
                    }

                    metrics = evaluation.get(
                        "metrics",
                        {},
                    )

                    for metric_name, metric_value in metrics.items():

                        if isinstance(
                            metric_value,
                            (int, float),
                        ):

                            row[
                                metric_name
                            ] = metric_value

                    evaluation_rows.append(
                        row
                    )

                evaluation_df = pd.DataFrame(
                    evaluation_rows
                )

                st.dataframe(
                    evaluation_df,
                    width="stretch",
                    hide_index=True,
                )


            best_model = ml.get(
                "best_model"
            )

            if best_model:

                st.divider()

                render_section_title(
                    "Best Model"
                )

                best_cols = st.columns(
                    2
                )

                best_cols[0].metric(
                    "Model",
                    best_model.get(
                        "estimator",
                        "Unknown",
                    ),
                )

                best_metrics = best_model.get(
                    "metrics",
                    {},
                )

                prominent_metrics = {
                    name: value
                    for name, value in best_metrics.items()
                    if str(name).strip().lower()
                    not in {"mse", "mean_squared_error"}
                }

                best_cols[1].write(
                    prominent_metrics
                )

                with st.expander("Technical Details"):
                    st.json(best_metrics)


    # ========================================================
    # BUSINESS INSIGHTS
    # ========================================================

    with tabs[6]:

        analytics = result[
            "analytics"
        ]

        insights = analytics.get(
            "insights",
            {},
        ).get(
            "insights",
            [],
        )

        render_section_title(
            "Executive Summary"
        )

        st.write(
            f"The cleaned dataset contains "
            f"{summary['total_rows']:,} records "
            f"and has a quality score of "
            f"{quality['quality_score']:.1f}."
        )

        if insights:

            render_section_title(
                "Key Findings"
            )

            for insight in insights:

                title = insight.get(
                    "title",
                    "Insight",
                )

                description = insight.get(
                    "description",
                    "",
                )

                category = insight.get(
                    "category",
                    "general",
                )

                severity = insight.get(
                    "severity",
                    "info",
                )

                st.markdown(
                    f"""
                    <div class="insight-card">

                        <div class="insight-title">
                            {title}
                        </div>

                        <div class="insight-description">
                            {description}
                        </div>

                        <div class="insight-meta">
                            Category: {category}
                            &nbsp;&nbsp;|&nbsp;&nbsp;
                            Severity: {severity}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:

            st.info(
                "No business insights are available."
            )


        # ----------------------------------------------------
        # TECHNICAL DETAILS
        # ----------------------------------------------------

        with st.expander(
            "Technical Details"
        ):

            st.json(
                {
                    "analytics": analytics,
                    "ml": result.get(
                        "ml"
                    ),
                    "dashboard": result.get(
                        "dashboard"
                    ),
                }
            )
