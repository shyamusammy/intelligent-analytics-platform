from app.schemas.etl import (
    DuplicateSummary,
    MissingValueSummary,
    OutlierSummary,
    QualityProfile,
)


class QualityScoreService:
    """
    Computes an overall data quality score.

    The quality score is based on:
    - Missing-value percentage
    - Duplicate-row percentage
    - Percentage of rows affected by outliers

    Outlier occurrences across multiple columns are not
    counted as separate rows for the outlier penalty.
    """

    def calculate(
        self,
        total_rows: int,
        total_columns: int,
        missing: MissingValueSummary,
        duplicates: DuplicateSummary,
        outliers: OutlierSummary,
    ) -> QualityProfile:
        # ---------------------------------------------------------
        # Missing-value penalty
        # ---------------------------------------------------------

        total_cells = (
            total_rows * total_columns
        )

        missing_penalty = 0.0

        if total_cells:
            missing_penalty = (
                missing.total_missing_values
                / total_cells
            ) * 100

        # ---------------------------------------------------------
        # Duplicate penalty
        # ---------------------------------------------------------

        duplicate_penalty = (
            duplicates.duplicate_percentage
        )

        # ---------------------------------------------------------
        # Outlier penalty
        # ---------------------------------------------------------

        outlier_penalty = 0.0

        if total_rows:
            outlier_penalty = (
                outliers.affected_rows
                / total_rows
            ) * 100

        # ---------------------------------------------------------
        # Final quality score
        # ---------------------------------------------------------

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