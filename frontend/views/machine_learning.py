"""Machine learning results view."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from components.layout import render_page_header, render_section_header
from components.metrics import metric_grid


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _format_estimator_name(value: Any) -> str:
    """Convert a backend estimator identifier into a readable label."""

    if not value:
        return "—"
    return str(value).replace("_", " ").replace("-", " ").title()


def _format_number(value: Any, decimals: int = 2) -> str:
    try:
        return f"{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return "—"


def _format_time(value: Any) -> str:
    try:
        return f"{float(value):.2f} s"
    except (TypeError, ValueError):
        return "—"


def _metric_value(name: str, value: Any) -> str:
    if name.lower() in {"r2", "accuracy", "precision", "recall", "f1_score"}:
        return _format_number(value, 3)
    return _format_number(value, 2)


def _comparison_rows(evaluations: list[Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for evaluation in evaluations:
        item = _as_dict(evaluation)
        metrics = _as_dict(item.get("metrics"))
        row: dict[str, Any] = {
            "Model": _format_estimator_name(item.get("estimator")),
        }
        for name, value in metrics.items():
            row[name.replace("_", " ").upper()] = _metric_value(name, value)
        row["Training Time"] = _format_time(item.get("training_time"))
        rows.append(row)
    return rows


def _render_validation(validation: dict[str, Any]) -> None:
    render_section_header("Model Validation")
    if validation.get("valid") is True:
        st.success("Model pipeline validated successfully.")
    else:
        st.error("Model validation failed.")
        errors = _as_list(validation.get("errors"))
        if errors:
            for error in errors:
                st.error(str(error))
        else:
            st.caption("No validation details were returned.")

    warnings = _as_list(validation.get("warnings"))
    for warning in warnings:
        st.warning(str(warning))


def _render_best_model(best_model: dict[str, Any]) -> None:
    render_section_header("Best Model", "Selected by the backend evaluation process.")
    if not best_model:
        st.info("No best model is available for this analysis.")
        return

    metrics = _as_dict(best_model.get("metrics"))
    st.subheader(_format_estimator_name(best_model.get("estimator")))
    hidden_metric_keys = {"mse", "mean_squared_error"}
    prominent_metrics = {
        name: value
        for name, value in metrics.items()
        if str(name).strip().lower() not in hidden_metric_keys
    }

    if prominent_metrics:
        metric_grid(
            [
                {
                    "label": name.replace("_", " ").upper(),
                    "value": _metric_value(name, value),
                    "accent": "success",
                }
                for name, value in prominent_metrics.items()
            ],
            columns=min(4, max(1, len(prominent_metrics))),
        )
    else:
        st.caption("No evaluation metrics were returned for the selected model.")


def _render_interpretation(task_type: str) -> None:
    render_section_header("Model Interpretation")
    if task_type == "regression":
        st.info(
            "MAE is the average absolute prediction error in the target's units. "
            "RMSE gives larger errors more weight. R² indicates the proportion "
            "of target variation explained on the evaluation data."
        )
    elif task_type == "classification":
        st.info(
            "Classification metrics describe how predictions compare with the "
            "held-out evaluation data. The displayed metrics are returned by the backend."
        )
    else:
        st.info("Metric definitions depend on the task type reported by the backend.")


def render(result: dict[str, Any]) -> None:
    """Render ML outputs defensively from the platform response."""

    render_page_header(
        "Machine Learning",
        "Evaluate predictive models and understand their performance.",
    )

    ml = _as_dict(_as_dict(result).get("ml"))
    if not ml:
        st.info("Machine learning results are not available for this analysis.")
        return

    task_type = str(ml.get("task_type") or "Not available")
    models_trained = ml.get("models_trained", 0)
    training_rows = ml.get("training_rows", 0)
    testing_rows = ml.get("testing_rows", 0)

    render_section_header("ML Overview")
    metric_grid(
        [
            {"label": "Task Type", "value": task_type.replace("_", " ").title(), "accent": "primary"},
            {"label": "Models Trained", "value": models_trained or "—", "accent": "primary"},
            {"label": "Training Rows", "value": _format_number(training_rows, 0), "accent": "primary"},
            {"label": "Testing Rows", "value": _format_number(testing_rows, 0), "accent": "primary"},
        ],
        columns=4,
    )

    _render_validation(_as_dict(ml.get("validation")))

    evaluations = _as_list(ml.get("evaluations"))
    render_section_header("Model Comparison")
    rows = _comparison_rows(evaluations)
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No model evaluations are available for this analysis.")

    _render_best_model(_as_dict(ml.get("best_model")))
    _render_interpretation(task_type.lower())

    render_section_header("Training / Evaluation Summary")
    st.caption(
        f"Models were trained using {_format_number(training_rows, 0)} rows and "
        f"evaluated on {_format_number(testing_rows, 0)} rows. "
        f"{models_trained or 0} candidate model(s) were evaluated for a {task_type} task."
    )

    warnings = _as_list(ml.get("warnings"))
    if warnings:
        render_section_header("Warnings")
        for warning in warnings:
            st.warning(str(warning))

    with st.expander("Technical Details"):
        st.json(ml)
