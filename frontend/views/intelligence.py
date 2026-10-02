"""Business-facing synthesis of platform insight results."""

from __future__ import annotations

from typing import Any

import streamlit as st

from components.intelligence import (
    render_executive_summary,
    render_insight,
    render_insights,
)
from components.layout import render_page_header, render_section_header


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _severity(value: Any) -> str:
    """Map backend severity labels to the shared card vocabulary."""

    normalized = str(value or "info").lower()
    if normalized in {"high", "medium"}:
        return "warning"
    return normalized if normalized in {"info", "warning", "danger", "success"} else "info"


def _format_estimator(value: Any) -> str:
    return str(value).replace("_", " ").title() if value else "—"


def _format_metric(name: str, value: Any) -> str:
    try:
        decimals = 3 if name.lower() in {"r2", "accuracy", "precision", "recall", "f1_score"} else 2
        return f"{float(value):,.{decimals}f}"
    except (TypeError, ValueError):
        return "—"


def _model_finding(ml: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
    best_model = _as_dict(ml.get("best_model"))
    metrics = _as_dict(best_model.get("metrics"))
    task_type = str(ml.get("task_type") or "").lower()
    if not best_model:
        return None

    description = f"The selected model is {_format_estimator(best_model.get('estimator'))}."
    if task_type == "regression" and "r2" in metrics:
        description += f" It explains {_format_metric('r2', metrics['r2'])} of target variation on the evaluation data."
    elif task_type == "classification" and "accuracy" in metrics:
        description += f" It reports evaluation accuracy of {_format_metric('accuracy', metrics['accuracy'])}."
    return description, metrics


def render(result: dict[str, Any]) -> None:
    """Render concise, data-driven business insights."""

    render_page_header(
        "Business Insights",
        "Turn analytical results into clear business findings and areas for attention.",
    )

    payload = _as_dict(result)
    analytics = _as_dict(payload.get("analytics"))
    insight_result = _as_dict(analytics.get("insights"))
    insights = [item for item in _as_list(insight_result.get("insights")) if isinstance(item, dict)]
    ml = _as_dict(payload.get("ml"))

    if not insights and not ml:
        st.info("Business insights are not available for this analysis.")
        return

    render_section_header("Executive Summary")
    if insights:
        titles = [str(item.get("title", "Finding")) for item in insights[:5]]
        render_executive_summary(
            "Analysis generated "
            f"{len(insights)} finding(s), including: {', '.join(titles)}."
        )
    else:
        render_executive_summary("Analysis completed, with model results available below.")

    render_section_header("Key Data Findings")
    data_findings = [
        item for item in insights
        if str(item.get("category", "")).lower() in {"correlation", "segmentation", "dataset", "trend"}
    ]
    if data_findings:
        render_insights(data_findings, max_items=5)
    else:
        st.info("No additional analytical findings were returned for this dataset.")

    render_section_header("Model Findings")
    model_finding = _model_finding(ml)
    if model_finding:
        description, metrics = model_finding
        render_insight(
            title="Selected Model",
            description=description,
            severity="info",
            category=str(ml.get("task_type") or "model"),
            evidence={name.upper(): _format_metric(name, value) for name, value in metrics.items() if name.lower() != "mse"},
        )
    else:
        st.info("Machine learning results are not available for this analysis.")

    render_section_header("Areas to Watch")
    attention_items = [
        item for item in insights
        if str(item.get("severity", "")).lower() in {"high", "medium", "warning", "danger"}
    ]
    validation = _as_dict(ml.get("validation"))
    warnings = _as_list(validation.get("warnings")) + _as_list(payload.get("warnings"))
    if attention_items:
        for item in attention_items[:5]:
            render_insight(
                title=str(item.get("title", "Area to Watch")),
                description=str(item.get("description", "")),
                severity=_severity(item.get("severity")),
                category=str(item.get("category", "")),
            )
    if warnings:
        for warning in warnings:
            st.warning(str(warning))
    if not attention_items and not warnings:
        st.info("No elevated areas for attention were returned by the analysis.")

    if data_findings:
        render_section_header("Questions for Further Analysis")
        for item in data_findings[:3]:
            st.caption(
                f"• What factors may explain the finding: {item.get('title', 'this result')}?"
            )

    with st.expander("View Detailed Insights"):
        if insights:
            rows = [
                {
                    "Title": item.get("title", "Insight"),
                    "Category": item.get("category", ""),
                    "Severity": item.get("severity", ""),
                    "Finding": item.get("description", ""),
                }
                for item in insights
            ]
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.caption("No detailed insight objects were returned.")
