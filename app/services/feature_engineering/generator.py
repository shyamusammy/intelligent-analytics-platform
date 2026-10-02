from __future__ import annotations

import pandas as pd


class DatetimeFeatureGenerator:
    """Generate stable calendar features from detected datetime columns."""

    def transform(self, dataframe: pd.DataFrame, columns: list[str]) -> tuple[pd.DataFrame, list[str]]:
        output = dataframe.copy()
        generated: list[str] = []
        for column in columns:
            values = pd.to_datetime(output[column], errors="coerce")
            prefix = f"{column}__"
            features = {
                f"{prefix}year": values.dt.year,
                f"{prefix}month": values.dt.month,
                f"{prefix}day": values.dt.day,
                f"{prefix}day_of_week": values.dt.dayofweek,
                f"{prefix}quarter": values.dt.quarter,
                f"{prefix}is_weekend": values.dt.dayofweek.isin([5, 6]).astype(int),
            }
            for name, series in features.items():
                output[name] = series.fillna(-1)
                generated.append(name)
            output = output.drop(columns=[column])
        return output, generated
