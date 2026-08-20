"""
Reusable layout components for the Streamlit application.
"""

import streamlit as st


# ============================================================
# PAGE HEADER
# ============================================================

def render_page_header(title: str, subtitle: str) -> None:
    """Render the main application page header."""

    st.html(
        f"""
        <div style="
            padding: 0.25rem 0 1.5rem 0;
        ">
            <h1 style="
                margin: 0;
                color: #111827;
                font-size: 2.35rem;
                font-weight: 750;
                letter-spacing: -0.04em;
                line-height: 1.15;
            ">
                {title}
            </h1>

            <div style="
                margin-top: 0.55rem;
                color: #64748B;
                font-size: 1rem;
                line-height: 1.6;
                max-width: 760px;
            ">
                {subtitle}
            </div>
        </div>
        """
    )


# ============================================================
# SECTION HEADER
# ============================================================

def render_section_header(
    title: str,
    description: str | None = None,
) -> None:
    """Render a consistent section heading."""

    st.html(
        f"""
        <div style="
            margin: 1.5rem 0 0.75rem 0;
        ">
            <h2 style="
                margin: 0;
                color: #1E293B;
                font-size: 1.35rem;
                font-weight: 700;
                letter-spacing: -0.02em;
            ">
                {title}
            </h2>
        </div>
        """
    )

    if description:
        st.caption(description)


# ============================================================
# METRIC CARD
# ============================================================

def render_metric_card(
    label: str,
    value: str,
    description: str | None = None,
) -> None:
    """Render a dashboard metric card."""

    description_html = ""

    if description:
        description_html = f"""
            <div style="
                margin-top: 0.35rem;
                color: #64748B;
                font-size: 0.78rem;
            ">
                {description}
            </div>
        """

    st.html(
        f"""
        <div style="
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            min-height: 110px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        ">

            <div style="
                color: #64748B;
                font-size: 0.78rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            ">
                {label}
            </div>

            <div style="
                margin-top: 0.45rem;
                color: #0F172A;
                font-size: 1.65rem;
                font-weight: 750;
                line-height: 1.2;
            ">
                {value}
            </div>

            {description_html}

        </div>
        """
    )


# ============================================================
# INFO CARD
# ============================================================

def render_info_card(
    title: str,
    message: str,
) -> None:
    """Render a subtle informational card."""

    st.html(
        f"""
        <div style="
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin: 0.75rem 0;
        ">

            <div style="
                color: #1E293B;
                font-size: 0.9rem;
                font-weight: 700;
                margin-bottom: 0.25rem;
            ">
                {title}
            </div>

            <div style="
                color: #64748B;
                font-size: 0.85rem;
                line-height: 1.5;
            ">
                {message}
            </div>

        </div>
        """
    )


# ============================================================
# DIVIDER
# ============================================================

def render_divider() -> None:
    """Render a lightweight visual divider."""

    st.html(
        """
        <div style="
            height: 1px;
            background: #E2E8F0;
            margin: 1.25rem 0;
        "></div>
        """
    )