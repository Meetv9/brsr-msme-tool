"""
Home.py — Main Landing Page for BRSR MSME Tool

Run this file with: streamlit run Home.py

Streamlit auto-detects the /pages folder and builds the sidebar menu.
"""

import streamlit as st
from PIL import Image
from pathlib import Path
_BASE_DIR = Path(__file__).parent
_ecosetu_icon = Image.open(_BASE_DIR / "assets" / "ecosetu_favicon.png")
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
    page_title="Ecosetu — BRSR for Indian MSMEs",
    page_icon="assets/ecosetu_favicon.png",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "mailto:meet.vaghani9909@gmail.com",
        "Report a bug": "mailto:meet.vaghani9909@gmail.com?subject=Ecosetu%20Bug%20Report",
        "About": "Ecosetu — BRSR compliance for Indian MSMEs. Built by Meet Vaghani. Visit ecosetu.co.in"
    }
)
# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR LOGO (shows on every page automatically)
# ─────────────────────────────────────────────────────────────────────────────
try:
    st.logo(
        str(_BASE_DIR / "assets" / "ecosetu_logo.png"),
        icon_image=str(_BASE_DIR / "assets" / "ecosetu_icon_128.png"),
        size="large"
    )
except (AttributeError, TypeError):
    # Fallback for older Streamlit versions
    with st.sidebar:
        st.image(str(_BASE_DIR / "assets" / "ecosetu_logo.png"),
                 use_container_width=True)
        st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 4rem; max-width: 1000px; margin-left: auto; margin-right: auto; }
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
# HERO — Ecosetu Branding
# ─────────────────────────────────────────────────────────────────────────────
col_logo, col_text = st.columns([1, 2.5])

with col_logo:
    st.image(
        str(_BASE_DIR / "assets" / "ecosetu_logo_large.png"),
        use_container_width=True
    )

with col_text:
    st.markdown("""
<div style="padding-top:10px;">
    <div style="font-size:11px; font-weight:600; color:#6366F1;
                letter-spacing:2px; margin-bottom:6px;">
        BRSR COMPLIANCE PLATFORM
    </div>
    <div style="font-size:26px; font-weight:700; color:#0F172A;
                line-height:1.2; margin-bottom:8px;">
        Making Indian businesses<br>go green.
    </div>
    <div style="font-size:14px; color:#64748B; line-height:1.5;">
        Bank-ready BRSR sustainability reports in 60 minutes —
        purpose-built for Indian MSMEs.
    </div>
</div>
""", unsafe_allow_html=True)

# Trust badges row
st.markdown("")
trust_col1, trust_col2, trust_col3, trust_col4 = st.columns(4)
with trust_col1:
    st.markdown(
        '<div style="text-align:center; padding:12px 4px; background:#F8FAFC; '
        'border-radius:8px; border:1px solid #E2E8F0;">'
        '<div style="font-size:18px;">🆓</div>'
        '<div style="font-size:11px; color:#64748B; margin-top:2px;">Free to use</div>'
        '</div>',
        unsafe_allow_html=True
    )
with trust_col2:
    st.markdown(
        '<div style="text-align:center; padding:12px 4px; background:#F8FAFC; '
        'border-radius:8px; border:1px solid #E2E8F0;">'
        '<div style="font-size:18px;">🔒</div>'
        '<div style="font-size:11px; color:#64748B; margin-top:2px;">Privacy-first</div>'
        '</div>',
        unsafe_allow_html=True
    )
with trust_col3:
    st.markdown(
        '<div style="text-align:center; padding:12px 4px; background:#F8FAFC; '
        'border-radius:8px; border:1px solid #E2E8F0;">'
        '<div style="font-size:18px;">⚡</div>'
        '<div style="font-size:11px; color:#64748B; margin-top:2px;">60-min report</div>'
        '</div>',
        unsafe_allow_html=True
    )
with trust_col4:
    st.markdown(
        '<div style="text-align:center; padding:12px 4px; background:#F8FAFC; '
        'border-radius:8px; border:1px solid #E2E8F0;">'
        '<div style="font-size:18px;">🇮🇳</div>'
        '<div style="font-size:11px; color:#64748B; margin-top:2px;">Built for India</div>'
        '</div>',
        unsafe_allow_html=True
    )

# ─────────────────────────────────────────────────────────────────────────
# FOUNDING 100 CTA
# ─────────────────────────────────────────────────────────────────────────
st.markdown("")  # spacer
cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
with cta_col2:
    st.link_button(
        "🌱  Become a Founding Member — Free for Life",
        "https://forms.gle/ZAvGwN25sCPT3gU3A",
        use_container_width=True,
        type="primary",
    )
    st.markdown(
        "<p style='text-align:center; color:#555; font-size:14px; margin-top:8px;'>"
        "First 100 companies only. No payment, no trial expiry, no catch."
        "</p>",
        unsafe_allow_html=True,
    )
st.markdown("")  # spacer    
# ─────────────────────────────────────────────────────────────────────────────
# WHY BRSR? — Educational content for new visitors
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📖 What is BRSR & Why It Matters")

with st.expander("**What is BRSR?**  (1 min read)", expanded=False):
    st.markdown("""
**BRSR** stands for **Business Responsibility & Sustainability Reporting**.

It's a SEBI-mandated disclosure framework that asks Indian companies:

> *"How do you treat your employees, customers, environment,
> and community — beyond just making profits?"*

The framework has **9 NGRBC principles** covering ethics, sustainability,
employee welfare, stakeholder engagement, human rights, environment,
policy advocacy, inclusive growth, and customer responsibility.

**Currently mandatory for:** Top 1,000 listed companies (by market cap)
**Voluntary for:** All other companies — but increasingly demanded by
buyers, banks, and government schemes.
""")

with st.expander("**Why should an MSME care about BRSR?**", expanded=False):
    st.markdown("""
You're not legally required to file BRSR (unless you're a top-1000 listed
company). But here's why MSMEs are doing it voluntarily:

| Reason | What it unlocks |
|--------|-----------------|
| 🏦 **Bank loans** | Lower interest rates from SBI, HDFC, ICICI on ESG-disclosed loans |
| 🌍 **Export contracts** | EU buyers demand sustainability disclosure (CSRD coming 2027) |
| 🏭 **Big buyer contracts** | Tata, Reliance, ITC, Marico now ask suppliers for ESG data |
| 🪙 **Government schemes** | PLI, RAMP, Aatmanirbhar Bharat schemes prioritize compliant MSMEs |
| 💰 **Green funding** | SIDBI, NABARD offer concessional rates to ESG-disclosed MSMEs |
| 📈 **Investor readiness** | If you ever raise funds, this is the first thing they'll ask |

**One clean BRSR report = leverage in 6 different conversations.**
""")

with st.expander("**How does this tool help me?**", expanded=False):
    st.markdown("""
This tool is built **specifically for Indian MSMEs**, not big corporates.
Here's what makes it different:

- ⚡ **Quick Mode** — Answer just 10–15 questions per principle in plain language
- 🌐 **Indian context** — Examples in Gujarat/Saurashtra/Indian regulatory terms
- 💼 **Tier-aware** — If you're a sole proprietor, we hide board/KMP questions
- 🧮 **Auto-calculations** — We compute scores, GHG emissions, water intensity for you
- 📄 **BRSR-format PDF** — Audit-ready report you can send to banks/buyers
- 🆓 **Free to use** — No signup, no payment, no data collection
- 🔒 **Privacy-first** — Your data stays in your browser session, never sent to a server

Built for MSMEs by an MSME-focused developer.
""")

with st.expander("**How long does this take?**", expanded=False):
    st.markdown("""
**Quick Mode:** ~45–60 minutes for the entire BRSR report (all 9 principles).

**Full Mode:** ~3–4 hours if you want to fill every SEBI essential indicator.

You can save and resume anytime — your progress is auto-saved in your
browser session.

**Tip:** Have these ready before you start:
- Last year's turnover figure
- Number of employees and workers
- Electricity bills (annual kWh consumption)
- PCB Consent to Operate certificate
- A rough idea of your sourcing patterns
""")

st.markdown("")

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
# PRIMARY CTA — Start Section A
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("")
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    if st.button(
        "🚀  Start with Section A — General Disclosures",
        type="primary",
        use_container_width=True,
        key="cta_start_section_a"
    ):
        st.switch_page("pages/1_Section_A.py")
    st.caption(
        "Takes about 10–15 minutes. Your progress is auto-saved.",
        unsafe_allow_html=False
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
# FOOTER — Ecosetu branding + Your details
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
st.markdown("---")

# Top row: Brand statement
st.markdown("""
<div style="text-align:center; padding:16px 0 8px 0;">
    <div style="font-size:14px; font-weight:600; color:#0F4C2C;
                letter-spacing:0.3px; margin-bottom:4px;">
        ECOSETU
    </div>
    <div style="font-size:12px; color:#64748B; font-style:italic;">
        Green compliance, bridged.
    </div>
</div>
""", unsafe_allow_html=True)

# Three-column info grid
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("""
<div style="padding:12px;">
    <div style="font-size:10px; font-weight:600; color:#94A3B8;
                letter-spacing:1.5px; margin-bottom:8px;">
        BUILT BY
    </div>
    <div style="font-size:13px; font-weight:600; color:#0F172A;
                margin-bottom:4px;">
        Meet Ketankumar Vaghani
    </div>
    <div style="font-size:11px; color:#64748B; line-height:1.5;">
        Certified ESG Professional<br/>
        Bhavnagar, Gujarat
    </div>
</div>
""", unsafe_allow_html=True)

with col_b:
    st.markdown("""
<div style="padding:12px;">
    <div style="font-size:10px; font-weight:600; color:#94A3B8;
                letter-spacing:1.5px; margin-bottom:8px;">
        AN INITIATIVE BY
    </div>
    <div style="font-size:13px; font-weight:600; color:#0F172A;
                margin-bottom:4px;">
        Keprin Overseas Corporation
    </div>
    <div style="font-size:11px; color:#64748B; line-height:1.5;">
        Bhavnagar, India
    </div>
</div>
""", unsafe_allow_html=True)

with col_c:
    st.markdown("""
<div style="padding:12px;">
    <div style="font-size:10px; font-weight:600; color:#94A3B8;
                letter-spacing:1.5px; margin-bottom:8px;">
        CONNECT
    </div>
    <a href="https://www.linkedin.com/in/meetvaghani/" target="_blank"
       style="font-size:13px; font-weight:500; color:#0F4C2C;
              text-decoration:none; display:block; margin-bottom:4px;">
        LinkedIn →
    </a>
    <a href="mailto:meet.vaghani9909@gmail.com"
       style="font-size:11px; color:#64748B; text-decoration:none;">
        meet.vaghani9909@gmail.com
    </a>
</div>
""", unsafe_allow_html=True)

# Bottom disclaimer
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:12px 0 24px 0;">
    <div style="font-size:11px; color:#94A3B8; line-height:1.6;
                max-width:560px; margin:0 auto;">
        Built on the SEBI BRSR framework. Ecosetu is a self-service tool for
        MSME ESG disclosure preparation and is not a substitute for qualified
        legal, financial, or ESG advisory services. For final BRSR submission
        to SEBI, listed entities should consult an authorised auditor.
    </div>
    <div style="font-size:10px; color:#CBD5E1; margin-top:12px;">
        © 2026 Ecosetu · An initiative by Keprin Overseas Corporation
    </div>
</div>
""", unsafe_allow_html=True)