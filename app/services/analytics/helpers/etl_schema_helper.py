from app.schemas.etl import (
    ETLProfile,
    DetectedDataType,
)


class ETLSchemaHelper:
    """
    Utility class for consuming ETL schema knowledge.

    Responsibilities
    ----------------
    - Locate datetime columns
    - Locate numeric columns
    - Locate categorical columns

    This helper contains NO business logic.
    """

    @staticmethod
    def get_datetime_column(
        profile: ETLProfile,
    ) -> str | None:
        """
        Return the first detected datetime column.
        """

        for column in profile.schema_profile.columns:

            if (
                column.detected_type
                == DetectedDataType.DATETIME
            ):
                return column.name

        return None

    @staticmethod
    def get_numeric_columns(
        profile: ETLProfile,
    ) -> list[str]:
        """
        Return all numeric columns.
        """

        numeric_columns: list[str] = []

        for column in profile.schema_profile.columns:

            if column.detected_type in (
                DetectedDataType.INTEGER,
                DetectedDataType.FLOAT,
            ):

                numeric_columns.append(
                    column.name,
                )

        return numeric_columns

    @staticmethod
    def get_categorical_columns(
        profile: ETLProfile,
    ) -> list[str]:
        """
        Return all categorical columns.
        """

        categorical_columns: list[str] = []

        for column in profile.schema_profile.columns:

            if (
                column.detected_type
                == DetectedDataType.CATEGORICAL
            ):

                categorical_columns.append(
                    column.name,
                )

        return categorical_columns

    @staticmethod
    def get_text_columns(
        etl_profile: ETLProfile,
    ) -> list[str]:
        """
        Return all text columns detected by the ETL Engine.
        """

        return [
            column.name
            for column in etl_profile.schema_profile.columns
            if column.detected_type == DetectedDataType.TEXT
        ]