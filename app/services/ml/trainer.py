import time

from pandas import DataFrame
from pandas import Series
from numpy import ndarray
from sklearn.model_selection import train_test_split

from app.core.constants import MLConstants
from app.core.enums import MLEstimator
from app.schemas.ml import TrainResult
from app.schemas.ml import TrainedModel
from app.services.ml.factory import ModelFactory
from sklearn.base import BaseEstimator


class ModelTrainer:

    def train(
        self,
        dataframe: DataFrame,
        target_column: str,
        estimators: list[MLEstimator]
    ) -> TrainResult:

        features, target = self._split_features_target(
            dataframe,
            target_column
        )

        x_train, x_test, y_train, y_test = self._split_train_test(
            features,
            target
        )

        trained_models = self._train_models(
            x_train,
            x_test,
            y_train,
            y_test,
            estimators
        )

        return TrainResult(
            models=trained_models,
            training_rows=len(x_train),
            testing_rows=len(x_test),
        )

    def _split_features_target(
        self,
        dataframe: DataFrame,
        target_column: str
    ) -> tuple[DataFrame, Series]:

        features: DataFrame = dataframe.drop(
            columns=[target_column]
        )   

        target: Series = dataframe[target_column]

        return (
            features,
            target,
        )

    def _split_train_test(
        self,
        features: DataFrame,
        target: Series
    ) -> tuple[
        DataFrame,
        DataFrame,
        Series,
        Series,
    ]:

        return train_test_split(
            features,
            target,
            test_size=MLConstants.TEST_SIZE,
            random_state=MLConstants.RANDOM_STATE,
        )

    def _train_models(
        self,
        x_train: DataFrame,
        x_test: DataFrame,
        y_train: Series,
        y_test: Series,
        estimators: list[MLEstimator]
    ) -> list[TrainedModel]:

        trained_models: list[TrainedModel] = []

        for estimator in estimators:

            trained_model = self._train_model(
                estimator,
                x_train,
                x_test,
                y_train,
                y_test,
            )

            trained_models.append(
                trained_model
            )


        return trained_models

    def _train_model(
        self,
        estimator: MLEstimator,
        x_train: DataFrame,
        x_test: DataFrame,
        y_train: Series,
        y_test: Series
    ) -> TrainedModel:

        model: BaseEstimator = ModelFactory.create(
            estimator
        )

        start_time: float = time.perf_counter()

        model.fit(
            x_train,
            y_train
        )

        training_time: float = (
            time.perf_counter() - start_time
        )

        predictions: ndarray = model.predict(
            x_test
        )

        return TrainedModel(
            estimator=estimator,
            model=model,
            predictions=predictions,
            y_test=y_test,
            training_time=training_time,
        )
