"""JSON-safe response builders for results containing trained estimators."""

from app.schemas.ml import MLEngineResult
from app.schemas.pipeline import PlatformPipelineResult


def ml_result_response(result: MLEngineResult) -> dict:
    """Return ML metadata and metrics without serializing estimator objects."""

    response = {
        "validation": result.validation.model_dump(mode="json"),
        "task_type": result.task_type.value if result.task_type else None,
        "estimators": [estimator.value for estimator in result.estimators],
        "models_trained": len(result.train_result.models) if result.train_result else 0,
        "training_rows": result.train_result.training_rows if result.train_result else 0,
        "testing_rows": result.train_result.testing_rows if result.train_result else 0,
        "evaluations": [],
        "best_model": None,
        "feature_engineering": result.feature_engineering.model_dump(mode="json") if result.feature_engineering else None,
    }

    if not result.evaluation_result:
        return response

    for evaluated in result.evaluation_result.models:
        response["evaluations"].append(
            {
                "estimator": evaluated.trained_model.estimator.value,
                "metrics": evaluated.metrics.model_dump(mode="json"),
                "training_time": evaluated.trained_model.training_time,
            }
        )

    best = result.evaluation_result.best_model
    response["best_model"] = {
        "estimator": best.trained_model.estimator.value,
        "metrics": best.metrics.model_dump(mode="json"),
    }
    return response


def platform_result_response(result: PlatformPipelineResult) -> dict:
    """Return all pipeline outputs in a response safe for JSON encoding."""

    return {
        "etl": result.etl.model_dump(mode="json"),
        "cleaning": result.cleaning.model_dump(mode="json") if result.cleaning else None,
        "analytics": result.analytics.model_dump(mode="json"),
        "ml": ml_result_response(result.ml) if result.ml else None,
        "dashboard": result.dashboard.model_dump(mode="json") if result.dashboard else None,
        "feature_engineering": result.feature_engineering.model_dump(mode="json") if result.feature_engineering else None,
        "status": result.status,
        "warnings": result.warnings,
    }
