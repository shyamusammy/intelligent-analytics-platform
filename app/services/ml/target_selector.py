import pandas as pd


class TargetSelector:
    """Choose a plausible prediction target without dataset-specific rules."""

    KEYWORDS = ("target", "label", "outcome", "price", "revenue", "sales", "profit", "score", "value")

    def select(self, dataframe: pd.DataFrame) -> str | None:
        columns = [column for column in dataframe.columns if dataframe[column].nunique(dropna=True) >= 2]
        if not columns:
            return None
        for column in columns:
            if any(keyword in column.lower() for keyword in self.KEYWORDS):
                return column
        categorical = [column for column in columns if not pd.api.types.is_numeric_dtype(dataframe[column]) and dataframe[column].nunique(dropna=True) <= 20]
        if categorical:
            return categorical[-1]
        numeric = [column for column in columns if pd.api.types.is_numeric_dtype(dataframe[column])]
        return numeric[-1] if numeric else None
