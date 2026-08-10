import pandas as pd

from pandas.api.types import (
    is_numeric_dtype,
)

from app.schemas.context import (
    KnowledgeContext,
)

from app.schemas.analytics import (
    CategoricalColumnStatistics,
    DatasetSummary,
    NumericColumnStatistics,
    StatisticsResult,
)

from app.services.analytics.helpers.etl_schema_helper import (
    ETLSchemaHelper,
)


class StatisticsService:
    """
    Service responsible for generating descriptive statistics
    for a dataset.

    Responsibilities
    ----------------
    - Dataset summary
    - Numeric column statistics
    - Categorical column statistics

    This service contains NO persistence logic.
    """

    # ==========================================================
    # PUBLIC
    # ==========================================================

    def run(
        self,
        dataframe: pd.DataFrame,
        knowledge: KnowledgeContext,
    ) -> StatisticsResult:
        """
        Generate descriptive statistics for the dataset.
        """

        return StatisticsResult(
            dataset_summary=self._build_dataset_summary(
                dataframe=dataframe,
                knowledge=knowledge,
            ),
            numeric_statistics=self._build_numeric_statistics(
                dataframe,
            ),
            categorical_statistics=self._build_categorical_statistics(
                dataframe=dataframe,
                knowledge=knowledge,
            ),
        )

    # ==========================================================
    # PRIVATE
    # ==========================================================

    def _build_dataset_summary(
        self,
        dataframe: pd.DataFrame,
        knowledge: KnowledgeContext,
    ) -> DatasetSummary:
        """
        Build overall dataset summary using the ETL profile.
        """

        numeric_columns = len(
            ETLSchemaHelper.get_numeric_columns(
                knowledge.etl_profile,
            )
        )

        categorical_columns = len(
            ETLSchemaHelper.get_categorical_columns(
                knowledge.etl_profile,
            )
        )

        datetime_column = (
            ETLSchemaHelper.get_datetime_column(
                knowledge.etl_profile,
            )
        )

        datetime_columns = (
            1
            if datetime_column
            else 0
        )

        text_columns = len(
            ETLSchemaHelper.get_text_columns(
                knowledge.etl_profile,
            )
        )


        return DatasetSummary(
            total_rows=len(dataframe),

            total_columns=(
                knowledge.etl_profile
                .schema_profile
                .total_columns
            ),

            numeric_columns=numeric_columns,

            categorical_columns=categorical_columns,

            datetime_columns=datetime_columns,

            text_columns=text_columns,

            missing_cells=(
                knowledge.etl_profile
                .missing_values
                .total_missing_values
            ),

            duplicate_rows=(
                knowledge.etl_profile
                .duplicates
                .duplicate_rows
            ),
        )

    def _build_numeric_statistics(
        self,
        dataframe: pd.DataFrame,
    ) -> list[NumericColumnStatistics]:
        """
        Build descriptive statistics for numeric columns.
        """

        statistics: list[
            NumericColumnStatistics
        ] = []

        numeric_dataframe = dataframe.select_dtypes(
            include=["number"],
        )

        for column in numeric_dataframe.columns:

            series = numeric_dataframe[column]

            statistics.append(
                NumericColumnStatistics(
                    column_name=column,
                    mean=self._safe_float(
                        series.mean()
                    ),
                    median=self._safe_float(
                        series.median()
                    ),
                    minimum=self._safe_float(
                        series.min()
                    ),
                    maximum=self._safe_float(
                        series.max()
                    ),
                    std_dev=self._safe_float(
                        series.std()
                    ),
                    variance=self._safe_float(
                        series.var()
                    ),
                    skewness=self._safe_float(
                        series.skew()
                    ),
                    kurtosis=self._safe_float(
                        series.kurt()
                    ),
                )
            )

        return statistics

    def _build_categorical_statistics(
        self,
        dataframe: pd.DataFrame,
        knowledge=KnowledgeContext,
    ) -> list[CategoricalColumnStatistics]:
        """
        Build descriptive statistics for ETL-detected categorical columns.
        """

        statistics: list[
            CategoricalColumnStatistics
        ] = []

        categorical_columns = (
            ETLSchemaHelper.get_categorical_columns(
                knowledge.etl_profile,
            )
        )

        for column in categorical_columns:
            
            if column not in dataframe.columns:
                continue

            series = dataframe[column]

            mode = series.mode(
                dropna=True,
            )

            if mode.empty:

                most_frequent = None
                most_frequent_count = None

            else:

                value_counts = series.value_counts(
                    dropna=True,
                )

                most_frequent = str(
                    mode.iloc[0]
                )

                most_frequent_count = int(
                    value_counts.iloc[0]
                )

            statistics.append(
                CategoricalColumnStatistics(
                    column_name=column,
                    unique_values=int(
                        series.nunique(
                            dropna=True,
                        )
                    ),
                    most_frequent=most_frequent,
                    most_frequent_count=most_frequent_count,
                )
            )

        return statistics

    def _safe_float(
        self,
        value: object,
    ) -> float:
        """
        Convert NaN values to 0.0.
        """

        if pd.isna(value):

            return 0.0

        return float(value)