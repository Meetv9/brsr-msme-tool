"""
Home.py — Main Landing Page for BRSR MSME Tool

Run this file with: streamlit run Home.py

Streamlit auto-detects the /pages folder and builds the sidebar menu.
"""

import streamlit as st
from business_profile import (
    show_business_type_selector,
    show_tier_badge,
    get_business_type,
    is_sole_prop,
    is_listed,
)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BRSR Tool for MSMEs",
    page_icon="🌱",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; max-width: 860px; }
    .hero-box {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border: 2px solid #66bb6a; border-radius: 16px;
        padding: 24px; margin: 16px 0; text-align: center;
    }
    .progress-card {
        border: 1px solid #e0e0e0; border-radius: 12px;
        padding: 16px; margin: 8px 0;
    }
    .score-big {
        font-size: 56px; font-weight: 700;
        color: #1b5e20; margin: 8px 0;
    }
    .section-link {
        background: #f5f5f5; border-left: 4px solid #43a047;
        padding: 12px 16px; margin: 8px 0; border-radius: 0 8px 8px 0;
        font-size: 14px;
    }
    .done-tick {
        color: #2e7d32; font-weight: 700; font-size: 16px;
    }
    .pending-tick {
        color: #bdbdbd; font-size: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div style="font-size:48px">🌱</div>
    <div style="font-size:28px;font-weight:700;color:#1b5e20;">
        BRSR Tool for Indian MSMEs
    </div>
    <div style="font-size:15px;color:#2e7d32;margin-top:8px;">
        Business Responsibility & Sustainability Reporting — simplified for small businesses.
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: BUSINESS TYPE SELECTOR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
show_business_type_selector()

btype = get_business_type()
show_tier_badge()

if is_sole_prop():
    st.info(
        "✅ We'll hide board-related, shareholder, and formal policy "
        "questions since they don't apply to sole proprietorships."
    )
elif is_listed():
    st.warning(
        "⚠️ Listed companies must complete the full BRSR. "
        "All Essential + Leadership indicators will be shown."
    )

# ─────────────────────────────────────────────────────────────────────────────
# PROGRESS TRACKER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📊 Your BRSR Progress")

# Check what has been filled
sections = [
    ("Section A — General Disclosures", "data", "company_name",
     "1_📋_Section_A"),
    ("Section B — Management & Process", "data_b", None,
     "2_🧭_Section_B"),
    ("Principle 1 — Ethics & Integrity", "p1", None,
     "3_⚖️_Principle_1"),
    ("Principle 2 — Sustainable Products", "p2", None,
     "4_🔄_Principle_2"),
    ("Principle 3 — Employee Wellbeing", "p3", None,
     "5_👥_Principle_3"),
    ("Principles 4 & 5 — Stakeholders & Human Rights", "p4_5", None,
     "6_🤝_Principle_4_5"),
    ("Principle 6 — Environment", "p6", None,
     "7_🌿_Principle_6"),
    ("Principles 7, 8, 9 — Policy, Community & Customers", "p789", None,
     "8_🤝_Principle_7_8_9"),
]

completed = 0
total_sections = len(sections)

for name, key, subkey, page_name in sections:
    data = st.session_state.get(key, {})
    if subkey:
        is_done = bool(data.get(subkey))
    else:
        is_done = bool(data) and len(data) > 1

    mark = '<span class="done-tick">✅</span>' if is_done else '<span class="pending-tick">⭕</span>'
    if is_done:
        completed += 1

    st.markdown(
        f'<div class="section-link">{mark} &nbsp; {name}</div>',
        unsafe_allow_html=True
    )

st.markdown("")
progress_pct = completed / total_sections
st.progress(progress_pct)
st.caption(f"Completed: {completed} of {total_sections} sections")

# ─────────────────────────────────────────────────────────────────────────────
# OVERALL SCORE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🏆 Overall BRSR Readiness Score")


def collect_scores():
    """Gather sub-scores from each principle's session state."""
    scores = {}

    # Section A — ESG score (already calculated)
    data = st.session_state.get("data", {})
    if data.get("company_name"):
        # Rough ESG score based on completeness
        a_score = 0
        if data.get("company_name"): a_score += 10
        if data.get("email"): a_score += 5
        if data.get("activities"): a_score += 10
        if data.get("total_perm_emp", 0) > 0: a_score += 15
        if data.get("has_grievance"): a_score += 15
        if data.get("issues"): a_score += 15
        if data.get("board_female", 0) > 0: a_score += 10
        if data.get("export_pct", 0) > 0: a_score += 10
        if data.get("products"): a_score += 10
        scores["Section A"] = min(a_score, 100)

    # Each principle stores its own score
    for key, label in [
        ("p1", "P1"), ("p2", "P2"), ("p3", "P3"),
        ("p4_5", "P4+5"), ("p6", "P6"), ("p789", "P7+8+9")
    ]:
        pdata = st.session_state.get(key, {})
        if pdata.get("score") is not None and pdata.get("score") != 0:
            scores[label] = pdata["score"]

    return scores


scores = collect_scores()

if scores:
    avg_score = round(sum(scores.values()) / len(scores))
    colour = "#2e7d32" if avg_score >= 70 else "#ef6c00" if avg_score >= 40 else "#c62828"
    st.markdown(
        f'<div class="progress-card" style="text-align:center;">'
        f'<div class="score-big" style="color:{colour};">{avg_score}/100</div>'
        f'<div style="color:#666;font-size:14px;">'
        f'Average across {len(scores)} completed section(s)</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Individual scores
    st.markdown("**Section-wise scores:**")
    cols = st.columns(min(len(scores), 4))
    for i, (label, val) in enumerate(scores.items()):
        with cols[i % len(cols)]:
            st.metric(label, f"{val}/100")
else:
    st.info(
        "📝 Start filling Section A using the sidebar to see your score."
    )

# ─────────────────────────────────────────────────────────────────────────────
# WHAT TO DO NEXT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🧭 What to do next")

if completed == 0:
    st.info(
        "👉 Start with **Section A** in the sidebar. It captures your "
        "basic company information and auto-fills later sections."
    )
elif completed < total_sections:
    next_section = next(
        (name for name, key, subkey, _ in sections
         if not (st.session_state.get(key, {}) and
                 (st.session_state.get(key, {}).get(subkey) if subkey
                  else len(st.session_state.get(key, {})) > 1))),
        None
    )
    if next_section:
        st.info(f"👉 Continue with **{next_section}** from the sidebar.")
else:
    st.success(
        "🎉 **All sections complete!** Head to **'9 Generate Report'** "
        "in the sidebar to download your BRSR-ready PDF."
    )

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Built for MSMEs based on SEBI BRSR format. "
    "Not a substitute for professional legal or ESG advice."
)
