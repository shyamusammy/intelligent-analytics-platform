import pandas as pd

from app.schemas.etl import (
    ColumnProfile,
    SchemaProfile,
)

from app.services.etl.schema.datatype_inference import (
    DataTypeInferenceService,
)


class SchemaDetector:
    """
    Detects the schema of a pandas DataFrame.

    Responsibilities
    ----------------
    - Inspect every column
    - Infer semantic datatype
    - Calculate basic schema properties

    This service performs NO statistical analysis.
    """

    def __init__(
        self,
        inference_service: DataTypeInferenceService | None = None,
    ) -> None:

        self.inference_service = (
            inference_service
            or DataTypeInferenceService()
        )

    def detect(
        self,
        dataframe: pd.DataFrame,
    ) -> SchemaProfile:
        """
        Detect the schema of a dataset.
        """

        columns = []

        for column_name in dataframe.columns:

            series = dataframe[column_name]

            profile = ColumnProfile(

                name=column_name,

                pandas_dtype=str(series.dtype),

                detected_type=self.inference_service.infer(
                    series
                ),

                nullable=series.isna().any(),

                unique=series.is_unique,

                null_count=int(
                    series.isna().sum()
                ),
            )

            columns.append(profile)

        return SchemaProfile(

            total_columns=len(columns),

            columns=columns,
        )