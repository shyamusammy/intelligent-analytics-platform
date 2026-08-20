"""
Reusable pipeline visualization for the Streamlit application.
"""

import html

import streamlit as st


# ============================================================
# PIPELINE CONFIGURATION
# ============================================================

PIPELINE_STEPS = [
    {
        "key": "upload",
        "label": "Upload",
        "description": "Add your dataset",
        "icon": "&#8593;",
    },
    {
        "key": "etl",
        "label": "Clean",
        "description": "Prepare the data",
        "icon": "&#10003;",
    },
    {
        "key": "profile",
        "label": "Profile",
        "description": "Understand the data",
        "icon": "&#9675;",
    },
    {
        "key": "analytics",
        "label": "Analytics",
        "description": "Find patterns",
        "icon": "&#9670;",
    },
    {
        "key": "ml",
        "label": "ML",
        "description": "Build models",
        "icon": "&#9671;",
    },
    {
        "key": "intelligence",
        "label": "Insights",
        "description": "Make decisions",
        "icon": "&#10022;",
    },
]


# ============================================================
# PIPELINE
# ============================================================

def render_pipeline(
    current_step: str,
    completed_steps: list[str],
) -> None:
    """
    Render the platform analysis pipeline.
    """

    completed = set(completed_steps)

    cards = []

    for index, step in enumerate(PIPELINE_STEPS):

        is_completed = step["key"] in completed
        is_current = step["key"] == current_step

        if is_completed:
            background = "#EFF6FF"
            border = "#BFDBFE"
            icon_background = "#2563EB"
            icon_color = "#FFFFFF"
            label_color = "#1E3A8A"
            status = "Complete"
            status_color = "#2563EB"
            status_background = "#DBEAFE"

        elif is_current:
            background = "#F8FAFC"
            border = "#CBD5E1"
            icon_background = "#0F172A"
            icon_color = "#FFFFFF"
            label_color = "#0F172A"
            status = "Current"
            status_color = "#0F172A"
            status_background = "#E2E8F0"

        else:
            background = "#FFFFFF"
            border = "#E2E8F0"
            icon_background = "#F1F5F9"
            icon_color = "#64748B"
            label_color = "#475569"
            status = "Pending"
            status_color = "#64748B"
            status_background = "#F1F5F9"

        card = f"""
<div style="flex:1; min-width:130px;">
<div style="background:{background}; border:1px solid {border}; border-radius:12px; padding:14px 10px 12px; min-height:132px; box-sizing:border-box; text-align:center;">
<div style="width:34px; height:34px; margin:0 auto 9px; border-radius:50%; background:{icon_background}; color:{icon_color}; display:flex; align-items:center; justify-content:center; font-size:15px; font-weight:700;">
{step["icon"]}
</div>
<div style="color:{label_color}; font-size:14px; font-weight:700; line-height:1.2;">
{html.escape(step["label"])}
</div>
<div style="margin-top:5px; color:#64748B; font-size:11px; line-height:1.35;">
{html.escape(step["description"])}
</div>
<div style="margin-top:9px; color:{status_color}; background:{status_background}; display:inline-block; padding:3px 8px; border-radius:999px; font-size:10px; font-weight:700;">
{status}
</div>
</div>
</div>
"""

        cards.append(card)

        if index < len(PIPELINE_STEPS) - 1:

            connector_color = (
                "#BFDBFE"
                if (
                    step["key"] in completed
                    and PIPELINE_STEPS[index + 1]["key"] in completed
                )
                else "#E2E8F0"
            )

            cards.append(
                f"""
<div style="flex:0 0 22px; height:1px; background:{connector_color}; margin:66px 3px 0;">
</div>
"""
            )

    pipeline_html = f"""
<div style="width:100%; overflow-x:auto; padding:4px 0 8px;">
<div style="display:flex; align-items:flex-start; width:100%; min-width:820px;">
{"".join(cards)}
</div>
</div>
"""

    st.markdown(
        pipeline_html,
        unsafe_allow_html=True,
    )