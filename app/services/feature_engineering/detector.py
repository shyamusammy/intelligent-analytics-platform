from __future__ import annotations

import pandas as pd

from app.core.constants import FeatureEngineeringConstants
from app.schemas.feature_engineering import FeatureDecision


class FeatureDetector:
    """Classify usable ML features using deterministic dataframe signals."""

    _IDENTIFIER_TOKENS = ("id", "uuid", "key", "identifier", "code")

    def detect(self, dataframe: pd.DataFrame, datetime_columns: set[str] | None = None) -> tuple[dict[str, list[str]], list[FeatureDecision]]:
        datetime_columns = datetime_columns or set()
        groups = {"numeric": [], "categorical": [], "datetime": []}
        removed: list[FeatureDecision] = []
        for column in dataframe.columns:
            series = dataframe[column]
            cardinality = int(series.nunique(dropna=True))
            ratio = cardinality / max(1, len(series))
            lower_name = str(column).lower()
            dominant_ratio = float(series.value_counts(dropna=False, normalize=True).iloc[0]) if len(series) else 1.0
            identifier_name = any(token == lower_name or lower_name.endswith(f"_{token}") for token in self._IDENTIFIER_TOKENS)
            if column in datetime_columns or pd.api.types.is_datetime64_any_dtype(series):
                groups["datetime"].append(column)
            elif cardinality <= 1:
                removed.append(FeatureDecision(column=column, feature_type="constant", decision="removed", reason="constant_column", cardinality=cardinality))
            elif dominant_ratio >= FeatureEngineeringConstants.NEAR_CONSTANT_RATIO:
                removed.append(FeatureDecision(column=column, feature_type="near_constant", decision="removed", reason="near_constant_column", cardinality=cardinality))
            elif pd.api.types.is_numeric_dtype(series):
                if identifier_name or (ratio >= 0.98 and pd.api.types.is_integer_dtype(series)):
                    removed.append(FeatureDecision(column=column, feature_type="identifier", decision="removed", reason="identifier_like", cardinality=cardinality))
                else:
                    groups["numeric"].append(column)
            elif cardinality > FeatureEngineeringConstants.HIGH_CARDINALITY_THRESHOLD:
                removed.append(FeatureDecision(column=column, feature_type="categorical", decision="excluded", reason="high_cardinality", cardinality=cardinality))
            elif identifier_name:
                removed.append(FeatureDecision(column=column, feature_type="identifier", decision="removed", reason="identifier_like", cardinality=cardinality))
            else:
                groups["categorical"].append(column)
        return groups, removed
