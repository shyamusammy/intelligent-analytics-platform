from app.core.enums import MLTaskType
from app.services.ml.selector import ModelSelector


def run_test(
    name: str,
    task_type: MLTaskType
):

    selector = ModelSelector()

    models = selector.select(
        task_type
    )

    print("=" * 60)
    print(name)
    print("=" * 60)

    print(f"Task Type: {task_type.value}")

    print("\nSelected Models:")

    for model in models:
        print(f"- {model.value}")

    print(f"\nTotal Models: {len(models)}")
    print()


def main():

    run_test(
        "Classification",
        MLTaskType.CLASSIFICATION
    )

    run_test(
        "Regression",
        MLTaskType.REGRESSION
    )


if __name__ == "__main__":
    main()