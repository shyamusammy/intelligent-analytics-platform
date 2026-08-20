"""Dataset cleaning that preserves the original uploaded file."""

import pandas as pd

from app.repositories.dataset_repository import DatasetRepository
from app.schemas.cleaning import CleaningAction, CleaningReport
from app.schemas.etl import DetectedDataType, ETLProfile
from app.services.etl.profiling.duplicate_detector import DuplicateDetector
from app.services.etl.profiling.missing_value_analyzer import MissingValueAnalyzer
from app.services.etl.quality.outlier_detector import OutlierDetector
from app.services.etl.quality.quality_score import QualityScoreService


class CleaningEngine:
    """Create a cleaned dataset using the ETL schema profile as input knowledge."""

    def __init__(self, repository: DatasetRepository | None = None) -> None:
        self._repository = repository or DatasetRepository()

    def run(
        self,
        workspace_id: str,
        dataset_id: str,
        profile: ETLProfile,
        target_column: str | None = None,
    ) -> CleaningReport:
        # ---------------------------------------------------------
        # 1. Load original dataset
        # ---------------------------------------------------------
        dataframe = self._repository.load_dataframe(
            workspace_id,
            dataset_id,
        )

        original_rows = len(dataframe)

        # ---------------------------------------------------------
        # 2. Calculate RAW dataset quality
        # ---------------------------------------------------------
        missing_before = MissingValueAnalyzer().analyze(dataframe)

        duplicates_before = DuplicateDetector().analyze(dataframe)

        outliers_before = OutlierDetector().detect(dataframe)

        quality_before = QualityScoreService().calculate(
            total_rows=len(dataframe),
            total_columns=len(dataframe.columns),
            missing=missing_before,
            duplicates=duplicates_before,
            outliers=outliers_before,
        )

        # ---------------------------------------------------------
        # 3. Start cleaning
        # ---------------------------------------------------------
        cleaned = dataframe.drop_duplicates().copy()

        actions: list[CleaningAction] = []

        # ---------------------------------------------------------
        # 4. Handle missing target column
        # ---------------------------------------------------------
        if target_column and target_column in cleaned.columns:
            missing_target = int(
                cleaned[target_column].isna().sum()
            )

            if missing_target:
                cleaned = cleaned.dropna(
                    subset=[target_column]
                )

                actions.append(
                    CleaningAction(
                        column_name=target_column,
                        strategy="dropped_rows_with_missing_target",
                        values_replaced=missing_target,
                    )
                )

        # ---------------------------------------------------------
        # 5. Apply type-aware missing-value strategies
        # ---------------------------------------------------------
        for column in profile.schema_profile.columns:
            column_name = column.name

            if (
                column_name not in cleaned.columns
                or column_name == target_column
            ):
                continue

            missing_count = int(
                cleaned[column_name].isna().sum()
            )

            if not missing_count:
                continue

            # -----------------------------------------------------
            # Numerical columns
            # -----------------------------------------------------
            if column.detected_type in (
                DetectedDataType.INTEGER,
                DetectedDataType.FLOAT,
            ):
                series = cleaned[column_name]

                skewness = series.skew(skipna=True)

                # Use median for strongly skewed data.
                # Use mean otherwise.
                strategy = (
                    "median"
                    if abs(float(skewness or 0)) >= 1
                    else "mean"
                )

                value = (
                    series.median(skipna=True)
                    if strategy == "median"
                    else series.mean(skipna=True)
                )

                if pd.notna(value):
                    cleaned[column_name] = series.fillna(value)

                    actions.append(
                        CleaningAction(
                            column_name=column_name,
                            strategy=strategy,
                            values_replaced=missing_count,
                        )
                    )

            # -----------------------------------------------------
            # Categorical columns
            # -----------------------------------------------------
            elif column.detected_type == DetectedDataType.CATEGORICAL:
                mode = cleaned[column_name].mode(
                    dropna=True
                )

                if not mode.empty:
                    cleaned[column_name] = (
                        cleaned[column_name].fillna(
                            mode.iloc[0]
                        )
                    )

                    actions.append(
                        CleaningAction(
                            column_name=column_name,
                            strategy="mode",
                            values_replaced=missing_count,
                        )
                    )

            # -----------------------------------------------------
            # Datetime columns
            # -----------------------------------------------------
            elif column.detected_type == DetectedDataType.DATETIME:
                cleaned[column_name] = (
                    cleaned[column_name].fillna(
                        "Unknown date"
                    )
                )

                actions.append(
                    CleaningAction(
                        column_name=column_name,
                        strategy="missing_datetime_placeholder",
                        values_replaced=missing_count,
                    )
                )

        # ---------------------------------------------------------
        # 6. Final type-aware fallback
        #
        # This handles columns that were not covered above,
        # including:
        # - text
        # - mixed
        # - unknown
        # - all-null columns
        # - any residual nulls
        # ---------------------------------------------------------
        for column_name in cleaned.columns:
            missing_count = int(
                cleaned[column_name].isna().sum()
            )

            if not missing_count:
                continue

            series = cleaned[column_name]

            if pd.api.types.is_numeric_dtype(series):
                cleaned[column_name] = series.fillna(0)

                strategy = "numeric_fallback_zero"

            else:
                cleaned[column_name] = series.fillna(
                    "Unknown"
                )

                strategy = "missing_value_placeholder"

            actions.append(
                CleaningAction(
                    column_name=column_name,
                    strategy=strategy,
                    values_replaced=missing_count,
                )
            )

        # ---------------------------------------------------------
        # 7. FINAL NULL VALIDATION
        #
        # Cleaning must never be reported as successful if
        # missing values remain.
        # ---------------------------------------------------------
        missing_after = MissingValueAnalyzer().analyze(
            cleaned
        )

        if missing_after.total_missing_values != 0:
            raise ValueError(
                "Cleaning failed: "
                f"{missing_after.total_missing_values} "
                "missing values remain after cleaning."
            )

        # ---------------------------------------------------------
        # 8. Validate duplicates after cleaning
        # ---------------------------------------------------------
        duplicates_after = DuplicateDetector().analyze(
            cleaned
        )

        # The current cleaning pipeline removes duplicates
        # before imputation, so this should normally be zero.
        if duplicates_after.duplicate_rows != 0:
            raise ValueError(
                "Cleaning failed: "
                f"{duplicates_after.duplicate_rows} "
                "duplicate rows remain after cleaning."
            )

        # ---------------------------------------------------------
        # 9. Calculate cleaned dataset quality
        # ---------------------------------------------------------
        outliers_after = OutlierDetector().detect(
            cleaned
        )

        quality_after = QualityScoreService().calculate(
            total_rows=len(cleaned),
            total_columns=len(cleaned.columns),
            missing=missing_after,
            duplicates=duplicates_after,
            outliers=outliers_after,
        )

        # ---------------------------------------------------------
        # 10. Save cleaned dataset
        # ---------------------------------------------------------
        cleaned_path = (
            self._repository.save_cleaned_dataframe(
                workspace_id,
                dataset_id,
                cleaned,
            )
        )

        # ---------------------------------------------------------
        # 11. Validate the SAVED cleaned dataset
        #
        # Reload the actual file from disk rather than relying
        # only on the in-memory DataFrame.
        # ---------------------------------------------------------
        saved_cleaned = (
            self._repository.load_cleaned_dataframe(
                workspace_id,
                dataset_id,
            )
        )

        saved_missing = MissingValueAnalyzer().analyze(
            saved_cleaned
        )

        if saved_missing.total_missing_values != 0:
            raise ValueError(
                "Saved cleaned dataset validation failed: "
                f"{saved_missing.total_missing_values} "
                "missing values remain."
            )

        saved_duplicates = DuplicateDetector().analyze(
            saved_cleaned
        )

        if saved_duplicates.duplicate_rows != 0:
            raise ValueError(
                "Saved cleaned dataset validation failed: "
                f"{saved_duplicates.duplicate_rows} "
                "duplicate rows remain."
            )

        # ---------------------------------------------------------
        # 12. Create cleaning report
        # ---------------------------------------------------------
        report = CleaningReport(
            original_row_count=original_rows,
            cleaned_row_count=len(cleaned),

            duplicates_removed=duplicates_before.duplicate_rows,

            missing_values_before=(
                missing_before.total_missing_values
            ),

            missing_values_after=(
                missing_after.total_missing_values
            ),

            duplicate_rows_after=(
                duplicates_after.duplicate_rows
            ),

            quality_score_before=(
                quality_before.quality_score
            ),

            quality_score_after=(
                quality_after.quality_score
            ),

            columns_affected=[
                action.column_name
                for action in actions
            ],

            actions=actions,

            cleaned_dataset_path=str(
                cleaned_path
            ),
        )

        # ---------------------------------------------------------
        # 13. Persist cleaning report
        # ---------------------------------------------------------
        self._repository.save_cleaning_report(
            workspace_id,
            dataset_id,
            report,
        )

        return report