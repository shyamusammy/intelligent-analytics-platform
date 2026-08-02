from pandas import DataFrame

from app.core.enums import MLEstimator
from app.core.enums import MLTaskType

from app.services.ml.trainer import ModelTrainer
from app.services.ml.evaluator import ModelEvaluator


def classification_dataset() -> DataFrame:

    return DataFrame(
        {
            "age": [
                18, 20, 22, 24, 26,
                28, 30, 32, 34, 36,
                38, 40, 42, 44, 46,
                48, 50, 52, 54, 56,
                58, 60, 62, 64, 66,
                68, 70, 72, 74, 76,
            ],
            "income": [
                20, 22, 24, 26, 28,
                30, 32, 34, 36, 38,
                40, 42, 44, 46, 48,
                50, 52, 54, 56, 58,
                60, 62, 64, 66, 68,
                70, 72, 74, 76, 78,
            ],
            "purchased": [
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                1, 1, 1, 1, 1,
                1, 1, 1, 1, 1,
                1, 1, 1, 1, 1,
            ],
        }
    )


def main():

    trainer = ModelTrainer()

    train_result = trainer.train(
        dataframe=classification_dataset(),
        target_column="purchased",
        estimators=[
            MLEstimator.LOGISTIC_REGRESSION,
            MLEstimator.RANDOM_FOREST_CLASSIFIER,
        ],
    )

    evaluator = ModelEvaluator()

    evaluation_result = evaluator.evaluate(
        MLTaskType.CLASSIFICATION,
        train_result,
    )

    print("=" * 70)
    print("Classification Evaluation")
    print("=" * 70)

    print()

    for model in evaluation_result.models:

        metrics = model.metrics

        print(f"Estimator      : {model.trained_model.estimator.value}")
        print(f"Training Time  : {model.trained_model.training_time:.6f} sec")
        print(f"Accuracy       : {metrics.accuracy:.4f}")
        print(f"Precision      : {metrics.precision:.4f}")
        print(f"Recall         : {metrics.recall:.4f}")
        print(f"F1 Score       : {metrics.f1_score:.4f}")

        print("-" * 70)

    print()

    print("Best Model")
    print("-" * 70)
    print(
        evaluation_result.best_model.trained_model.estimator.value
    )


if __name__ == "__main__":
    main()