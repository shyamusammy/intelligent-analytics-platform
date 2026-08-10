import pandas as pd

from app.core.constants import ETLConstants

from app.schemas.context import (
    KnowledgeContext,
)

from app.schemas.analytics import (
    Segment,
    SegmentationResult,
)

from app.services.analytics.helpers.etl_schema_helper import (
    ETLSchemaHelper,
)


class SegmentationService:
    """
    Service responsible for generating categorical
    data segments.

    Responsibilities
    ----------------
    - Use ETL knowledge to identify categorical columns
    - Calculate category counts
    - Calculate category percentages

    This service contains NO persistence logic.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def run(
        self,
        dataframe: pd.DataFrame,
        knowledge: KnowledgeContext,
    ) -> SegmentationResult:
        """
        Generate dataset segments using ETL schema knowledge.
        """

        return SegmentationResult(
            segments=self._build_segments(
                dataframe=dataframe,
                knowledge=knowledge,
            )
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_segments(
        self,
        dataframe: pd.DataFrame,
        knowledge: KnowledgeContext,
    ) -> list[Segment]:
        """
        Build segments for ETL-detected categorical columns.
        """

        segments: list[Segment] = []

        total_rows = len(dataframe)

        categorical_columns = (
            ETLSchemaHelper.get_categorical_columns(
                knowledge.etl_profile,
            )
        )

        for column in categorical_columns:

            if column not in dataframe.columns:
                continue

            unique_count = dataframe[column].nunique(
                dropna=True,
            )

            unique_ratio = (
                unique_count / total_rows
                if total_rows > 0
                else 0
            )

            if (
                unique_count
                > ETLConstants.MAX_CATEGORICAL_UNIQUE_VALUES
            ):
                continue

            if (
                unique_ratio
                > ETLConstants.CATEGORICAL_UNIQUE_RATIO
            ):
                continue

            counts = dataframe[column].value_counts(
                dropna=False,
            )

            for category, count in counts.items():

                percentage = (
                    (count / total_rows) * 100
                    if total_rows > 0
                    else 0.0
                )

                segments.append(
                    Segment(
                        column_name=column,
                        category=str(category),
                        count=int(count),
                        percentage=round(
                            percentage,
                            2,
                        ),
                    )
                )

        return segments