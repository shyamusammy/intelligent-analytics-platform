from __future__ import annotations

import numpy as np
import pandas as pd

from app.schemas.feature_engineering import FeatureValidationResult


class FeatureEngineeringValidator:
    def validate(self, train: pd.DataFrame, test: pd.DataFrame, target_column: str) -> FeatureValidationResult:
        errors: list[str] = []
        if target_column in train.columns or target_column in test.columns:
            errors.append("Target leakage: target column exists in the feature matrix.")
        if train.columns.duplicated().any():
            errors.append("Duplicate generated feature names detected.")
        if list(train.columns) != list(test.columns):
            errors.append("Training and testing feature schemas do not match.")
        if not np.isfinite(train.select_dtypes(include="number").to_numpy()).all() or not np.isfinite(test.select_dtypes(include="number").to_numpy()).all():
            errors.append("Feature matrix contains invalid or infinite numeric values.")
        return FeatureValidationResult(valid=not errors, errors=errors)
