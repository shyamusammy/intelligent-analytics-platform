from pandas import DataFrame, Series
from sklearn.model_selection import train_test_split

from app.core.constants import MLConstants


class DatasetSplitter:
    """Create reproducible holdout datasets before learned transformations."""

    def split(self, dataframe: DataFrame, target_column: str) -> tuple[DataFrame, DataFrame, Series, Series]:
        features = dataframe.drop(columns=[target_column])
        target = dataframe[target_column]
        return train_test_split(features, target, test_size=MLConstants.TEST_SIZE, random_state=MLConstants.RANDOM_STATE)
