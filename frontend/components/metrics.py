"""
Intelligent Analytics Platform
Reusable metric and KPI components.

All components render through Streamlit and support
the existing Overview page component API.
"""

from __future__ import annotations

from html import escape
from typing import Any

import streamlit as st

from styles.theme import COLORS


# ============================================================
# THEME HELPERS
# ============================================================

def _get_color(name: str, fallback: str) -> str:
    """
    Safely retrieve a color from the application theme.
    """

    try:
        value = COLORS.get(name)

        if value:
            return value

    except AttributeError:
        pass

    return fallback


def _safe(value: Any) -> str:
    """
    Convert a value to HTML-safe text.
    """

    if value is None:
        return "—"

    return escape(str(value))


def _normalize_accent(accent: str | None) -> str:
    """
    Convert semantic accent names into HEX colors.
    """

    if not accent:
        return _get_color(
            "PRIMARY",
            "#0284C7",
        )

    accent_value = str(accent).strip()
    accent_lower = accent_value.lower()

    # --------------------------------------------------------
    # Direct HEX color
    # --------------------------------------------------------

    if accent_lower.startswith("#"):
        return accent_value

    # --------------------------------------------------------
    # Semantic colors
    # --------------------------------------------------------

    accent_map = {

        "primary": _get_color(
            "PRIMARY",
            "#0284C7",
        ),

        "blue": _get_color(
            "PRIMARY",
            "#0284C7",
        ),

        "success": _get_color(
            "SUCCESS",
            "#16A34A",
        ),

        "green": _get_color(
            "SUCCESS",
            "#16A34A",
        ),

        "warning": _get_color(
            "WARNING",
            "#D97706",
        ),

        "orange": _get_color(
            "WARNING",
            "#D97706",
        ),

        "danger": _get_color(
            "DANGER",
            "#DC2626",
        ),

        "error": _get_color(
            "DANGER",
            "#DC2626",
        ),

        "red": _get_color(
            "DANGER",
            "#DC2626",
        ),

        "info": _get_color(
            "INFO",
            "#2563EB",
        ),

        "purple": _get_color(
            "PURPLE",
            "#7C3AED",
        ),

        "neutral": _get_color(
            "TEXT_MUTED",
            "#64748B",
        ),

        "gray": _get_color(
            "TEXT_MUTED",
            "#64748B",
        ),
    }

    return accent_map.get(
        accent_lower,
        _get_color(
            "PRIMARY",
            "#0284C7",
        ),
    )


# ============================================================
# HTML RENDERER
# ============================================================

def _render_html(content: str) -> None:
    """
    Render HTML using Streamlit's native HTML renderer.

    IMPORTANT:
    Do NOT use st.markdown() here.

    st.html() prevents the metric components from appearing
    as literal HTML/code on the page.
    """

    try:
        st.html(content)

    except AttributeError:
        # Compatibility fallback for older Streamlit versions.
        st.markdown(
            content,
            unsafe_allow_html=True,
        )


# ============================================================
# BASIC METRIC CARD
# ============================================================

def metric_card(
    label: str,
    value: str | int | float,
    description: str | None = None,
    status: str | None = None,
    accent: str = "primary",
) -> None:
    """
    Render a single metric card.
    """

    accent_color = _normalize_accent(
        accent
    )

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------

    description_html = ""

    if description is not None:

        description_html = f"""
        <div style="
            color:#64748B;
            font-size:0.75rem;
            line-height:1.4;
            margin-top:0.45rem;
        ">
            {_safe(description)}
        </div>
        """

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    status_html = ""

    if status is not None:

        status_html = f"""
        <div style="
            display:inline-flex;
            align-items:center;
            margin-top:0.65rem;
            padding:0.25rem 0.55rem;
            border-radius:999px;
            background:{accent_color}12;
            color:{accent_color};
            font-size:0.68rem;
            font-weight:700;
            line-height:1;
        ">
            {_safe(status)}
        </div>
        """

    # --------------------------------------------------------
    # Card
    # --------------------------------------------------------

    html = f"""
    <div style="
        position:relative;
        width:100%;
        min-height:128px;
        box-sizing:border-box;
        padding:1rem 1.05rem 0.95rem 1.15rem;
        background:#FFFFFF;
        border:1px solid #E2E8F0;
        border-radius:10px;
        overflow:hidden;
        box-shadow:0 1px 2px rgba(15,23,42,0.03);
    ">

        <!-- Accent bar -->

        <div style="
            position:absolute;
            left:0;
            top:0;
            bottom:0;
            width:4px;
            background:{accent_color};
        "></div>

        <!-- Header -->

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:0.5rem;
        ">

            <div style="
                color:#64748B;
                font-size:0.68rem;
                font-weight:700;
                text-transform:uppercase;
                letter-spacing:0.05em;
            ">
                {_safe(label)}
            </div>

            <div style="
                width:7px;
                height:7px;
                border-radius:50%;
                background:{accent_color};
                flex-shrink:0;
            "></div>

        </div>

        <!-- Value -->

        <div style="
            color:#0F172A;
            font-size:1.55rem;
            font-weight:750;
            line-height:1.1;
            margin-top:0.5rem;
            overflow:hidden;
            text-overflow:ellipsis;
            white-space:nowrap;
        ">
            {_safe(value)}
        </div>

        <!-- Description -->

        {description_html}

        <!-- Status -->

        {status_html}

    </div>
    """

    _render_html(html)


# ============================================================
# COMPARISON CARD
# ============================================================

def comparison_card(
    label: str | None = None,
    before_label: str = "Before",
    before_value: Any = "—",
    after_label: str = "After",
    after_value: Any = "—",
    description: str | None = None,
    accent: str = "primary",
    title: str | None = None,
) -> None:
    """
    Render a before/after comparison card.

    Supports both:

        comparison_card(
            label="Quality Score",
            ...
        )

    and the existing Overview API:

        comparison_card(
            title="Quality Score",
            ...
        )

    This compatibility is intentional so existing Overview
    code does not need to be changed.
    """

    # --------------------------------------------------------
    # Resolve title / label
    # --------------------------------------------------------

    if title is not None:
        display_label = title

    elif label is not None:
        display_label = label

    else:
        display_label = "Comparison"

    accent_color = _normalize_accent(
        accent
    )

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------

    description_html = ""

    if description is not None:

        description_html = f"""
        <div style="
            color:#64748B;
            font-size:0.72rem;
            line-height:1.35;
            margin-top:0.55rem;
        ">
            {_safe(description)}
        </div>
        """

    # --------------------------------------------------------
    # Card
    # --------------------------------------------------------

    html = f"""
    <div style="
        position:relative;
        width:100%;
        min-height:150px;
        box-sizing:border-box;
        padding:1rem 1.1rem 1rem 1.15rem;
        background:#FFFFFF;
        border:1px solid #E2E8F0;
        border-radius:10px;
        overflow:hidden;
        box-shadow:0 1px 2px rgba(15,23,42,0.03);
    ">

        <!-- Accent -->

        <div style="
            position:absolute;
            left:0;
            top:0;
            bottom:0;
            width:4px;
            background:{accent_color};
        "></div>

        <!-- Title -->

        <div style="
            color:#64748B;
            font-size:0.68rem;
            font-weight:700;
            text-transform:uppercase;
            letter-spacing:0.05em;
        ">
            {_safe(display_label)}
        </div>

        <!-- Comparison -->

        <div style="
            display:flex;
            align-items:center;
            gap:0.9rem;
            margin-top:0.85rem;
        ">

            <!-- BEFORE -->

            <div style="
                flex:1;
                min-width:0;
            ">

                <div style="
                    color:#64748B;
                    font-size:0.68rem;
                    font-weight:650;
                    margin-bottom:0.3rem;
                ">
                    {_safe(before_label)}
                </div>

                <div style="
                    color:#0F172A;
                    font-size:1.35rem;
                    font-weight:750;
                    line-height:1.1;
                    overflow:hidden;
                    text-overflow:ellipsis;
                    white-space:nowrap;
                ">
                    {_safe(before_value)}
                </div>

            </div>

            <!-- ARROW -->

            <div style="
                color:#94A3B8;
                font-size:1.05rem;
                font-weight:700;
                flex-shrink:0;
                padding-top:0.8rem;
            ">
                →
            </div>

            <!-- AFTER -->

            <div style="
                flex:1;
                min-width:0;
            ">

                <div style="
                    color:#64748B;
                    font-size:0.68rem;
                    font-weight:650;
                    margin-bottom:0.3rem;
                ">
                    {_safe(after_label)}
                </div>

                <div style="
                    color:#0F172A;
                    font-size:1.35rem;
                    font-weight:750;
                    line-height:1.1;
                    overflow:hidden;
                    text-overflow:ellipsis;
                    white-space:nowrap;
                ">
                    {_safe(after_value)}
                </div>

            </div>

        </div>

        <!-- Description -->

        {description_html}

    </div>
    """

    _render_html(html)


# ============================================================
# COMPACT METRIC
# ============================================================

def compact_metric(
    label: str,
    value: str | int | float,
    description: str | None = None,
    accent: str = "primary",
) -> None:
    """
    Render a compact metric.
    """

    accent_color = _normalize_accent(
        accent
    )

    description_html = ""

    if description:

        description_html = f"""
        <div style="
            color:#64748B;
            font-size:0.72rem;
            margin-top:0.3rem;
            line-height:1.35;
        ">
            {_safe(description)}
        </div>
        """

    html = f"""
    <div style="
        position:relative;
        width:100%;
        min-height:92px;
        box-sizing:border-box;
        padding:0.85rem 1rem 0.8rem 1.1rem;
        background:#FFFFFF;
        border:1px solid #E2E8F0;
        border-radius:10px;
        overflow:hidden;
        box-shadow:0 1px 2px rgba(15,23,42,0.03);
    ">

        <div style="
            position:absolute;
            left:0;
            top:0;
            bottom:0;
            width:3px;
            background:{accent_color};
        "></div>

        <div style="
            color:#64748B;
            font-size:0.68rem;
            font-weight:700;
            text-transform:uppercase;
            letter-spacing:0.05em;
        ">
            {_safe(label)}
        </div>

        <div style="
            color:#0F172A;
            font-size:1.35rem;
            font-weight:750;
            line-height:1.15;
            margin-top:0.35rem;
            overflow:hidden;
            text-overflow:ellipsis;
            white-space:nowrap;
        ">
            {_safe(value)}
        </div>

        {description_html}

    </div>
    """

    _render_html(html)


# ============================================================
# STATUS BADGE
# ============================================================

def status_badge(
    text: str,
    status: str = "info",
) -> None:
    """
    Render a status badge.
    """

    status_lower = str(
        status
    ).lower().strip()

    status_colors = {

        "success": (
            _get_color(
                "SUCCESS",
                "#16A34A",
            ),
            "#F0FDF4",
        ),

        "complete": (
            _get_color(
                "SUCCESS",
                "#16A34A",
            ),
            "#F0FDF4",
        ),

        "warning": (
            _get_color(
                "WARNING",
                "#D97706",
            ),
            "#FFFBEB",
        ),

        "danger": (
            _get_color(
                "DANGER",
                "#DC2626",
            ),
            "#FEF2F2",
        ),

        "error": (
            _get_color(
                "DANGER",
                "#DC2626",
            ),
            "#FEF2F2",
        ),

        "info": (
            _get_color(
                "PRIMARY",
                "#0284C7",
            ),
            "#F0F9FF",
        ),

        "primary": (
            _get_color(
                "PRIMARY",
                "#0284C7",
            ),
            "#F0F9FF",
        ),

        "neutral": (
            _get_color(
                "TEXT_MUTED",
                "#64748B",
            ),
            "#F8FAFC",
        ),
    }

    text_color, background_color = status_colors.get(
        status_lower,
        status_colors["info"],
    )

    html = f"""
    <div style="
        display:inline-flex;
        align-items:center;
        gap:0.35rem;
        padding:0.3rem 0.65rem;
        border-radius:999px;
        background:{background_color};
        color:{text_color};
        border:1px solid {text_color}20;
        font-size:0.7rem;
        font-weight:700;
        line-height:1;
    ">

        <span style="
            width:6px;
            height:6px;
            border-radius:50%;
            background:{text_color};
            display:inline-block;
        "></span>

        {_safe(text)}

    </div>
    """

    _render_html(html)


# ============================================================
# KPI VALUE
# ============================================================

def kpi_value(
    label: str,
    value: str | int | float,
    delta: str | None = None,
    delta_type: str = "neutral",
) -> None:
    """
    Render a KPI value with optional delta.
    """

    delta_colors = {

        "positive": _get_color(
            "SUCCESS",
            "#16A34A",
        ),

        "success": _get_color(
            "SUCCESS",
            "#16A34A",
        ),

        "negative": _get_color(
            "DANGER",
            "#DC2626",
        ),

        "danger": _get_color(
            "DANGER",
            "#DC2626",
        ),

        "warning": _get_color(
            "WARNING",
            "#D97706",
        ),

        "neutral": _get_color(
            "TEXT_MUTED",
            "#64748B",
        ),
    }

    delta_color = delta_colors.get(
        str(delta_type).lower(),
        delta_colors["neutral"],
    )

    delta_html = ""

    if delta:

        delta_html = f"""
        <div style="
            display:inline-flex;
            align-items:center;
            margin-top:0.45rem;
            color:{delta_color};
            font-size:0.72rem;
            font-weight:700;
        ">
            {_safe(delta)}
        </div>
        """

    html = f"""
    <div style="
        padding:0.25rem 0;
    ">

        <div style="
            color:#64748B;
            font-size:0.72rem;
            font-weight:650;
            margin-bottom:0.3rem;
        ">
            {_safe(label)}
        </div>

        <div style="
            color:#0F172A;
            font-size:1.6rem;
            font-weight:750;
            line-height:1.1;
        ">
            {_safe(value)}
        </div>

        {delta_html}

    </div>
    """

    _render_html(html)


# ============================================================
# METRIC ITEM
# ============================================================

def metric_item(
    label: str,
    value: str | int | float,
    description: str | None = None,
    accent: str = "primary",
) -> None:
    """
    Render a simple metric item.
    """

    accent_color = _normalize_accent(
        accent
    )

    description_html = ""

    if description:

        description_html = f"""
        <div style="
            color:#64748B;
            font-size:0.7rem;
            margin-top:0.15rem;
        ">
            {_safe(description)}
        </div>
        """

    html = f"""
    <div style="
        position:relative;
        padding-left:0.85rem;
        margin-bottom:0.8rem;
    ">

        <div style="
            position:absolute;
            left:0;
            top:0.15rem;
            width:3px;
            height:calc(100% - 0.3rem);
            background:{accent_color};
            border-radius:999px;
        "></div>

        <div style="
            color:#64748B;
            font-size:0.72rem;
            font-weight:650;
        ">
            {_safe(label)}
        </div>

        <div style="
            color:#0F172A;
            font-size:1.05rem;
            font-weight:700;
            margin-top:0.2rem;
        ">
            {_safe(value)}
        </div>

        {description_html}

    </div>
    """

    _render_html(html)


# ============================================================
# EMPTY METRIC
# ============================================================

def empty_metric(
    label: str,
    description: str | None = None,
    accent: str = "neutral",
) -> None:
    """
    Render an empty metric.
    """

    metric_card(
        label=label,
        value="—",
        description=description,
        accent=accent,
    )


# ============================================================
# METRIC GRID
# ============================================================

def metric_grid(
    metrics: list[dict[str, Any]],
    columns: int = 4,
) -> None:
    """
    Render multiple metric cards in a Streamlit grid.
    """

    if not metrics:
        return

    try:
        columns = int(columns)

    except (
        TypeError,
        ValueError,
    ):
        columns = 4

    columns = max(
        1,
        min(columns, 6),
    )

    streamlit_columns = st.columns(
        columns
    )

    for index, metric in enumerate(
        metrics
    ):

        if not isinstance(
            metric,
            dict,
        ):
            continue

        column = streamlit_columns[
            index % columns
        ]

        with column:

            metric_card(
                label=metric.get(
                    "label",
                    "",
                ),
                value=metric.get(
                    "value",
                    "—",
                ),
                description=metric.get(
                    "description"
                ),
                status=metric.get(
                    "status"
                ),
                accent=metric.get(
                    "accent",
                    "primary",
                ),
            )


# ============================================================
# TWO COLUMN METRIC ROW
# ============================================================

def metric_pair(
    left: dict[str, Any],
    right: dict[str, Any],
) -> None:
    """
    Render two metrics side by side.
    """

    col1, col2 = st.columns(
        2
    )

    with col1:

        metric_card(
            label=left.get(
                "label",
                "",
            ),
            value=left.get(
                "value",
                "—",
            ),
            description=left.get(
                "description"
            ),
            status=left.get(
                "status"
            ),
            accent=left.get(
                "accent",
                "primary",
            ),
        )

    with col2:

        metric_card(
            label=right.get(
                "label",
                "",
            ),
            value=right.get(
                "value",
                "—",
            ),
            description=right.get(
                "description"
            ),
            status=right.get(
                "status"
            ),
            accent=right.get(
                "accent",
                "primary",
            ),
        )


# ============================================================
# THREE COLUMN METRIC ROW
# ============================================================

def metric_triplet(
    first: dict[str, Any],
    second: dict[str, Any],
    third: dict[str, Any],
) -> None:
    """
    Render three metrics side by side.
    """

    col1, col2, col3 = st.columns(
        3
    )

    metrics = [
        first,
        second,
        third,
    ]

    for column, metric in zip(
        (
            col1,
            col2,
            col3,
        ),
        metrics,
    ):

        with column:

            metric_card(
                label=metric.get(
                    "label",
                    "",
                ),
                value=metric.get(
                    "value",
                    "—",
                ),
                description=metric.get(
                    "description"
                ),
                status=metric.get(
                    "status"
                ),
                accent=metric.get(
                    "accent",
                    "primary",
                ),
            )


# ============================================================
# FOUR COLUMN METRIC ROW
# ============================================================

def metric_quad(
    first: dict[str, Any],
    second: dict[str, Any],
    third: dict[str, Any],
    fourth: dict[str, Any],
) -> None:
    """
    Render four metrics side by side.
    """

    col1, col2, col3, col4 = st.columns(
        4
    )

    metrics = [
        first,
        second,
        third,
        fourth,
    ]

    for column, metric in zip(
        (
            col1,
            col2,
            col3,
            col4,
        ),
        metrics,
    ):

        with column:

            metric_card(
                label=metric.get(
                    "label",
                    "",
                ),
                value=metric.get(
                    "value",
                    "—",
                ),
                description=metric.get(
                    "description"
                ),
                status=metric.get(
                    "status"
                ),
                accent=metric.get(
                    "accent",
                    "primary",
                ),
            )


# ============================================================
# PUBLIC API
# ============================================================

__all__ = [
    "metric_card",
    "comparison_card",
    "compact_metric",
    "status_badge",
    "kpi_value",
    "metric_item",
    "empty_metric",
    "metric_grid",
    "metric_pair",
    "metric_triplet",
    "metric_quad",
]