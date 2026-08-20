"""
Intelligent Analytics Platform
Reusable business intelligence and insight components.
"""

import html

import streamlit as st

from styles.theme import COLORS


# ============================================================
# HELPERS
# ============================================================

SEVERITY_CONFIG = {
    "critical": {
        "color": COLORS["danger"],
        "background": COLORS["danger_soft"],
        "icon": "!",
        "label": "Critical",
    },
    "danger": {
        "color": COLORS["danger"],
        "background": COLORS["danger_soft"],
        "icon": "!",
        "label": "Critical",
    },
    "warning": {
        "color": COLORS["warning"],
        "background": COLORS["warning_soft"],
        "icon": "!",
        "label": "Warning",
    },
    "success": {
        "color": COLORS["success"],
        "background": COLORS["success_soft"],
        "icon": "✓",
        "label": "Positive",
    },
    "info": {
        "color": COLORS["info"],
        "background": COLORS["info_soft"],
        "icon": "i",
        "label": "Info",
    },
}


def _severity_config(severity: str) -> dict:
    """Return visual configuration for an insight severity."""

    normalized = str(severity or "info").lower().strip()

    return SEVERITY_CONFIG.get(
        normalized,
        SEVERITY_CONFIG["info"],
    )


def _safe(value) -> str:
    """Safely escape text before rendering HTML."""

    if value is None:
        return ""

    return html.escape(str(value))


# ============================================================
# INSIGHT CARD
# ============================================================

def render_insight(
    title: str,
    description: str,
    severity: str = "info",
    category: str | None = None,
    recommendation: str | None = None,
    evidence: dict | None = None,
) -> None:
    """
    Render one structured business insight.

    Parameters
    ----------
    title:
        Short insight title.

    description:
        Explanation of the finding.

    severity:
        critical | warning | success | info

    category:
        Optional insight category.

    recommendation:
        Optional recommended action.

    evidence:
        Optional metric/value dictionary.
    """

    config = _severity_config(severity)

    title = _safe(title)
    description = _safe(description)

    category_html = ""

    if category:
        category_html = f"""
        <span style="
            color: {COLORS["text_muted"]};
            font-size: 0.68rem;
            font-weight: 650;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-left: 0.5rem;
        ">
            {_safe(category)}
        </span>
        """

    recommendation_html = ""

    if recommendation:
        recommendation_html = f"""
        <div style="
            margin-top: 0.85rem;
            padding-top: 0.75rem;
            border-top: 1px solid {COLORS["border"]};
        ">
            <div style="
                color: {COLORS["text"]};
                font-size: 0.76rem;
                font-weight: 700;
                margin-bottom: 0.2rem;
            ">
                Recommended action
            </div>

            <div style="
                color: {COLORS["text_secondary"]};
                font-size: 0.8rem;
                line-height: 1.45;
            ">
                {_safe(recommendation)}
            </div>
        </div>
        """

    evidence_html = ""

    if evidence:

        evidence_items = []

        for key, value in evidence.items():

            evidence_items.append(
                f"""
                <div style="
                    background: {COLORS["surface_alt"]};
                    border-radius: 7px;
                    padding: 0.45rem 0.65rem;
                ">
                    <div style="
                        color: {COLORS["text_muted"]};
                        font-size: 0.65rem;
                    ">
                        {_safe(key)}
                    </div>

                    <div style="
                        color: {COLORS["text"]};
                        font-size: 0.78rem;
                        font-weight: 700;
                        margin-top: 2px;
                    ">
                        {_safe(value)}
                    </div>
                </div>
                """
            )

        evidence_html = f"""
        <div style="
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.8rem;
        ">
            {"".join(evidence_items)}
        </div>
        """

    st.markdown(
        f"""
        <div style="
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border"]};
            border-left: 4px solid {config["color"]};
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.75rem;
        ">

            <div style="
                display: flex;
                align-items: flex-start;
                gap: 0.75rem;
            ">

                <div style="
                    flex-shrink: 0;
                    width: 26px;
                    height: 26px;
                    border-radius: 50%;
                    background: {config["background"]};
                    color: {config["color"]};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 0.78rem;
                    font-weight: 750;
                ">
                    {config["icon"]}
                </div>

                <div style="flex: 1;">

                    <div style="
                        display: flex;
                        align-items: center;
                        flex-wrap: wrap;
                        gap: 0.35rem;
                    ">

                        <div style="
                            color: {COLORS["text"]};
                            font-size: 0.92rem;
                            font-weight: 700;
                        ">
                            {title}
                        </div>

                        <span style="
                            color: {config["color"]};
                            background: {config["background"]};
                            padding: 2px 7px;
                            border-radius: 999px;
                            font-size: 0.64rem;
                            font-weight: 700;
                        ">
                            {config["label"]}
                        </span>

                        {category_html}

                    </div>

                    <div style="
                        color: {COLORS["text_secondary"]};
                        font-size: 0.82rem;
                        line-height: 1.5;
                        margin-top: 0.35rem;
                    ">
                        {description}
                    </div>

                    {evidence_html}
                    {recommendation_html}

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# INSIGHT LIST
# ============================================================

def render_insights(
    insights: list[dict],
    max_items: int | None = None,
) -> None:
    """
    Render a list of structured insights.

    Expected format:

    [
        {
            "title": "...",
            "description": "...",
            "severity": "warning",
            "category": "data_quality",
            "recommendation": "...",
            "evidence": {
                "skewness": "59.06"
            }
        }
    ]
    """

    if not insights:
        st.info("No significant insights were generated.")

        return

    visible_insights = insights

    if max_items is not None:
        visible_insights = insights[:max_items]

    for insight in visible_insights:

        if not isinstance(insight, dict):
            continue

        render_insight(
            title=insight.get(
                "title",
                "Insight",
            ),
            description=insight.get(
                "description",
                "",
            ),
            severity=insight.get(
                "severity",
                "info",
            ),
            category=insight.get(
                "category",
            ),
            recommendation=insight.get(
                "recommendation",
            ),
            evidence=insight.get(
                "evidence",
            ),
        )


# ============================================================
# EXECUTIVE SUMMARY CARD
# ============================================================

def render_executive_summary(
    summary: str,
    title: str = "Executive Summary",
) -> None:
    """Render a prominent executive-level summary."""

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(
                135deg,
                {COLORS["primary_soft"]} 0%,
                {COLORS["surface"]} 100%
            );
            border: 1px solid #BFDBFE;
            border-radius: 14px;
            padding: 1.25rem 1.35rem;
            margin-bottom: 1.25rem;
        ">

            <div style="
                color: {COLORS["primary"]};
                font-size: 0.72rem;
                font-weight: 750;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-bottom: 0.45rem;
            ">
                {html.escape(title)}
            </div>

            <div style="
                color: {COLORS["text"]};
                font-size: 0.95rem;
                line-height: 1.6;
            ">
                {html.escape(summary)}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# INSIGHT SUMMARY
# ============================================================

def render_insight_summary(
    critical: int = 0,
    warnings: int = 0,
    positive: int = 0,
    info: int = 0,
) -> None:
    """Render a compact summary of insight severity."""

    metrics = [
        (
            "Critical",
            critical,
            COLORS["danger"],
            COLORS["danger_soft"],
        ),
        (
            "Warnings",
            warnings,
            COLORS["warning"],
            COLORS["warning_soft"],
        ),
        (
            "Positive",
            positive,
            COLORS["success"],
            COLORS["success_soft"],
        ),
        (
            "Information",
            info,
            COLORS["info"],
            COLORS["info_soft"],
        ),
    ]

    cols = st.columns(4)

    for col, (label, value, color, background) in zip(
        cols,
        metrics,
    ):

        with col:

            st.markdown(
                f"""
                <div style="
                    background: {background};
                    border-radius: 10px;
                    padding: 0.7rem 0.8rem;
                    text-align: center;
                ">

                    <div style="
                        color: {color};
                        font-size: 1.15rem;
                        font-weight: 750;
                    ">
                        {value}
                    </div>

                    <div style="
                        color: {COLORS["text_secondary"]};
                        font-size: 0.7rem;
                        margin-top: 2px;
                    ">
                        {label}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )