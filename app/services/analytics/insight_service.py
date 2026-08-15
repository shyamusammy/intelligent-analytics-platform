from app.core.enums import (
    CorrelationStrength,
    InsightCategory,
    InsightSeverity,
)

from app.schemas.analytics import (
    CorrelationResult,
    Insight,
    InsightResult,
    KPIResult,
    Segment,
    SegmentationResult,
    StatisticsResult,
    TrendResult,
    NumericColumnStatistics,
)


class InsightService:
    """
    Service responsible for converting analytical
    results into human-readable business insights.

    Responsibilities
    ----------------
    - Generate dataset insights
    - Generate statistical insights
    - Generate KPI insights
    - Generate correlation insights
    - Generate trend insights
    - Generate segmentation insights

    This service contains NO analytical calculations
    and NO persistence logic.
    """

    # ==========================================================
    # THRESHOLDS
    # ==========================================================

    STRONG_SKEWNESS_THRESHOLD = 1.0

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def run(
        self,
        statistics: StatisticsResult,
        kpis: KPIResult,
        correlations: CorrelationResult,
        trends: TrendResult,
        segmentation: SegmentationResult,
    ) -> InsightResult:
        """
        Generate business insights from analytical results.
        """

        insights: list[Insight] = []

        insights.extend(
            self._build_statistics_insights(
                statistics,
            )
        )

        insights.extend(
            self._build_kpi_insights(
                kpis,
            )
        )

        insights.extend(
            self._build_correlation_insights(
                correlations,
            )
        )

        insights.extend(
            self._build_trend_insights(
                trends,
            )
        )

        insights.extend(
            self._build_segmentation_insights(
                segmentation,
            )
        )

        return InsightResult(
            insights=insights,
        )

    # ==========================================================
    # STATISTICAL INSIGHTS
    # ==========================================================

    def _build_statistics_insights(
        self,
        statistics: StatisticsResult,
    ) -> list[Insight]:
        """
        Generate insights from numeric statistics.

        Statistical calculations are performed by
        StatisticsService. This method only interprets
        the resulting statistics.
        """

        insights: list[Insight] = []

        for metric in statistics.numeric_statistics:

            insights.extend(
                self._build_numeric_column_insights(
                    metric,
                )
            )

        return insights

    def _build_numeric_column_insights(
        self,
        metric: NumericColumnStatistics,
    ) -> list[Insight]:
        """
        Generate insights for an individual numeric column.
        """

        insights: list[Insight] = []

        # ------------------------------------------------------
        # Constant / No Variation
        # ------------------------------------------------------

        if metric.minimum == metric.maximum:

            insights.append(
                Insight(
                    title="No Variation",
                    description=(
                        f"{metric.column_name} has no variation "
                        f"across the dataset because all observed "
                        f"values are identical."
                    ),
                    category=InsightCategory.DATASET,
                    severity=InsightSeverity.MEDIUM,
                )
            )

            return insights

        # ------------------------------------------------------
        # Strong Right Skew
        # ------------------------------------------------------

        if (
            metric.skewness
            >= self.STRONG_SKEWNESS_THRESHOLD
        ):

            insights.append(
                Insight(
                    title="Right-Skewed Distribution",
                    description=(
                        f"{metric.column_name} shows a strongly "
                        f"right-skewed distribution, indicating "
                        f"that a relatively small number of "
                        f"high-value records may be influencing "
                        f"the average."
                    ),
                    category=InsightCategory.DATASET,
                    severity=InsightSeverity.INFO,
                )
            )

        # ------------------------------------------------------
        # Strong Left Skew
        # ------------------------------------------------------

        elif (
            metric.skewness
            <= -self.STRONG_SKEWNESS_THRESHOLD
        ):

            insights.append(
                Insight(
                    title="Left-Skewed Distribution",
                    description=(
                        f"{metric.column_name} shows a strongly "
                        f"left-skewed distribution, indicating "
                        f"that a relatively small number of "
                        f"low-value records may be influencing "
                        f"the distribution."
                    ),
                    category=InsightCategory.DATASET,
                    severity=InsightSeverity.INFO,
                )
            )

        return insights

    # ==========================================================
    # KPI INSIGHTS
    # ==========================================================

    def _build_kpi_insights(
        self,
        kpis: KPIResult,
    ) -> list[Insight]:
        """
        Generate insights from KPIs.
        """

        insights: list[Insight] = []

        for metric in kpis.metrics:

            if metric.name == "Total Rows":

                insights.append(
                    Insight(
                        title="Dataset Size",
                        description=(
                            f"The dataset contains "
                            f"{int(metric.value):,} records."
                        ),
                        category=InsightCategory.KPI,
                        severity=InsightSeverity.INFO,
                    )
                )

            elif metric.name == "Total Columns":

                insights.append(
                    Insight(
                        title="Dataset Structure",
                        description=(
                            f"The dataset contains "
                            f"{int(metric.value)} columns."
                        ),
                        category=InsightCategory.KPI,
                        severity=InsightSeverity.INFO,
                    )
                )

            elif (
                metric.name == "Missing Cells"
                and metric.value > 0
            ):

                insights.append(
                    Insight(
                        title="Missing Values",
                        description=(
                            f"The dataset contains "
                            f"{int(metric.value)} missing values."
                        ),
                        category=InsightCategory.DATASET,
                        severity=InsightSeverity.HIGH,
                    )
                )

            elif (
                metric.name == "Duplicate Rows"
                and metric.value > 0
            ):

                insights.append(
                    Insight(
                        title="Duplicate Records",
                        description=(
                            f"The dataset contains "
                            f"{int(metric.value)} duplicate rows."
                        ),
                        category=InsightCategory.DATASET,
                        severity=InsightSeverity.MEDIUM,
                    )
                )

        return insights

    # ==========================================================
    # CORRELATION INSIGHTS
    # ==========================================================

    def _build_correlation_insights(
        self,
        correlations: CorrelationResult,
    ) -> list[Insight]:
        """
        Generate insights from correlations.
        """

        insights: list[Insight] = []

        for correlation in correlations.correlations:

            if correlation.strength not in (
                CorrelationStrength.STRONG,
                CorrelationStrength.VERY_STRONG,
            ):
                continue

            strength = (
                correlation.strength.value
                .replace("_", " ")
            )

            insights.append(
                Insight(
                    title="Correlation Analysis",
                    description=(
                        f"{correlation.column_a} and "
                        f"{correlation.column_b} have a "
                        f"{strength} "
                        f"{correlation.direction.value} "
                        f"correlation."
                    ),
                    category=InsightCategory.CORRELATION,
                    severity=InsightSeverity.INFO,
                )
            )

        return insights

    # ==========================================================
    # TREND INSIGHTS
    # ==========================================================

    def _build_trend_insights(
        self,
        trends: TrendResult,
    ) -> list[Insight]:
        """
        Generate insights from trend analysis.
        """

        insights: list[Insight] = []

        for trend in trends.trends:

            article = (
                "an"
                if trend.direction.value == "increasing"
                else "a"
            )

            description = (
                f"{trend.metric_name} shows "
                f"{article} "
                f"{trend.direction.value} trend "
                f"over time."
            )

            insights.append(
                Insight(
                    title="Trend Analysis",
                    description=description,
                    category=InsightCategory.TREND,
                    severity=InsightSeverity.INFO,
                )
            )

        return insights

    # ==========================================================
    # SEGMENTATION INSIGHTS
    # ==========================================================

    def _build_segmentation_insights(
        self,
        segmentation: SegmentationResult,
    ) -> list[Insight]:
        """
        Generate insights from dataset segmentation.
        """

        insights: list[Insight] = []

        grouped_segments: dict[
            str,
            list[Segment],
        ] = {}

        for segment in segmentation.segments:

            grouped_segments.setdefault(
                segment.column_name,
                [],
            ).append(segment)

        for (
            column_name,
            segments,
        ) in grouped_segments.items():

            largest_segment = max(
                segments,
                key=lambda segment: segment.count,
            )

            insights.append(
                Insight(
                    title="Segmentation Analysis",
                    description=(
                        f"{largest_segment.category} is "
                        f"the largest category in "
                        f"'{column_name}', representing "
                        f"{largest_segment.percentage:.2f}% "
                        f"of all records."
                    ),
                    category=InsightCategory.SEGMENTATION,
                    severity=InsightSeverity.INFO,
                )
            )

        return insights