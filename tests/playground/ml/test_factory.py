from app.core.enums import MLEstimator
from app.services.ml.factory import ModelFactory


def run_test(
    estimator: MLEstimator
):

    model = ModelFactory.create(
        estimator
    )

    print("=" * 60)
    print(f"Estimator: {estimator.value}")
    print(f"Model Type: {type(model).__name__}")
    print()


def main():

    estimators = [
        MLEstimator.LINEAR_REGRESSION,
        MLEstimator.LOGISTIC_REGRESSION,
        MLEstimator.RANDOM_FOREST_REGRESSOR,
        MLEstimator.RANDOM_FOREST_CLASSIFIER,
    ]

    for estimator in estimators:
        run_test(estimator)


if __name__ == "__main__":
    main()
try:
    ModelFactory.create("invalid")  # type: ignore
except ValueError as e:
    print("=" * 60)
    print("Error Test")
    print("=" * 60)
    print(e)