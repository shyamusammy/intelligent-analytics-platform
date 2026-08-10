import pandas as pd

from app.core.enums import (
    CorrelationDirection,
    CorrelationMethod,
    CorrelationStrength,
)

from app.schemas.context import (
    KnowledgeContext,
)

from app.schemas.analytics import (
    CorrelationPair,
    CorrelationResult,
)

from app.services.analytics.helpers.etl_schema_helper import (
    ETLSchemaHelper,
)


class CorrelationService:
    """
    Service responsible for generating correlations
    between numeric columns.

    Responsibilities
    ----------------
    - Use ETL knowledge to identify numeric columns
    - Compute Pearson correlations
    - Classify correlation strength
    - Determine correlation direction

    This service contains NO persistence logic.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def run(
        self,
        dataframe: pd.DataFrame,
        knowledge: KnowledgeContext,
    ) -> CorrelationResult:
        """
        Generate correlations for ETL-detected
        numeric columns.
        """

        correlations = self._build_correlations(
            dataframe=dataframe,
            knowledge=knowledge,
        )

        correlations.sort(
            key=lambda pair: abs(pair.coefficient),
            reverse=True,
        )

        return CorrelationResult(
            correlations=correlations,
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_correlations(
        self,
        dataframe: pd.DataFrame,
        knowledge: KnowledgeContext,
    ) -> list[CorrelationPair]:
        """
        Build unique Pearson correlations between
        ETL-detected numeric columns.
        """

        correlations: list[
            CorrelationPair
        ] = []

        numeric_columns = (
            ETLSchemaHelper.get_numeric_columns(
                knowledge.etl_profile,
            )
        )

        existing_columns = [
            column
            for column in numeric_columns
            if column in dataframe.columns
        ]

        if not existing_columns:
            return correlations

        numeric_dataframe = dataframe[
            existing_columns
        ]

        correlation_matrix = numeric_dataframe.corr(
            method="pearson",
        )

        columns = list(
            correlation_matrix.columns
        )

        for i in range(len(columns)):

            for j in range(i + 1, len(columns)):

                column_a = columns[i]
                column_b = columns[j]

                coefficient = correlation_matrix.loc[
                    column_a,
                    column_b,
                ]

                if pd.isna(coefficient):
                    continue

                coefficient = float(
                    coefficient
                )

                correlations.append(
                    CorrelationPair(
                        column_a=column_a,
                        column_b=column_b,
                        coefficient=coefficient,
                        method=CorrelationMethod.PEARSON,
                        strength=self._get_strength(
                            coefficient,
                        ),
                        direction=self._get_direction(
                            coefficient,
                        ),
                    )
                )

        return correlations

    def _get_strength(
        self,
        coefficient: float,
    ) -> CorrelationStrength:
        """
        Classify correlation strength.
        """

        value = abs(
            coefficient,
        )

        if value >= 0.90:
            return CorrelationStrength.VERY_STRONG

        if value >= 0.70:
            return CorrelationStrength.STRONG

        if value >= 0.50:
            return CorrelationStrength.MODERATE

        if value >= 0.30:
            return CorrelationStrength.WEAK

        return CorrelationStrength.VERY_WEAK

    def _get_direction(
        self,
        coefficient: float,
    ) -> CorrelationDirection:
        """
        Determine correlation direction.
        """

        if coefficient > 0:
            return CorrelationDirection.POSITIVE

        if coefficient < 0:
            return CorrelationDirection.NEGATIVE

        return CorrelationDirection.NONE