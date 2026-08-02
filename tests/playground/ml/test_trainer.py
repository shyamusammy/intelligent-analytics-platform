from pandas import DataFrame

from app.core.enums import MLEstimator
from app.services.ml.trainer import ModelTrainer


def regression_dataset() -> DataFrame:

    return DataFrame(
        {
            "experience": [
                1, 2, 3, 4, 5,
                6, 7, 8, 9, 10,
                11, 12, 13, 14, 15,
                16, 17, 18, 19, 20,
                21, 22, 23, 24, 25,
                26, 27, 28, 29, 30,
            ],
            "salary": [
                30000, 35000, 40000, 45000, 50000,
                55000, 60000, 65000, 70000, 75000,
                80000, 85000, 90000, 95000, 100000,
                105000, 110000, 115000, 120000, 125000,
                130000, 135000, 140000, 145000, 150000,
                155000, 160000, 165000, 170000, 175000,
            ],
        }
    )


def main():

    trainer = ModelTrainer()

    result = trainer.train(
        dataframe=regression_dataset(),
        target_column="salary",
        estimators=[
            MLEstimator.LINEAR_REGRESSION,
            MLEstimator.RANDOM_FOREST_REGRESSOR,
        ],
    )

    print("=" * 60)
    print("Training Results")
    print("=" * 60)

    print(f"Models Trained: {len(result.models)}")

    print()

    for trained_model in result.models:

        print(f"Estimator      : {trained_model.estimator.value}")
        print(f"Model          : {type(trained_model.model).__name__}")
        print(f"Training Time  : {trained_model.training_time:.6f} sec")
        print(f"Predictions    : {len(trained_model.predictions)}")
        print(f"Test Samples   : {len(trained_model.y_test)}")

        print("-" * 60)


if __name__ == "__main__":
    main()