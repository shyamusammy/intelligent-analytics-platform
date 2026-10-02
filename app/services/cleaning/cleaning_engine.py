"""
Intelligent Analytics Platform
Dataset cleaning engine.

CleaningEngine:
    - Preserves the original uploaded dataset.
    - Removes duplicate rows.
    - Handles missing target values.
    - Applies type-aware missing-value strategies.
    - Detects original outliers using reusable IQR boundaries.
    - Cleans numeric outliers using non-destructive capping.
    - Never deletes rows because of outliers.
    - Protects the target column from outlier modification.
    - Calculates dataset quality before and after cleaning.
    - Saves and validates the cleaned dataset.
    - Persists a complete CleaningReport.
"""

from __future__ import annotations

import pandas as pd

from app.repositories.dataset_repository import DatasetRepository
from app.schemas.cleaning import CleaningAction, CleaningReport
from app.schemas.etl import DetectedDataType, ETLProfile

from app.services.etl.profiling.duplicate_detector import (
    DuplicateDetector,
)
from app.services.etl.profiling.missing_value_analyzer import (
    MissingValueAnalyzer,
)
from app.services.etl.quality.outlier_cleaner import (
    OutlierCleaner,
)
from app.services.etl.quality.outlier_detector import (
    OutlierDetector,
)
from app.services.etl.quality.quality_score import (
    QualityScoreService,
)


class CleaningEngine:
    """
    Create a cleaned dataset using the ETL schema profile.

    Cleaning policy
    ---------------

    1. Duplicate rows are removed.
    2. Missing target rows are removed.
    3. Missing values are handled using type-aware strategies.
    4. Numeric outliers are NOT deleted.
    5. Numeric outliers are capped using the original IQR bounds.
    6. The target column is protected from outlier modification.
    7. Original IQR boundaries are reused when calculating
       outliers_after.

    Reusing the original boundaries is important because
    recalculating Q1/Q3 after cleaning can cause the apparent
    number of outliers to increase even though the original
    extreme values were already corrected.
    """

    def __init__(
        self,
        repository: DatasetRepository | None = None,
    ) -> None:
        self._repository = (
            repository or DatasetRepository()
        )

    # ============================================================
    # PUBLIC
    # ============================================================

    def run(
        self,
        workspace_id: str,
        dataset_id: str,
        profile: ETLProfile,
        target_column: str | None = None,
    ) -> CleaningReport:
        """
        Execute the complete dataset cleaning workflow.

        Workflow
        --------

        Load original dataset
                ↓
        Analyze missing values
                ↓
        Detect duplicates
                ↓
        Calculate original outlier boundaries
                ↓
        Detect original outliers
                ↓
        Calculate original quality
                ↓
        Remove duplicate rows
                ↓
        Remove rows with missing target
                ↓
        Handle missing values
                ↓
        Cap numeric outliers
                ↓
        Validate missing values
                ↓
        Remove duplicates created by capping
                ↓
        Detect remaining outliers using ORIGINAL boundaries
                ↓
        Calculate cleaned quality
                ↓
        Save cleaned dataset
                ↓
        Validate saved dataset
                ↓
        Persist CleaningReport
        """

        # ========================================================
        # 1. LOAD ORIGINAL DATASET
        # ========================================================

        dataframe = self._repository.load_dataframe(
            workspace_id,
            dataset_id,
        )

        original_rows = len(dataframe)

        # ========================================================
        # 2. INITIALIZE SERVICES
        # ========================================================

        missing_analyzer = MissingValueAnalyzer()
        duplicate_detector = DuplicateDetector()
        outlier_detector = OutlierDetector()
        outlier_cleaner = OutlierCleaner()
        quality_service = QualityScoreService()

        # ========================================================
        # 3. RAW DATASET ANALYSIS
        # ========================================================

        missing_before = missing_analyzer.analyze(
            dataframe
        )

        duplicates_before = duplicate_detector.analyze(
            dataframe
        )

        # ========================================================
        # 4. CALCULATE ORIGINAL OUTLIER BOUNDARIES
        # ========================================================

        """
        Calculate the IQR boundaries ONCE from the original
        uploaded dataset.

        These same boundaries are reused after cleaning.

        This prevents the following problem:

            raw data
                ↓
            calculate Q1/Q3
                ↓
            clean outliers
                ↓
            calculate NEW Q1/Q3
                ↓
            different outlier population

        Instead we use:

            raw data
                ↓
            calculate Q1/Q3
                ↓
            clean data
                ↓
            evaluate cleaned data using ORIGINAL Q1/Q3
        """

        outlier_boundaries = (
            outlier_detector.calculate_boundaries(
                dataframe
            )
        )

        # ========================================================
        # 5. DETECT RAW OUTLIERS
        # ========================================================

        outliers_before = outlier_detector.detect(
            dataframe,
            boundaries=outlier_boundaries,
        )

        # ========================================================
        # 6. RAW DATASET QUALITY
        # ========================================================

        quality_before = quality_service.calculate(
            total_rows=len(dataframe),
            total_columns=len(dataframe.columns),
            missing=missing_before,
            duplicates=duplicates_before,
            outliers=outliers_before,
        )

        # ========================================================
        # 7. START CLEANING
        # ========================================================

        cleaned = dataframe.copy()

        actions: list[CleaningAction] = []

        # ========================================================
        # 8. REMOVE ORIGINAL DUPLICATES
        # ========================================================

        cleaned = cleaned.drop_duplicates().copy()

        # ========================================================
        # 9. HANDLE MISSING TARGET COLUMN
        # ========================================================

        if (
            target_column
            and target_column in cleaned.columns
        ):
            missing_target = int(
                cleaned[target_column].isna().sum()
            )

            if missing_target:
                cleaned = cleaned.dropna(
                    subset=[target_column]
                ).copy()

                actions.append(
                    CleaningAction(
                        column_name=target_column,
                        strategy=(
                            "dropped_rows_with_missing_target"
                        ),
                        values_replaced=missing_target,
                    )
                )

        # ========================================================
        # 10. TYPE-AWARE MISSING VALUE STRATEGIES
        # ========================================================

        for column in profile.schema_profile.columns:

            column_name = column.name

            # ----------------------------------------------------
            # Skip missing columns.
            # ----------------------------------------------------

            if column_name not in cleaned.columns:
                continue

            # ----------------------------------------------------
            # Target column was already handled.
            # ----------------------------------------------------

            if column_name == target_column:
                continue

            missing_count = int(
                cleaned[column_name].isna().sum()
            )

            if not missing_count:
                continue

            # ====================================================
            # NUMERICAL COLUMNS
            # ====================================================

            if column.detected_type in (
                DetectedDataType.INTEGER,
                DetectedDataType.FLOAT,
            ):
                series = cleaned[column_name]

                # ------------------------------------------------
                # All-null numerical column.
                # Let the final fallback handle it.
                # ------------------------------------------------

                if series.dropna().empty:
                    continue

                skewness = series.skew(
                    skipna=True
                )

                # ------------------------------------------------
                # Strongly skewed → median.
                # Otherwise → mean.
                # ------------------------------------------------

                strategy = (
                    "median"
                    if abs(float(skewness or 0)) >= 1
                    else "mean"
                )

                if strategy == "median":
                    value = series.median(
                        skipna=True
                    )
                else:
                    value = series.mean(
                        skipna=True
                    )

                if pd.notna(value):
                    cleaned[column_name] = (
                        series.fillna(value)
                    )

                    actions.append(
                        CleaningAction(
                            column_name=column_name,
                            strategy=strategy,
                            values_replaced=missing_count,
                        )
                    )

            # ====================================================
            # CATEGORICAL COLUMNS
            # ====================================================

            elif (
                column.detected_type
                == DetectedDataType.CATEGORICAL
            ):
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

            # ====================================================
            # DATETIME COLUMNS
            # ====================================================

            elif (
                column.detected_type
                == DetectedDataType.DATETIME
            ):
                cleaned[column_name] = (
                    cleaned[column_name].fillna(
                        "Unknown date"
                    )
                )

                actions.append(
                    CleaningAction(
                        column_name=column_name,
                        strategy=(
                            "missing_datetime_placeholder"
                        ),
                        values_replaced=missing_count,
                    )
                )

        # ========================================================
        # 11. FINAL MISSING VALUE FALLBACK
        # ========================================================

        for column_name in cleaned.columns:

            missing_count = int(
                cleaned[column_name].isna().sum()
            )

            if not missing_count:
                continue

            series = cleaned[column_name]

            if pd.api.types.is_numeric_dtype(
                series
            ):
                cleaned[column_name] = (
                    series.fillna(0)
                )

                strategy = (
                    "numeric_fallback_zero"
                )

            else:
                cleaned[column_name] = (
                    series.fillna("Unknown")
                )

                strategy = (
                    "missing_value_placeholder"
                )

            actions.append(
                CleaningAction(
                    column_name=column_name,
                    strategy=strategy,
                    values_replaced=missing_count,
                )
            )

        # ========================================================
        # 12. OUTLIER CLEANING
        # ========================================================

        """
        Cap numeric outliers.

        IMPORTANT:

        The target column is protected.

        Rows are never removed because of outliers.
        """

        protected_columns: set[str] = set()

        if (
            target_column
            and target_column in cleaned.columns
        ):
            protected_columns.add(
                target_column
            )

        # --------------------------------------------------------
        # Snapshot before outlier cleaning.
        # --------------------------------------------------------

        before_outlier_cleaning = cleaned.copy()

        # --------------------------------------------------------
        # Apply non-destructive outlier capping.
        #
        # OutlierCleaner calculates its own IQR boundaries on
        # the current dataframe.
        #
        # To keep the cleaner behavior aligned with the original
        # boundaries, we therefore perform the actual replacement
        # here using the ORIGINAL boundaries.
        # --------------------------------------------------------

        for column_name, stats in (
            outlier_boundaries.items()
        ):

            # ----------------------------------------------------
            # Column must still exist.
            # ----------------------------------------------------

            if column_name not in cleaned.columns:
                continue

            # ----------------------------------------------------
            # Protected columns must never be modified.
            # ----------------------------------------------------

            if column_name in protected_columns:
                continue

            series = cleaned[column_name]

            # ----------------------------------------------------
            # Only numeric columns are relevant.
            # ----------------------------------------------------

            if not pd.api.types.is_numeric_dtype(
                series
            ):
                continue

            lower = stats["lower"]
            upper = stats["upper"]

            outlier_mask = (
                (series < lower)
                | (series > upper)
            ).fillna(False)

            if not outlier_mask.any():
                continue

            # ----------------------------------------------------
            # Convert only when replacement is required.
            #
            # This prevents integer-column assignment issues when
            # IQR boundaries are fractional.
            # ----------------------------------------------------

            if not pd.api.types.is_float_dtype(
                cleaned[column_name]
            ):
                cleaned[column_name] = (
                    cleaned[column_name].astype(float)
                )

            series = cleaned[column_name]

            lower_outliers = (
                outlier_mask
                & (series < lower)
            )

            upper_outliers = (
                outlier_mask
                & (series > upper)
            )

            cleaned.loc[
                lower_outliers,
                column_name,
            ] = lower

            cleaned.loc[
                upper_outliers,
                column_name,
            ] = upper

            # ----------------------------------------------------
            # Count actual replacements.
            # ----------------------------------------------------

            changed_count = int(
                outlier_mask.sum()
            )

            if changed_count:
                actions.append(
                    CleaningAction(
                        column_name=column_name,
                        strategy="outlier_cap",
                        values_replaced=changed_count,
                    )
                )

        # ========================================================
        # 13. FINAL NULL VALIDATION
        # ========================================================

        missing_after = missing_analyzer.analyze(
            cleaned
        )

        if (
            missing_after.total_missing_values
            != 0
        ):
            raise ValueError(
                "Cleaning failed: "
                f"{missing_after.total_missing_values} "
                "missing values remain after cleaning."
            )

        # ========================================================
        # 14. REMOVE DUPLICATES CREATED BY OUTLIER CAPPING
        # ========================================================

        """
        Outlier capping can turn previously different rows into
        identical rows.

        Therefore a final duplicate-removal pass is required.

        Example:

            Row A: age = 100
            Row B: age = 12.5

        If 100 is capped to 12.5, both rows become identical.

        Those newly created duplicates are removed here.
        """

        duplicates_after_outlier_cleaning = (
            duplicate_detector.analyze(cleaned)
        )

        duplicates_created_by_outlier_cleaning = (
            duplicates_after_outlier_cleaning.duplicate_rows
        )

        if duplicates_created_by_outlier_cleaning:

            cleaned = cleaned.drop_duplicates().copy()

            actions.append(
                CleaningAction(
                    column_name="__dataset__",
                    strategy=(
                        "removed_duplicates_created_by_outlier_cleaning"
                    ),
                    values_replaced=(
                        duplicates_created_by_outlier_cleaning
                    ),
                )
            )

        # ========================================================
        # 15. FINAL DUPLICATE VALIDATION
        # ========================================================

        duplicates_after = duplicate_detector.analyze(
            cleaned
        )

        if duplicates_after.duplicate_rows != 0:
            raise ValueError(
                "Cleaning failed: "
                f"{duplicates_after.duplicate_rows} "
                "duplicate rows remain after final cleaning."
            )

        # ========================================================
        # 16. DETECT OUTLIERS AFTER CLEANING
        # ========================================================

        """
        Reuse the ORIGINAL boundaries.

        Do NOT recalculate Q1/Q3 after cleaning.

        This gives a true before/after comparison against the
        same statistical definition of an outlier.
        """

        outliers_after = outlier_detector.detect(
            cleaned,
            boundaries=outlier_boundaries,
        )

        # ========================================================
        # 17. CLEANED DATASET QUALITY
        # ========================================================

        quality_after = quality_service.calculate(
            total_rows=len(cleaned),
            total_columns=len(cleaned.columns),
            missing=missing_after,
            duplicates=duplicates_after,
            outliers=outliers_after,
        )

        # ========================================================
        # 18. SAVE CLEANED DATASET
        # ========================================================

        cleaned_path = (
            self._repository.save_cleaned_dataframe(
                workspace_id,
                dataset_id,
                cleaned,
            )
        )

        # ========================================================
        # 19. VALIDATE SAVED CLEANED DATASET
        # ========================================================

        saved_cleaned = (
            self._repository.load_cleaned_dataframe(
                workspace_id,
                dataset_id,
            )
        )

        # --------------------------------------------------------
        # Validate missing values.
        # --------------------------------------------------------

        saved_missing = missing_analyzer.analyze(
            saved_cleaned
        )

        if (
            saved_missing.total_missing_values
            != 0
        ):
            raise ValueError(
                "Saved cleaned dataset validation failed: "
                f"{saved_missing.total_missing_values} "
                "missing values remain."
            )

        # --------------------------------------------------------
        # Validate duplicates.
        # --------------------------------------------------------

        saved_duplicates = (
            duplicate_detector.analyze(
                saved_cleaned
            )
        )

        if (
            saved_duplicates.duplicate_rows
            != 0
        ):
            raise ValueError(
                "Saved cleaned dataset validation failed: "
                f"{saved_duplicates.duplicate_rows} "
                "duplicate rows remain."
            )

        # --------------------------------------------------------
        # Validate saved outliers using the ORIGINAL boundaries.
        # --------------------------------------------------------

        saved_outliers = outlier_detector.detect(
            saved_cleaned,
            boundaries=outlier_boundaries,
        )

        # The saved file should represent the same cleaned
        # dataset that was measured before saving.
        if (
            saved_outliers.total_outliers
            != outliers_after.total_outliers
        ):
            raise ValueError(
                "Saved cleaned dataset validation failed: "
                "outlier statistics changed after persistence."
            )

        # ========================================================
        # 20. BUILD UNIQUE COLUMNS AFFECTED
        # ========================================================

        columns_affected: list[str] = []

        for action in actions:

            if (
                action.column_name
                not in columns_affected
            ):
                columns_affected.append(
                    action.column_name
                )

        # ========================================================
        # 21. CREATE CLEANING REPORT
        # ========================================================

        report = CleaningReport(
            original_row_count=original_rows,

            cleaned_row_count=len(cleaned),

            duplicates_removed=(
                duplicates_before.duplicate_rows
            ),

            missing_values_before=(
                missing_before.total_missing_values
            ),

            missing_values_after=(
                missing_after.total_missing_values
            ),

            duplicate_rows_after=(
                duplicates_after.duplicate_rows
            ),

            # ----------------------------------------------------
            # OUTLIERS
            # ----------------------------------------------------

            outliers_before=outliers_before,

            outliers_after=outliers_after,

            # ----------------------------------------------------
            # QUALITY
            # ----------------------------------------------------

            quality_score_before=(
                quality_before.quality_score
            ),

            quality_score_after=(
                quality_after.quality_score
            ),

            # ----------------------------------------------------
            # ACTIONS
            # ----------------------------------------------------

            columns_affected=columns_affected,

            actions=actions,

            cleaned_dataset_path=str(
                cleaned_path
            ),
        )

        # ========================================================
        # 22. PERSIST CLEANING REPORT
        # ========================================================

        self._repository.save_cleaning_report(
            workspace_id,
            dataset_id,
            report,
        )

        return report