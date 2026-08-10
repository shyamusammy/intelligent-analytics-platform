from pandas import DataFrame

from app.schemas.context import (
    KnowledgeContext,
)

from app.services.analytics.helpers.etl_schema_helper import (
    ETLSchemaHelper,
)


class MLPreprocessor:
    """
    Prepares datasets for machine learning.

    Responsibilities
    ----------------
    - Use ETL knowledge to identify numeric feature columns
    - Remove unsupported feature columns
    - Prepare the dataset for model training

    Future enhancements
    -------------------
    - Missing value imputation
    - Categorical encoding
    - Feature scaling
    - Feature engineering
    """

    def prepare(
        self,
        dataframe: DataFrame,
        target_column: str,
        knowledge: KnowledgeContext,
    ) -> DataFrame:
        """
        Prepare the dataset for model training
        using ETL schema knowledge.
        """

        target = dataframe[target_column]

        numeric_columns = (
            ETLSchemaHelper.get_numeric_columns(
                knowledge.etl_profile,
            )
        )

        feature_columns = [
            column
            for column in numeric_columns
            if column != target_column
            and column in dataframe.columns
        ]

        features = dataframe[
            feature_columns
        ].copy()

        features[target_column] = target

        return features