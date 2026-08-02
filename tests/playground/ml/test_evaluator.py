from pandas import DataFrame

from app.core.enums import MLEstimator
from app.core.enums import MLTaskType

from app.services.ml.trainer import ModelTrainer
from app.services.ml.evaluator import ModelEvaluator


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

    train_result = trainer.train(
        dataframe=regression_dataset(),
        target_column="salary",
        estimators=[
            MLEstimator.LINEAR_REGRESSION,
            MLEstimator.RANDOM_FOREST_REGRESSOR,
        ],
    )

    evaluator = ModelEvaluator()

    evaluation_result = evaluator.evaluate(
        MLTaskType.REGRESSION,
        train_result,
    )

    print("=" * 70)
    print("Evaluation Results")
    print("=" * 70)

    print()

    for model in evaluation_result.models:

        metrics = model.metrics

        print(f"Estimator      : {model.trained_model.estimator.value}")
        print(f"Training Time  : {model.trained_model.training_time:.6f} sec")
        print(f"MAE            : {metrics.mae:.4f}")
        print(f"MSE            : {metrics.mse:.4f}")
        print(f"RMSE           : {metrics.rmse:.4f}")
        print(f"R² Score       : {metrics.r2:.4f}")

        print("-" * 70)

    print()

    print("Best Model")
    print("-" * 70)

    print(
        evaluation_result.best_model.trained_model.estimator.value
    )


if __name__ == "__main__":
    main()