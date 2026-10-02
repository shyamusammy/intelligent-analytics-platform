import pandas as pd

from app.services.etl.quality.outlier_cleaner import OutlierCleaner


def test_outlier_cleaner_edge_cases() -> None:
    cleaner = OutlierCleaner()

    dataframe = pd.DataFrame(
        {
            "age": [5, 6, 7, 8, 9, 100],
            "salary": [40000, 45000, 50000, 55000, 60000, 1000000],
            "category": [
                "A",
                "A",
                "B",
                "B",
                "C",
                "C",
            ],
            "constant": [5, 5, 5, 5, 5, 5],
            "missing": [1, 2, None, 4, 5, 6],
        }
    )

    # ---------------------------------------------------------
    # 1. KEEP
    # ---------------------------------------------------------
    kept = cleaner.clean(
        dataframe,
        strategy="keep",
    )

    assert kept.equals(dataframe)

    # ---------------------------------------------------------
    # 2. CAP
    # ---------------------------------------------------------
    capped = cleaner.clean(
        dataframe,
        strategy="cap",
    )

    # age = 100 should be capped
    assert capped["age"].max() < 100

    # salary = 1,000,000 should be capped
    assert capped["salary"].max() < 1_000_000

    # categorical columns must remain unchanged
    assert capped["category"].equals(
        dataframe["category"]
    )

    # constant column must remain unchanged
    assert capped["constant"].equals(
        dataframe["constant"]
    )

    # missing values must remain missing
    assert pd.isna(capped["missing"].iloc[2])

    # ---------------------------------------------------------
    # 3. MEDIAN
    # ---------------------------------------------------------
    median_cleaned = cleaner.clean(
        dataframe,
        strategy="median",
    )

    assert median_cleaned["age"].max() < 100
    assert median_cleaned["salary"].max() < 1_000_000

    # ---------------------------------------------------------
    # 4. PROTECTED COLUMN
    # ---------------------------------------------------------
    protected = cleaner.clean(
        dataframe,
        strategy="cap",
        protected_columns={"age"},
    )

    # age outlier must remain untouched
    assert protected["age"].iloc[-1] == 100

    # salary can still be cleaned
    assert protected["salary"].max() < 1_000_000

    # ---------------------------------------------------------
    # 5. INVALID STRATEGY
    # ---------------------------------------------------------
    try:
        cleaner.clean(
            dataframe,
            strategy="remove",  # type: ignore[arg-type]
        )
        raise AssertionError(
            "Expected ValueError for unsupported strategy"
        )
    except ValueError:
        pass

    print("=" * 80)
    print("OUTLIER CLEANER — EDGE-CASE TEST")
    print("=" * 80)

    print("Original age maximum :", dataframe["age"].max())
    print("Capped age maximum   :", capped["age"].max())
    print(
        "Original salary maximum :",
        dataframe["salary"].max(),
    )
    print(
        "Capped salary maximum   :",
        capped["salary"].max(),
    )

    print("-" * 80)
    print("✓ KEEP strategy passed")
    print("✓ CAP strategy passed")
    print("✓ MEDIAN strategy passed")
    print("✓ Protected-column test passed")
    print("✓ Constant-column test passed")
    print("✓ Missing-value preservation passed")
    print("✓ Invalid-strategy validation passed")
    print("✓ OutlierCleaner edge-case test passed")
    print("=" * 80)


if __name__ == "__main__":
    test_outlier_cleaner_edge_cases()