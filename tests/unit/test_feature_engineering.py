import pandas as pd
import pytest

from app.schemas.context import KnowledgeContext
from app.services.feature_engineering import FeatureEngineeringEngine
from app.services.feature_engineering.detector import FeatureDetector


def test_detector_identifies_and_excludes_feature_types() -> None:
    dataframe = pd.DataFrame({
        "record_id": [1, 2, 3, 4],
        "amount": [10.0, 11.0, 12.0, 13.0],
        "segment": ["a", "b", "a", "b"],
        "constant": [1, 1, 1, 1],
    })
    groups, removed = FeatureDetector().detect(dataframe)
    assert groups["numeric"] == ["amount"]
    assert groups["categorical"] == ["segment"]
    assert {item.column for item in removed} == {"record_id", "constant"}


def test_fit_transform_generates_datetime_and_handles_unseen_categories() -> None:
    train = pd.DataFrame({
        "amount": [1.0, 2.0, 3.0, 4.0],
        "segment": ["a", "b", "a", "b"],
        "event_date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]),
    })
    test = pd.DataFrame({
        "amount": [5.0],
        "segment": ["unseen"],
        "event_date": pd.to_datetime(["2024-02-01"]),
    })
    engine = FeatureEngineeringEngine()
    transformed_train = engine.fit_transform(train, "target", KnowledgeContext())
    transformed_test = engine.transform(test, "target")
    assert list(transformed_train.columns) == list(transformed_test.columns)
    assert "event_date__month" in transformed_train.columns
    assert engine.report.validation.valid


def test_high_cardinality_and_target_leakage_are_protected() -> None:
    train = pd.DataFrame({
        "amount": [float(value) for value in range(60)],
        "category": [f"item_{value}" for value in range(60)],
    })
    engine = FeatureEngineeringEngine()
    transformed = engine.fit_transform(train, "target", KnowledgeContext())
    assert "category" not in transformed.columns
    assert any(item.reason == "high_cardinality" for item in engine.report.removed_columns)
    with pytest.raises(ValueError, match="Target leakage"):
        engine.transform(train.assign(target=1), "target")
