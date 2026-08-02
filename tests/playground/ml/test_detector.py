from pandas import DataFrame

from app.services.ml.detector import MLDetector


def run_test(
    name: str,
    dataframe: DataFrame,
    target_column: str
):

    detector = MLDetector()

    print("=" * 70)
    print(name)
    print("=" * 70)

    print(f"Rows: {len(dataframe)}")

    print(
        "Numeric:",
        detector._is_numeric_target(
            dataframe,
            target_column
        )
    )

    print(
        "Unique Values:",
        detector._get_unique_values(
            dataframe,
            target_column
        )
    )

    print(
        "Unique Ratio:",
        round(
            detector._get_unique_ratio(
                dataframe,
                target_column
            ),
            4
        )
    )

    print(
        "Detected Task:",
        detector.detect(
            dataframe,
            target_column
        )
    )

    print()


def main():

    # ----------------------------------------------------
    # Regression (30 unique numeric values)
    # ----------------------------------------------------

    regression_df = DataFrame({
        "Revenue": list(range(100, 3100, 100))
    })

    run_test(
        "Regression",
        regression_df,
        "Revenue"
    )

    # ----------------------------------------------------
    # Binary Classification
    # ----------------------------------------------------

    binary_df = DataFrame({
        "Purchased": [0, 1] * 15
    })

    run_test(
        "Binary Classification",
        binary_df,
        "Purchased"
    )

    # ----------------------------------------------------
    # Text Classification
    # ----------------------------------------------------

    text_df = DataFrame({
        "Risk": (
            ["Low"] * 10 +
            ["Medium"] * 10 +
            ["High"] * 10
        )
    })

    run_test(
        "Text Classification",
        text_df,
        "Risk"
    )

    # ----------------------------------------------------
    # Multi-class Classification
    # ----------------------------------------------------

    multiclass_df = DataFrame({
        "Priority": [1, 2, 3] * 10
    })

    run_test(
        "Multi-class Classification",
        multiclass_df,
        "Priority"
    )


if __name__ == "__main__":
    main()