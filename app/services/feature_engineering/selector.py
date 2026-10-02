from __future__ import annotations

import pandas as pd

from app.core.constants import FeatureEngineeringConstants


class FeatureSelector:
    """Enforce the conservative first-sprint feature-count limit."""

    def select(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        if len(dataframe.columns) > FeatureEngineeringConstants.MAX_FEATURES:
            raise ValueError(f"Feature count exceeds limit of {FeatureEngineeringConstants.MAX_FEATURES}.")
        return dataframe
