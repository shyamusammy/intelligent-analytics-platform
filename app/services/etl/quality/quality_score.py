from app.schemas.etl import (
    DuplicateSummary,
    MissingValueSummary,
    OutlierSummary,
    QualityProfile,
)


class QualityScoreService:
    """
    Computes an overall data quality score.
    """

    def calculate(
        self,
        total_rows: int,
        total_columns: int,
        missing: MissingValueSummary,
        duplicates: DuplicateSummary,
        outliers: OutlierSummary,
    ) -> QualityProfile:

        total_cells = total_rows * total_columns

        missing_penalty = 0.0

        if total_cells:

            missing_penalty = (
                missing.total_missing_values
                / total_cells
            ) * 100

        duplicate_penalty = (
            duplicates.duplicate_percentage
        )

        outlier_penalty = 0.0

        if total_rows:

            outlier_penalty = (
                outliers.total_outliers
                / total_rows
            ) * 100

        score = max(
            0.0,
            round(
                100
                - missing_penalty
                - duplicate_penalty
                - outlier_penalty,
                2,
            ),
        )

        return QualityProfile(

            quality_score=score,

            missing_penalty=round(
                missing_penalty,
                2,
            ),

            duplicate_penalty=round(
                duplicate_penalty,
                2,
            ),

            outlier_penalty=round(
                outlier_penalty,
                2,
            ),
        )