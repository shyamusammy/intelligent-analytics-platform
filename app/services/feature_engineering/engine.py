from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

from app.schemas.context import KnowledgeContext
from app.schemas.etl import DetectedDataType
from app.schemas.feature_engineering import FeatureEngineeringReport
from app.services.feature_engineering.detector import FeatureDetector
from app.services.feature_engineering.generator import DatetimeFeatureGenerator
from app.services.feature_engineering.selector import FeatureSelector
from app.services.feature_engineering.validator import FeatureEngineeringValidator


class FeatureEngineeringEngine:
    """Fit deterministic feature transformations on train data only."""

    def __init__(self) -> None:
        self._detector = FeatureDetector()
        self._generator = DatetimeFeatureGenerator()
        self._selector = FeatureSelector()
        self._validator = FeatureEngineeringValidator()
        self._transformer: ColumnTransformer | None = None
        self._input_columns: list[str] = []
        self._datetime_columns: list[str] = []
        self._report: FeatureEngineeringReport | None = None

    @property
    def report(self) -> FeatureEngineeringReport:
        if self._report is None:
            raise RuntimeError("Feature engineering has not been fitted.")
        return self._report

    def fit_transform(self, x_train: pd.DataFrame, target_column: str, knowledge: KnowledgeContext) -> pd.DataFrame:
        if target_column in x_train.columns:
            raise ValueError("Target leakage: target column supplied to feature engineering.")
        profile_datetimes = {
            column.name for column in (knowledge.etl_profile.schema_profile.columns if knowledge.etl_profile else [])
            if column.detected_type == DetectedDataType.DATETIME and column.name in x_train.columns
        }
        groups, removed = self._detector.detect(x_train, profile_datetimes)
        self._datetime_columns = groups["datetime"]
        removed_names = {item.column for item in removed}
        self._input_columns = [column for column in x_train.columns if column not in removed_names]
        base, generated = self._generator.transform(x_train[self._input_columns], self._datetime_columns)
        numeric = [column for column in base.columns if pd.api.types.is_numeric_dtype(base[column])]
        categorical = [column for column in base.columns if column not in numeric]
        self._transformer = ColumnTransformer(
            [("numeric", "passthrough", numeric), ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical)],
            remainder="drop",
            verbose_feature_names_out=False,
        )
        transformed = self._to_dataframe(self._transformer.fit_transform(base), self._transformer.get_feature_names_out(), base.index)
        transformed = self._selector.select(transformed)
        validation = self._validator.validate(transformed, transformed.copy(), target_column)
        self._report = FeatureEngineeringReport(
            target_column=target_column,
            original_feature_count=len(x_train.columns),
            generated_feature_count=len(generated),
            final_feature_count=len(transformed.columns),
            numeric_features=groups["numeric"],
            categorical_features=groups["categorical"],
            datetime_features=self._datetime_columns,
            encoded_features=[name for name in transformed.columns if name not in numeric],
            generated_datetime_features=generated,
            removed_columns=removed,
            decisions=removed,
            training_feature_count=len(transformed.columns),
            validation=validation,
        )
        if not validation.valid:
            raise ValueError("; ".join(validation.errors))
        return transformed

    def transform(self, x_test: pd.DataFrame, target_column: str) -> pd.DataFrame:
        if self._transformer is None:
            raise RuntimeError("Feature engineering must be fitted before transform.")
        if target_column in x_test.columns:
            raise ValueError("Target leakage: target column supplied to feature engineering.")
        missing = set(self._input_columns) - set(x_test.columns)
        if missing:
            raise ValueError(f"Test data is missing training columns: {sorted(missing)}")
        base, _ = self._generator.transform(x_test[self._input_columns], self._datetime_columns)
        transformed = self._to_dataframe(self._transformer.transform(base), self._transformer.get_feature_names_out(), base.index)
        transformed = self._selector.select(transformed)
        validation = self._validator.validate(self._to_dataframe(self._transformer.transform(self._generator.transform(x_test[self._input_columns], self._datetime_columns)[0]), self._transformer.get_feature_names_out(), base.index), transformed, target_column)
        if not validation.valid:
            raise ValueError("; ".join(validation.errors))
        self._report.testing_feature_count = len(transformed.columns)
        return transformed

    @staticmethod
    def _to_dataframe(values, columns, index) -> pd.DataFrame:
        return pd.DataFrame(values, columns=list(columns), index=index)
