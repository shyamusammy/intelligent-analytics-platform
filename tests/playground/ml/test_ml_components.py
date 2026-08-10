from pandas import DataFrame

from app.services.ml.engine import MLEngine

def invalid_dataset() -> DataFrame:

    return DataFrame(
        {
            "feature_1": [1, 2, 3, 4, 5],
            "feature_2": [10, 20, 30, 40, 50],
            "target": [100, 200, 300, 400, 500],
        }
    )

def regression_dataset() -> DataFrame:

    return DataFrame(
        {
            "experience": [
                1,2,3,4,5,
                6,7,8,9,10,
                11,12,13,14,15,
                16,17,18,19,20,
                21,22,23,24,25,
                26,27,28,29,30,
            ],

            "education": [
                10,10,10,11,11,
                11,12,12,12,13,
                13,13,14,14,14,
                15,15,15,16,16,
                16,17,17,17,18,
                18,18,19,19,20,
            ],

            "salary": [
                30000,35000,40000,45000,50000,
                55000,60000,65000,70000,75000,
                80000,85000,90000,95000,100000,
                105000,110000,115000,120000,125000,
                130000,135000,140000,145000,150000,
                155000,160000,165000,170000,175000,
            ],
        }
    )

def classification_dataset() -> DataFrame:

    return DataFrame(
        {
            "age": [
                18,20,22,24,26,
                28,30,32,34,36,
                38,40,42,44,46,
                48,50,52,54,56,
                58,60,62,64,66,
                68,70,72,74,76,
            ],
            "income": [
                20,22,24,26,28,
                30,32,34,36,38,
                40,42,44,46,48,
                50,52,54,56,58,
                60,62,64,66,68,
                70,72,74,76,78,
            ],
            "purchased": [
                0,0,0,0,0,
                0,0,0,0,0,
                0,0,0,0,0,
                1,1,1,1,1,
                1,1,1,1,1,
                1,1,1,1,1,
            ],
        }
    )


def print_result(title, result):

    print("=" * 70)
    print(title)
    print("=" * 70)

    print()

    print(f"Validation      : {result.validation.valid}")

    if not result.validation.valid:

        print()

        print("Errors")

        for error in result.validation.errors:

            print(f"- {error}")

        return

    print(f"Detected Task   : {result.task_type.value}")

    print()

    print("Selected Models")

    for estimator in result.estimators:

        print(f"- {estimator.value}")

    print()

    print("Evaluation")

    print("-" * 70)

    for model in result.evaluation_result.models:

        metrics = model.metrics

        print(f"Estimator : {model.trained_model.estimator.value}")

        if result.task_type.value == "regression":

            print(f"R²   : {metrics.r2:.4f}")
            print(f"RMSE : {metrics.rmse:.4f}")

        else:

            print(f"Accuracy : {metrics.accuracy:.4f}")
            print(f"F1 Score : {metrics.f1_score:.4f}")

        print("-" * 70)

    print()

    print(
        "Best Model      : "
        f"{result.evaluation_result.best_model.trained_model.estimator.value}"
    )

    print()


def main():

    engine = MLEngine()
    
    # Invalid Dataset
    invalid_result = engine.run(
        dataframe=invalid_dataset(),
        target_column="target",
    )

    print_result(
        "Invalid Dataset",
        invalid_result,
    )

    regression_result = engine.run(
        dataframe=regression_dataset(),
        target_column="salary",
    )

    print_result(
        "Regression Dataset",
        regression_result,
    )

    classification_result = engine.run(
        dataframe=classification_dataset(),
        target_column="purchased",
    )

    print_result(
        "Classification Dataset",
        classification_result,
    )


if __name__ == "__main__":
    main()