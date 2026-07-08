import streamlit as st
from sidebar_footer import render_sidebar_footer, render_pagehead
render_sidebar_footer()
# ─── TIER LOGIC (NEW) ──────────────────────────────────────────
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from business_profile import init_business_profile, show_tier_badge, show_sidebar_logo

init_business_profile()
show_sidebar_logo()
show_tier_badge()

# ─── END TIER LOGIC ────────────────────────────────────────────
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BRSR P3 | Employee Wellbeing",
    page_icon="👷",
    layout="centered"  # centered for phone-friendly experience
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; max-width: 800px; }

    .question-card {
        background: #ffffff;
        border: 1.5px solid #e0f2e9;
        border-radius: 16px;
        padding: 24px 28px;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(46,125,50,0.06);
    }
    .question-title {
        font-size: 20px;
        font-weight: 600;
        color: #1b5e20;
        margin-bottom: 4px;
    }
    .question-why {
        background: #e8f5e9;
        border-left: 4px solid #43a047;
        padding: 8px 12px;
        border-radius: 0 8px 8px 0;
        font-size: 13px;
        color: #2e7d32;
        margin: 10px 0 16px 0;
    }
    .example-text {
        background: #fff8e1;
        border-left: 4px solid #ffc107;
        padding: 8px 12px;
        border-radius: 0 8px 8px 0;
        font-size: 13px;
        color: #5d4037;
        margin: 8px 0;
    }
    .calc-result {
        background: #f0f4ff;
        border: 1px solid #c7d2fe;
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 16px;
        font-weight: 600;
        color: #3730a3;
        margin: 10px 0;
        text-align: center;
    }
    .good-result {
        background: #e8f5e9;
        border: 1px solid #a5d6a7;
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 14px;
        color: #1b5e20;
        margin: 8px 0;
    }
    .warn-result {
        background: #fff3e0;
        border: 1px solid #ffcc80;
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 14px;
        color: #e65100;
        margin: 8px 0;
    }
    .bad-result {
        background: #ffebee;
        border: 1px solid #ef9a9a;
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 14px;
        color: #c62828;
        margin: 8px 0;
    }
    .section-win {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border: 2px solid #66bb6a;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin: 16px 0;
    }
    .mode-card {
        border: 2px solid #e0e0e0;
        border-radius: 14px;
        padding: 20px;
        cursor: pointer;
        text-align: center;
        margin: 8px;
    }
    .mode-selected {
        border-color: #2e7d32;
        background: #e8f5e9;
    }
    .progress-label {
        font-size: 13px;
        color: #666;
        margin-bottom: 4px;
    }
    .stButton > button {
        border-radius: 10px;
        font-size: 15px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "p3_mode" not in st.session_state:
    st.session_state.p3_mode = None          # None = not chosen yet

if "p3_quick_step" not in st.session_state:
    st.session_state.p3_quick_step = 1

if "p3_full_step" not in st.session_state:
    st.session_state.p3_full_step = 1

if "p3" not in st.session_state:
    st.session_state.p3 = {}

p3 = st.session_state.p3

# ─────────────────────────────────────────────────────────────────────────────
# AUTO-PULL FROM SECTION A DATA
# ─────────────────────────────────────────────────────────────────────────────
sec_a = st.session_state.get("data", {})

def prefill(p3_key, sec_a_key, default=0):
    if p3_key not in p3 and sec_a.get(sec_a_key):
        p3[p3_key] = sec_a[sec_a_key]
    return p3.get(p3_key, default)

# Pre-fill from Section A if available
prefill("total_perm_emp",  "total_perm_emp",  0)
prefill("total_perm_wkr",  "total_perm_wkr",  0)
prefill("company_name",    "company_name",    "")

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def safe_pct(n, d):
    try:
        n, d = float(n or 0), float(d or 0)
        return round((n / d) * 100, 1) if d > 0 else 0.0
    except:
        return 0.0

def ltifr(lti, ph):
    try:
        lti, ph = float(lti or 0), float(ph or 0)
        if ph > 0:
            return round((lti * 1_000_000) / ph, 2)
        return None
    except:
        return None

def show_why(text):
    st.markdown(f'<div class="question-why">💰 {text}</div>',
                unsafe_allow_html=True)

def show_example(text):
    st.markdown(f'<div class="example-text">📌 Example: {text}</div>',
                unsafe_allow_html=True)

def show_calc(text):
    st.markdown(f'<div class="calc-result">🔢 {text}</div>',
                unsafe_allow_html=True)

def show_good(text):
    st.markdown(f'<div class="good-result">✅ {text}</div>',
                unsafe_allow_html=True)

def show_warn(text):
    st.markdown(f'<div class="warn-result">⚠️ {text}</div>',
                unsafe_allow_html=True)

def show_bad(text):
    st.markdown(f'<div class="bad-result">🚨 {text}</div>',
                unsafe_allow_html=True)

def next_q():
    st.session_state.p3_quick_step += 1

def prev_q():
    st.session_state.p3_quick_step -= 1

def next_full():
    st.session_state.p3_full_step += 1

def prev_full():
    st.session_state.p3_full_step -= 1

# ─────────────────────────────────────────────────────────────────────────────
# BANK READY SCORE
# ─────────────────────────────────────────────────────────────────────────────
def calc_bank_score():
    # Reads both Quick-Mode and Full-Mode session keys so the score is correct
    # regardless of which mode the user completed.
    score = 0
    total = p3.get("total_workforce", 1) or 1

    health = p3.get("health_covered", 0)
    if safe_pct(health, total) >= 80: score += 20
    elif safe_pct(health, total) >= 50: score += 10

    # PF: Quick stores a sentence in pf_deposited; Full stores pf_dep == "Y".
    pf_ok = ("yes" in str(p3.get("pf_deposited", "")).lower()) or (p3.get("pf_dep") == "Y")
    if pf_ok: score += 20

    injuries = p3.get("lti_total", 0)
    if injuries == 0: score += 20
    elif injuries <= 2: score += 10

    # Grievance: Quick stores 'grievance'; Full stores per-category griev_*.
    griev_ok = str(p3.get("grievance", "")).startswith("Yes") or any(
        p3.get(f"griev_{gk}") == "Yes"
        for gk in ["perm_wkr", "contract_wkr", "perm_emp", "contract_emp"]
    )
    if griev_ok: score += 20

    # Training: Quick stores training_count; Full stores per-category trained counts.
    full_trained = max(
        p3.get("tr_emp_hs_cur", 0) + p3.get("tr_wkr_hs_cur", 0),
        p3.get("tr_emp_sk_cur", 0) + p3.get("tr_wkr_sk_cur", 0),
    )
    trained = max(p3.get("training_count", 0), full_trained)
    training_pct = safe_pct(trained, total)
    if training_pct >= 80: score += 20
    elif training_pct >= 50: score += 10

    return min(score, 100)

# ─────────────────────────────────────────────────────────────────────────────
# ── MODE SELECTION SCREEN ────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.p3_mode is None:

    render_pagehead(
        "Step 5 of 9 · Principle 3",
        "Employee & Worker Wellbeing",
        "Show how you look after your people — health insurance, PF, safety "
        "training, and fair treatment of workers."
    )
    st.markdown("How would you like to fill this section?")
    st.markdown("")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="mode-card">
            <div style="font-size:40px">⚡</div>
            <div style="font-size:20px; font-weight:700; color:#2e7d32;">Quick Mode</div>
            <div style="font-size:14px; color:#555; margin-top:8px;">
                10 simple questions<br>
                Takes under 10 minutes<br>
                No calculations needed<br>
                Perfect for first-time users
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Quick Mode ⚡",
                     use_container_width=True, type="primary"):
            st.session_state.p3_mode = "quick"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="mode-card">
            <div style="font-size:40px">📋</div>
            <div style="font-size:20px; font-weight:700; color:#1565c0;">Full Mode</div>
            <div style="font-size:14px; color:#555; margin-top:8px;">
                All 15 Essential + 6 Leadership<br>
                Takes 30–45 minutes<br>
                Complete SEBI-ready report<br>
                For consultants or serious users
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Full Mode 📋",
                     use_container_width=True):
            st.session_state.p3_mode = "full"
            st.rerun()

    st.markdown("")
    st.info(
        "💡 Not sure? Start with Quick Mode. You can always switch to Full Mode "
        "later — your data will be saved."
    )
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# HEADER (shown in both modes)
# ─────────────────────────────────────────────────────────────────────────────
mode_label = "⚡ Quick Mode" if st.session_state.p3_mode == "quick" else "📋 Full Mode"
render_pagehead(
    f"Step 5 of 9 · Principle 3 · {mode_label}",
    "Employee & Worker Wellbeing",
    "Show how you look after your people — health insurance, PF, safety "
    "training, and fair treatment of workers."
)
_, col_h2 = st.columns([3, 1])
with col_h2:
    if st.button("Switch Mode"):
        st.session_state.p3_mode = None
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# ██████████████████████  QUICK MODE  ████████████████████████████████████████
# ═════════════════════════════════════════════════════════════════════════════
# Show tier badge in main content area (not lost above mode selection)
if st.session_state.get("p3_mode"):
    show_tier_badge()
if st.session_state.p3_mode == "quick":

    TOTAL_QUICK = 10
    step = st.session_state.p3_quick_step

    # Progress bar
    st.markdown(
        f'<div class="progress-label">Question {min(step, TOTAL_QUICK)} of {TOTAL_QUICK}</div>',
        unsafe_allow_html=True
    )
    st.progress(min(step, TOTAL_QUICK) / TOTAL_QUICK)
    st.markdown("")

    # ── Q1: TOTAL WORKFORCE ──────────────────────────────────────────────
    if step == 1:
        with st.container():
            st.markdown("### 👥 How many people work at your business?")
            show_why(
                "This is the foundation of your entire BRSR report. "
                "All other percentages are calculated from this number."
            )
            show_example(
                "A garment factory with 8 tailors, 2 supervisors, and 1 manager "
                "= 11 people total."
            )

            # Pre-fill from Section A if available
            default_total = (
                p3.get("total_workforce") or
                (sec_a.get("total_perm_emp", 0) +
                 sec_a.get("total_temp_emp", 0) +
                 sec_a.get("total_perm_wkr", 0) +
                 sec_a.get("total_temp_wkr", 0)) or 0
            )

            if default_total > 0:
                st.success(
                    f"✅ We found {default_total} people from your Section A data. "
                    "You can change this if it's wrong."
                )

            total = st.number_input(
                "Total people working (employees + workers, all types combined)",
                min_value=0,
                value=int(default_total),
                help="Count everyone — permanent, contract, full-time, part-time."
            )
            p3["total_workforce"] = total

            if total > 0:
                show_good(f"Got it — {total} people. We will use this for all calculations.")
            else:
                show_warn("Enter at least 1 to continue.")

        st.markdown("")
        _, c_next = st.columns([1, 1])
        with c_next:
            if st.button("Next →", type="primary",
                         use_container_width=True,
                         disabled=(total == 0)):
                next_q(); st.rerun()

    # ── Q2: HEALTH INSURANCE ─────────────────────────────────────────────
    elif step == 2:
        with st.container():
            st.markdown("### 🏥 How many of your people have health insurance?")
            show_why(
                "Health insurance is the most-checked benefit by banks and "
                "large buyers. ESI registration counts — it's free for you to register."
            )
            show_example(
                "If you have 11 people and all are registered under ESIC = 11 covered. "
                "If only 5 have a company health policy = 5 covered."
            )
            st.markdown(
                "**💡 ESIC automatically covers** workers earning below ₹21,000/month "
                "for health and accident insurance. Check your ESIC employer portal."
            )

            total = p3.get("total_workforce", 1)
            health = st.number_input(
                "Number of people with health insurance (ESIC or private policy)",
                min_value=0,
                max_value=total,
                value=p3.get("health_covered", 0)
            )
            p3["health_covered"] = health

            if total > 0:
                pct = safe_pct(health, total)
                show_calc(f"{health} out of {total} = {pct}% health coverage")

                if pct >= 100:
                    show_good(
                        "100% coverage — excellent! This is a top positive "
                        "indicator for bank loans."
                    )
                elif pct >= 80:
                    show_good(
                        f"{pct}% coverage — very good. Try to get the remaining "
                        f"{total - health} people covered under ESIC."
                    )
                elif pct >= 50:
                    show_warn(
                        f"{pct}% coverage. Registering with ESIC takes 1 day "
                        "and covers everyone below ₹21,000 salary."
                    )
                elif health > 0:
                    show_bad(
                        f"Only {pct}% covered. This will flag in bank and buyer audits. "
                        "ESIC registration is free and mandatory for most MSMEs."
                    )

        st.markdown("")
        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q3: PF ───────────────────────────────────────────────────────────
    elif step == 3:
        with st.container():
            st.markdown("### 💰 Do you deduct and deposit PF for your employees?")
            show_why(
                "PF compliance is checked by every bank before approving an "
                "MSME loan. Non-compliance can result in penalties and block "
                "government tenders."
            )
            show_example(
                "Every month you deduct 12% from employee salary and add another "
                "12% from your side — this goes to EPFO. If your CA does this, "
                "the answer is Yes."
            )

            st.markdown(
                "**💡 PF is mandatory** if you have 20 or more employees. "
                "If you have fewer than 20, it's voluntary but recommended."
            )

            pf = st.radio(
                "Provident Fund (PF) — deducted and deposited with EPFO?",
                ["Yes — we deduct and deposit every month",
                 "No — we don't do PF",
                 "Not Applicable — we have fewer than 20 employees"],
                index=["Yes — we deduct and deposit every month",
                       "No — we don't do PF",
                       "Not Applicable — we have fewer than 20 employees"].index(
                    p3.get("pf_deposited",
                           "Yes — we deduct and deposit every month")
                )
            )
            p3["pf_deposited"] = pf

            if "Yes" in pf:
                show_good(
                    "PF compliant — this is a major positive for bank loans "
                    "and vendor onboarding."
                )
            elif "No" in pf:
                show_bad(
                    "No PF — if you have 20+ employees this is a legal violation. "
                    "Contact your CA immediately."
                )
            else:
                show_warn(
                    "Not applicable for now. If your workforce grows to 20+, "
                    "PF registration becomes mandatory."
                )

        st.markdown("")
        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q4: PARENTAL LEAVE ───────────────────────────────────────────────
    elif step == 4:
        with st.container():
            st.markdown("### 👶 Did anyone take maternity or paternity leave this year?")
            show_why(
                "Return-to-work rate shows you're a fair employer. "
                "High return rates improve your ESG score and reduce "
                "recruitment costs."
            )
            show_example(
                "3 women took maternity leave. 2 came back to work after leave. "
                "Return rate = 2/3 = 67%. We calculate this for you."
            )

            took = st.number_input(
                "How many people took maternity or paternity leave this year?",
                min_value=0,
                value=p3.get("parental_took", 0),
                help="Count both maternity (women) and paternity (men) leave."
            )
            p3["parental_took"] = took

            if took > 0:
                returned = st.number_input(
                    "How many of them came back to work after their leave ended?",
                    min_value=0,
                    max_value=took,
                    value=p3.get("parental_returned", 0)
                )
                p3["parental_returned"] = returned

                still_here = st.number_input(
                    "Of those who came back, how many are STILL working today?",
                    min_value=0,
                    max_value=returned if returned > 0 else took,
                    value=p3.get("parental_retained", 0),
                    help="This gives us the retention rate — are they staying "
                         "with you long-term after coming back?"
                )
                p3["parental_retained"] = still_here

                # Auto-calculate
                return_rate = safe_pct(returned, took)
                retention_rate = safe_pct(still_here, returned) if returned > 0 else 0.0

                p3["parental_return_rate"] = return_rate
                p3["parental_retention_rate"] = retention_rate

                show_calc(
                    f"Return to work rate: {returned}/{took} = {return_rate}%  |  "
                    f"Retention rate: {still_here}/{returned if returned > 0 else took} "
                    f"= {retention_rate}%"
                )

                if return_rate >= 80:
                    show_good(
                        f"{return_rate}% return rate — excellent. "
                        "This shows you're a fair employer."
                    )
                elif return_rate >= 50:
                    show_warn(
                        f"{return_rate}% returned. Consider offering flexible "
                        "work options to improve this."
                    )
                elif took > 0:
                    show_bad(
                        f"Low return rate. Find out why people aren't coming "
                        "back — it may reveal a workplace culture issue."
                    )
            else:
                st.info("Nobody took parental leave this year — that's fine, "
                        "just answer 0.")
                p3["parental_returned"] = 0
                p3["parental_retained"] = 0
                p3["parental_return_rate"] = 0
                p3["parental_retention_rate"] = 0

        st.markdown("")
        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q5: TRAINING ─────────────────────────────────────────────────────
    elif step == 5:
        with st.container():
            st.markdown("### 📚 How many people received safety or skill training this year?")
            show_why(
                "Training coverage is checked by large buyers and banks. "
                "Even one safety induction session for new joiners counts. "
                "Documenting this costs nothing."
            )
            show_example(
                "You held a fire safety demo for all 11 workers in June = "
                "11 people trained. Or: 5 workers went for a NSDC skill course = 5."
            )

            total = p3.get("total_workforce", 1)

            safety_trained = st.number_input(
                "People who received Health & Safety training "
                "(fire safety, machine safety, first aid, PPE use, etc.)",
                min_value=0,
                max_value=total,
                value=p3.get("safety_trained", 0)
            )
            p3["safety_trained"] = safety_trained

            skill_trained = st.number_input(
                "People who received Skill Upgradation training "
                "(new machine operation, quality control, computer skills, etc.)",
                min_value=0,
                max_value=total,
                value=p3.get("skill_trained", 0)
            )
            p3["skill_trained"] = skill_trained
            p3["training_count"] = max(safety_trained, skill_trained)

            if total > 0:
                s_pct = safe_pct(safety_trained, total)
                sk_pct = safe_pct(skill_trained, total)
                show_calc(
                    f"Safety training: {safety_trained}/{total} = {s_pct}%  |  "
                    f"Skill training: {skill_trained}/{total} = {sk_pct}%"
                )

                if s_pct >= 80:
                    show_good(
                        f"{s_pct}% safety training coverage — strong. "
                        "This reduces your accident risk and insurance costs."
                    )
                elif s_pct > 0:
                    show_warn(
                        f"{s_pct}% safety training. Schedule one all-staff "
                        "safety session — it covers this completely."
                    )
                else:
                    show_bad(
                        "No safety training recorded. Even a 30-minute fire "
                        "safety demo counts. Document it."
                    )

        st.markdown("")
        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q6: SAFETY INCIDENTS ─────────────────────────────────────────────
    elif step == 6:
        with st.container():
            st.markdown("### 🚑 Did anyone get injured at work this year?")
            show_why(
                "Safety incident records are the first thing factory auditors "
                "check. Zero injuries = strong ESG profile. "
                "Even if injuries happened, documenting them honestly is better "
                "than hiding them."
            )
            show_example(
                "A worker cut their finger and had to take 2 days off = 1 injury. "
                "Someone slipped but came back same day = does not count as LTI. "
                "LTI = Lost Time Injury = missed work the next day."
            )

            injuries = st.number_input(
                "Number of workplace injuries where the person missed work "
                "the NEXT day (called Lost Time Injuries or LTI)",
                min_value=0,
                value=p3.get("lti_total", 0),
                help="If someone was hurt but came back to work the same day "
                     "or next day, that does NOT count here."
            )
            p3["lti_total"] = injuries

            fatalities = st.number_input(
                "Any deaths at workplace this year? (we hope the answer is 0)",
                min_value=0,
                value=p3.get("fatalities_total", 0)
            )
            p3["fatalities_total"] = fatalities

            if fatalities > 0:
                show_bad(
                    f"{fatalities} fatality/fatalities reported. "
                    "Ensure all legal procedures, insurance claims, and "
                    "corrective actions are documented. Add details in Full Mode."
                )
            elif injuries == 0:
                show_good(
                    "Zero injuries — excellent safety record. "
                    "This is a top positive indicator."
                )
            elif injuries <= 2:
                show_warn(
                    f"{injuries} injury/injuries. Document corrective actions "
                    "to show you've fixed the issue."
                )
            else:
                show_bad(
                    f"{injuries} injuries is high. A safety review is needed. "
                    "Document what corrective steps you're taking."
                )

        st.markdown("")
        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q7: JUGAAD LTIFR CALCULATOR ──────────────────────────────────────
    elif step == 7:
        with st.container():
            st.markdown("### ⏱️ Let's calculate your safety rate (LTIFR)")
            show_why(
                "LTIFR (Lost Time Injury Frequency Rate) is a standard safety "
                "metric. Banks, insurers, and large buyers use it to compare "
                "your safety performance."
            )

            st.markdown(
                '<div style="background:#fff3e0; border:2px dashed #ff9800; '
                'border-radius:12px; padding:16px; margin:10px 0;">'
                '<b>🔧 We calculate this for you.</b> Just answer these simple '
                'questions about your working hours.</div>',
                unsafe_allow_html=True
            )

            total = p3.get("total_workforce", 1)

            c1, c2 = st.columns(2)
            with c1:
                days = st.number_input(
                    "How many days was your factory/office open this year?",
                    min_value=1, max_value=365,
                    value=p3.get("working_days", 300),
                    help="Typical answer: 300. Subtract Sundays + public holidays."
                )
                p3["working_days"] = days

                hours = st.number_input(
                    "How many hours per day do your workers work?",
                    min_value=1.0, max_value=24.0,
                    value=float(p3.get("hours_per_day", 8.0)),
                    step=0.5,
                    help="Single shift = 8 hours. Double shift = 16 hours."
                )
                p3["hours_per_day"] = hours

            with c2:
                shifts = st.number_input(
                    "How many shifts per day?",
                    min_value=1, max_value=3,
                    value=p3.get("shifts", 1),
                    help="Most small factories run 1 shift."
                )
                p3["shifts"] = shifts

                st.markdown("")
                st.markdown("**Your numbers:**")
                person_hours = total * days * hours * shifts
                p3["person_hours"] = person_hours
                st.markdown(
                    f"**{total}** people × **{days}** days × "
                    f"**{hours}** hrs × **{shifts}** shift(s)"
                )
                show_calc(f"= {int(person_hours):,} person-hours")

            lti = p3.get("lti_total", 0)
            ltifr_val = ltifr(lti, person_hours)
            p3["ltifr"] = ltifr_val

            if ltifr_val is not None:
                st.markdown("")
                st.info(
                    f"**LTIFR formula:** {lti} injuries × 1,000,000 ÷ "
                    f"{int(person_hours):,} person-hours = **{ltifr_val}**"
                )
                if ltifr_val == 0:
                    show_good(
                        "LTIFR = 0. Perfect safety record — this is outstanding."
                    )
                elif ltifr_val < 1:
                    show_good(
                        f"LTIFR = {ltifr_val}. Below 1 is considered safe. "
                        "Good performance."
                    )
                elif ltifr_val < 5:
                    show_warn(
                        f"LTIFR = {ltifr_val}. Above 1 is a flag for auditors. "
                        "Focus on safety training."
                    )
                else:
                    show_bad(
                        f"LTIFR = {ltifr_val}. This is high. Immediate safety "
                        "review is recommended."
                    )

        st.markdown("")
        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q8: GRIEVANCE ────────────────────────────────────────────────────
    elif step == 8:
        with st.container():
            st.markdown("### 📣 Can your workers raise complaints without fear?")
            show_why(
                "Having a complaint system prevents small issues from becoming "
                "big strikes or legal cases. Large buyers require this before "
                "vendor onboarding."
            )
            show_example(
                "A WhatsApp number dedicated to complaints, a physical complaint "
                "register at the factory entrance, monthly open-door meeting with "
                "the owner — any of these count."
            )

            grievance = st.radio(
                "Do your workers have a way to raise complaints?",
                ["Yes — we have a system",
                 "No — we don't have a formal system yet"],
                index=0 if p3.get("grievance", "No").startswith("Yes") else 1
            )
            p3["grievance"] = grievance

            if grievance.startswith("Yes"):
                p3["grievance_desc"] = st.text_input(
                    "Briefly describe how (one line is enough)",
                    value=p3.get("grievance_desc", ""),
                    placeholder="e.g. Dedicated WhatsApp number + monthly "
                                "meeting with owner"
                )
                show_good(
                    "Grievance mechanism in place — this improves your vendor "
                    "rating significantly."
                )
            else:
                show_warn(
                    "No system yet. Create a WhatsApp group or complaint register "
                    "today — it takes 10 minutes and makes a big difference."
                )

        st.markdown("")
        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q9: LIFE INSURANCE ───────────────────────────────────────────────
    elif step == 9:
        with st.container():
            st.markdown("### 💀 If a worker dies at your workplace, "
                        "does their family receive any money?")
            show_why(
                "This shows you care about your workers beyond the minimum. "
                "Large corporates score vendors on this. ESIC already provides "
                "death benefits — if you have ESIC, the answer is likely Yes."
            )
            show_example(
                "If you have ESIC, the family gets ₹15,000 + 90% of wages "
                "for life. If you have a company group term life insurance = Yes."
            )

            life_ins = st.radio(
                "Life insurance or compensation package for workers/employees "
                "in case of death?",
                ["Yes — ESIC death benefit / company life insurance",
                 "No — we don't have this"],
                index=0 if p3.get("life_insurance", "No").startswith("Yes") else 1
            )
            p3["life_insurance"] = life_ins

            if life_ins.startswith("Yes"):
                show_good(
                    "This is a leadership indicator — shows you go beyond minimum "
                    "compliance and care for your workers."
                )
            else:
                show_warn(
                    "Consider enrolling in ESIC which automatically provides "
                    "death benefits. Registration is free."
                )

        st.markdown("")
        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q10: SAFETY MEASURES ─────────────────────────────────────────────
    elif step == 10:
        with st.container():
            st.markdown("### 🦺 What safety measures do you have at your workplace?")
            show_why(
                "This is your chance to tell banks and buyers what you do to "
                "keep your workers safe. Even basic measures count."
            )
            show_example(
                "PPE (helmets, gloves, safety shoes) provided to all workers. "
                "Fire extinguisher installed and tested every year. "
                "First aid kit at every workstation. Monthly safety checklist."
            )

            measures = st.text_area(
                "List your safety measures — one per line (be honest, even basic things count)",
                value=p3.get("safety_measures", ""),
                height=120,
                placeholder="e.g.\n"
                            "• Safety shoes and gloves provided to all workers\n"
                            "• Fire extinguisher installed at factory entrance\n"
                            "• First aid kit available\n"
                            "• No smoking rule enforced"
            )
            p3["safety_measures"] = measures

            if measures and len(measures.strip()) > 20:
                show_good(
                    "Good — these measures are documented. This will appear "
                    "directly in your BRSR report."
                )
            else:
                show_warn(
                    "Add at least 2-3 measures. Think about what you already "
                    "do — PPE, fire safety, first aid."
                )

        st.markdown("")
        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Finish & See Results 🎉",
                         type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── QUICK MODE SUMMARY ────────────────────────────────────────────────
    elif step > 10:

        st.balloons()

        st.markdown(
            '<div class="section-win">'
            '<div style="font-size:48px">🎉</div>'
            '<div style="font-size:22px; font-weight:700; color:#1b5e20;">'
            'Quick Mode Complete!</div>'
            '<div style="font-size:14px; color:#2e7d32; margin-top:8px;">'
            'You have filled the essential employee wellbeing disclosures.'
            '</div></div>',
            unsafe_allow_html=True
        )

        bank_score = calc_bank_score()
        p3["score"] = bank_score
        total = p3.get("total_workforce", 0)

        # Score display
        colour = "green" if bank_score >= 70 else "orange" if bank_score >= 40 else "red"
        st.markdown(
            f"<h2 style='color:{colour}; text-align:center'>"
            f"{bank_score}/100</h2>"
            "<p style='text-align:center; color:gray'>Bank-Ready Score</p>",
            unsafe_allow_html=True
        )
        st.progress(bank_score / 100)

        # Summary metrics
        st.markdown("---")
        st.markdown("### Your P3 Summary")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Workforce", total)
        m2.metric("Health Coverage",
                  f"{safe_pct(p3.get('health_covered', 0), total)}%")
        m3.metric("Safety Incidents",
                  p3.get("lti_total", 0))
        m4.metric("LTIFR",
                  p3.get("ltifr", "—"))

        m5, m6, m7, m8 = st.columns(4)
        m5.metric("PF Status",
                  "✅" if "Yes" in p3.get("pf_deposited", "") else "❌")
        m6.metric("Grievance",
                  "✅" if p3.get("grievance", "").startswith("Yes") else "❌")
        m7.metric("Safety Training",
                  f"{safe_pct(p3.get('safety_trained', 0), total)}%")
        m8.metric("Return from Leave",
                  f"{p3.get('parental_return_rate', 0)}%")

        # Recommendations
        st.markdown("---")
        st.markdown("### What To Do Next")

        recs = 0
        health_pct = safe_pct(p3.get("health_covered", 0), total)
        if health_pct < 80 and total > 0:
            show_warn(
                f"Health coverage is {health_pct}%. "
                "Register with ESIC to bring this to 100%."
            )
            recs += 1

        if "No" in p3.get("pf_deposited", ""):
            show_bad(
                "PF not being deposited. Contact your CA today — "
                "this is a legal requirement for 20+ employees."
            )
            recs += 1

        if p3.get("grievance", "").startswith("No"):
            show_warn(
                "No grievance mechanism. Create a WhatsApp complaint number "
                "today — takes 5 minutes."
            )
            recs += 1

        safety_pct = safe_pct(p3.get("safety_trained", 0), total)
        if safety_pct < 50 and total > 0:
            show_warn(
                f"Only {safety_pct}% safety training. "
                "One all-staff safety briefing will fix this."
            )
            recs += 1

        if recs == 0:
            show_good(
                "No major gaps! Your basic P3 compliance looks solid."
            )

        # Options
        st.markdown("---")
        st.markdown("### What would you like to do?")

        op1, op2 = st.columns(2)
        with op1:
            if st.button("📋 Switch to Full Mode\n(for complete report)",
                         use_container_width=True):
                st.session_state.p3_mode = "full"
                st.rerun()
        with op2:
            if st.button("💾 Save & Move to P4 →",
                         use_container_width=True, type="primary"):
                st.session_state.c_p3 = p3
                st.success(
                    "✅ P3 Quick Mode saved! "
                    "Next: Principle 4 — Stakeholder Engagement."
                )

# ═════════════════════════════════════════════════════════════════════════════
# ██████████████████████  FULL MODE  █████████████████████████████████████████
# ═════════════════════════════════════════════════════════════════════════════
else:

    full_step = st.session_state.p3_full_step
    TOTAL_FULL = 7

    full_steps_labels = {
        1: "🎯 Benefits",
        2: "🏦 Retirement & Leave",
        3: "📣 Grievance & Union",
        4: "📚 Training",
        5: "🦺 Health & Safety",
        6: "🏆 Leadership",
        7: "✅ Summary"
    }

    # Nav
    nav = st.columns(7)
    for i, (num, label) in enumerate(full_steps_labels.items()):
        with nav[i]:
            t = "primary" if full_step == num else "secondary"
            if st.button(label, key=f"fn_{num}",
                         type=t, use_container_width=True):
                st.session_state.p3_full_step = num
                st.rerun()

    st.progress(full_step / TOTAL_FULL)
    st.markdown("---")

    # ── FULL STEP 1: BENEFITS ─────────────────────────────────────────────
    if full_step == 1:
        st.header("🎯 Step 1 — Workforce & Benefits")

        st.info(
            "We'll ask you for counts. All percentages are calculated automatically. "
            "**Employees** = office/admin staff. **Workers** = factory/shop floor staff."
        )

        # Workforce counts
        with st.container(border=True):
            st.markdown("#### Your Workforce")
            show_example(
                "Permanent employees = on your payroll, fixed monthly salary. "
                "Contract = hired through agency or seasonal. "
                "Workers = physically work on your factory floor."
            )

            c1, c2 = st.columns(2)
            with c1:
                p3["perm_emp_m"] = st.number_input(
                    "Permanent Employees — Male",
                    min_value=0, value=p3.get("perm_emp_m", 0), key="f_pe_m"
                )
                p3["perm_emp_f"] = st.number_input(
                    "Permanent Employees — Female",
                    min_value=0, value=p3.get("perm_emp_f", 0), key="f_pe_f"
                )
                p3["contract_emp_m"] = st.number_input(
                    "Contract Employees — Male",
                    min_value=0, value=p3.get("contract_emp_m", 0), key="f_ce_m"
                )
                p3["contract_emp_f"] = st.number_input(
                    "Contract Employees — Female",
                    min_value=0, value=p3.get("contract_emp_f", 0), key="f_ce_f"
                )
            with c2:
                p3["perm_wkr_m"] = st.number_input(
                    "Permanent Workers — Male",
                    min_value=0, value=p3.get("perm_wkr_m", 0), key="f_pw_m"
                )
                p3["perm_wkr_f"] = st.number_input(
                    "Permanent Workers — Female",
                    min_value=0, value=p3.get("perm_wkr_f", 0), key="f_pw_f"
                )
                p3["contract_wkr_m"] = st.number_input(
                    "Contract Workers — Male",
                    min_value=0, value=p3.get("contract_wkr_m", 0), key="f_cw_m"
                )
                p3["contract_wkr_f"] = st.number_input(
                    "Contract Workers — Female",
                    min_value=0, value=p3.get("contract_wkr_f", 0), key="f_cw_f"
                )

            total_perm_emp = p3["perm_emp_m"] + p3["perm_emp_f"]
            total_perm_wkr = p3["perm_wkr_m"] + p3["perm_wkr_f"]
            total_all = (total_perm_emp +
                         p3["contract_emp_m"] + p3["contract_emp_f"] +
                         total_perm_wkr +
                         p3["contract_wkr_m"] + p3["contract_wkr_f"])
            p3["total_workforce"] = total_all

            tm = st.columns(3)
            tm[0].metric("Permanent Employees", total_perm_emp)
            tm[1].metric("Permanent Workers", total_perm_wkr)
            tm[2].metric("Total Workforce", total_all)

        # Benefits
        with st.container(border=True):
            st.markdown("#### Benefits Coverage")
            st.markdown(
                "For each benefit, enter how many people in each category "
                "are covered. We calculate percentages automatically."
            )

            benefit_types = [
                ("health_ins", "🏥 Health Insurance",
                 "ESIC counts. Check ESIC employer portal."),
                ("accident_ins", "🦺 Accident Insurance",
                 "ESIC also covers this. Check your policy."),
                ("maternity", "🤱 Maternity Benefits",
                 "Count women who received paid maternity leave."),
                ("paternity", "👶 Paternity Benefits",
                 "Count men who received paid paternity leave."),
                ("daycare", "🏫 Day Care Facilities",
                 "Do you provide or subsidise childcare for staff?"),
            ]

            for bk, blabel, btip in benefit_types:
                with st.expander(blabel):
                    st.caption(f"💡 {btip}")
                    bc = st.columns(4)
                    p3[f"{bk}_pe"] = bc[0].number_input(
                        "Perm Emp",
                        min_value=0, max_value=max(total_perm_emp, 1),
                        value=p3.get(f"{bk}_pe", 0), key=f"f_{bk}_pe"
                    )
                    p3[f"{bk}_pw"] = bc[1].number_input(
                        "Perm Workers",
                        min_value=0, max_value=max(total_perm_wkr, 1),
                        value=p3.get(f"{bk}_pw", 0), key=f"f_{bk}_pw"
                    )
                    pe_pct = safe_pct(p3[f"{bk}_pe"], total_perm_emp)
                    pw_pct = safe_pct(p3[f"{bk}_pw"], total_perm_wkr)
                    bc[2].metric("Emp Coverage", f"{pe_pct}%")
                    bc[3].metric("Worker Coverage", f"{pw_pct}%")

                    if bk == "health_ins":
                        p3["health_covered"] = p3[f"{bk}_pe"] + p3[f"{bk}_pw"]

        _, c_next = st.columns([1, 1])
        with c_next:
            if st.button("Next: Retirement & Leave →",
                         type="primary", use_container_width=True):
                next_full(); st.rerun()

    # ── FULL STEP 2: RETIREMENT & PARENTAL LEAVE ──────────────────────────
    elif full_step == 2:
        st.header("🏦 Step 2 — Retirement Benefits & Parental Leave")

        with st.container(border=True):
            st.markdown("#### PF, Gratuity, ESI — Current & Previous Year")
            show_example(
                "Ask your CA for the monthly ECR challan to find PF coverage. "
                "For ESI, check your ESIC employer login portal."
            )

            for rkey, rlabel, rtip in [
                ("pf", "PF (Provident Fund)",
                 "Mandatory for 20+ employees. Check PF challan."),
                ("gratuity", "Gratuity",
                 "After 5 years of service. Check payroll."),
                ("esi", "ESI",
                 "For salary below ₹21,000. Check ESIC portal."),
            ]:
                st.markdown(f"**{rlabel}** — *{rtip}*")
                rc = st.columns(6)
                p3[f"{rkey}_emp_cur"] = rc[0].number_input(
                    "% Emp (Current)",
                    min_value=0.0, max_value=100.0,
                    value=float(p3.get(f"{rkey}_emp_cur", 0.0)),
                    key=f"f_{rkey}_ec"
                )
                p3[f"{rkey}_wkr_cur"] = rc[1].number_input(
                    "% Workers (Current)",
                    min_value=0.0, max_value=100.0,
                    value=float(p3.get(f"{rkey}_wkr_cur", 0.0)),
                    key=f"f_{rkey}_wc"
                )
                p3[f"{rkey}_dep"] = rc[2].selectbox(
                    "Deposited?",
                    ["Y", "N", "N.A."],
                    index=["Y", "N", "N.A."].index(
                        p3.get(f"{rkey}_dep", "Y")
                    ),
                    key=f"f_{rkey}_dep"
                )
                p3[f"{rkey}_emp_prev"] = rc[3].number_input(
                    "% Emp (Previous)",
                    min_value=0.0, max_value=100.0,
                    value=float(p3.get(f"{rkey}_emp_prev", 0.0)),
                    key=f"f_{rkey}_ep"
                )
                p3[f"{rkey}_wkr_prev"] = rc[4].number_input(
                    "% Workers (Previous)",
                    min_value=0.0, max_value=100.0,
                    value=float(p3.get(f"{rkey}_wkr_prev", 0.0)),
                    key=f"f_{rkey}_wp"
                )
                p3[f"{rkey}_dep_prev"] = rc[5].selectbox(
                    "Deposited (Prev)?",
                    ["Y", "N", "N.A."],
                    index=["Y", "N", "N.A."].index(
                        p3.get(f"{rkey}_dep_prev", "Y")
                    ),
                    key=f"f_{rkey}_dp"
                )
                if p3[f"{rkey}_dep"] == "N" and rkey in ["pf", "esi"]:
                    show_bad(
                        f"{rlabel} not deposited — legal violation. "
                        "Contact CA immediately."
                    )
                st.markdown("")

        with st.container(border=True):
            st.markdown("#### Parental Leave — Tell us counts, we calculate rates")
            show_example(
                "3 women took maternity leave. 2 came back. 1 is still "
                "working 12 months later. Return rate = 67%, Retention = 50%."
            )

            pl_cats = [
                ("perm_emp_m",  "Permanent Employees — Male"),
                ("perm_emp_f",  "Permanent Employees — Female"),
                ("perm_wkr_m",  "Permanent Workers — Male"),
                ("perm_wkr_f",  "Permanent Workers — Female"),
            ]

            for pk, plabel in pl_cats:
                with st.expander(plabel):
                    plc = st.columns(3)
                    took = plc[0].number_input(
                        "Took leave",
                        min_value=0, value=p3.get(f"pl_{pk}_took", 0),
                        key=f"f_pl_{pk}_t"
                    )
                    returned = plc[1].number_input(
                        "Came back",
                        min_value=0, max_value=max(took, 1),
                        value=p3.get(f"pl_{pk}_returned", 0),
                        key=f"f_pl_{pk}_r"
                    )
                    retained = plc[2].number_input(
                        "Still here now",
                        min_value=0,
                        max_value=max(returned, 1),
                        value=p3.get(f"pl_{pk}_retained", 0),
                        key=f"f_pl_{pk}_ret"
                    )

                    p3[f"pl_{pk}_took"] = took
                    p3[f"pl_{pk}_returned"] = returned
                    p3[f"pl_{pk}_retained"] = retained

                    if took > 0:
                        rr = safe_pct(returned, took)
                        ret = safe_pct(retained, returned) if returned > 0 else 0.0
                        show_calc(
                            f"Return rate: {returned}/{took} = {rr}%  |  "
                            f"Retention: {retained}/{returned if returned > 0 else took} = {ret}%"
                        )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_full(); st.rerun()
        with c_next:
            if st.button("Next: Grievance & Union →",
                         type="primary", use_container_width=True):
                next_full(); st.rerun()

    # ── FULL STEP 3: GRIEVANCE & UNION ────────────────────────────────────
    elif full_step == 3:
        st.header("📣 Step 3 — Grievance Mechanism & Union Membership")

        with st.container(border=True):
            st.markdown("#### Grievance Mechanism — per staff category")
            show_example(
                "A WhatsApp number for complaints, a physical register at "
                "the factory gate, or a monthly open-door session all count."
            )

            for gk, glabel in [
                ("perm_wkr",     "Permanent Workers"),
                ("contract_wkr", "Contract Workers"),
                ("perm_emp",     "Permanent Employees"),
                ("contract_emp", "Contract Employees"),
            ]:
                gc = st.columns([1, 2])
                with gc[0]:
                    p3[f"griev_{gk}"] = st.radio(
                        glabel,
                        ["Yes", "No"],
                        horizontal=True,
                        index=0 if p3.get(f"griev_{gk}", "No") == "Yes" else 1,
                        key=f"f_g_{gk}"
                    )
                with gc[1]:
                    if p3[f"griev_{gk}"] == "Yes":
                        p3[f"griev_{gk}_desc"] = st.text_input(
                            "How? (brief)",
                            value=p3.get(f"griev_{gk}_desc", ""),
                            placeholder="e.g. Monthly meeting with supervisor",
                            key=f"f_gd_{gk}"
                        )

        with st.container(border=True):
            st.markdown("#### Union Membership")
            st.caption(
                "Most MSMEs have no unions — answer 0. "
                "That is a completely valid answer."
            )

            for uk, ulabel in [
                ("perm_emp_m", "Permanent Employees — Male"),
                ("perm_emp_f", "Permanent Employees — Female"),
                ("perm_wkr_m", "Permanent Workers — Male"),
                ("perm_wkr_f", "Permanent Workers — Female"),
            ]:
                uc = st.columns(3)
                uc[0].markdown(f"**{ulabel}**")
                total_val = p3.get(uk, 0)
                p3[f"union_{uk}_cur"] = uc[1].number_input(
                    "In union (Current FY)",
                    min_value=0,
                    value=p3.get(f"union_{uk}_cur", 0),
                    key=f"f_u_{uk}_c"
                )
                union_pct = safe_pct(p3[f"union_{uk}_cur"], total_val)
                uc[2].metric("Union %", f"{union_pct}%")

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_full(); st.rerun()
        with c_next:
            if st.button("Next: Training →",
                         type="primary", use_container_width=True):
                next_full(); st.rerun()

    # ── FULL STEP 4: TRAINING & REVIEWS ───────────────────────────────────
    elif full_step == 4:
        st.header("📚 Step 4 — Training & Performance Reviews")

        with st.container(border=True):
            st.markdown("#### Training — Enter counts, we calculate percentages")
            show_example(
                "10 workers attended a fire safety demo in June = 10 trained "
                "on health & safety. 3 workers went for a welding skills course = "
                "3 trained on skill upgradation."
            )

            for tk, tlabel in [
                ("emp", "Employees"),
                ("wkr", "Workers"),
            ]:
                st.markdown(f"**{tlabel}**")
                tc = st.columns(5)
                default_total = (
                    (p3.get("perm_emp_m", 0) + p3.get("perm_emp_f", 0))
                    if tk == "emp"
                    else (p3.get("perm_wkr_m", 0) + p3.get("perm_wkr_f", 0))
                )
                p3[f"tr_{tk}_total"] = tc[0].number_input(
                    "Total",
                    min_value=0,
                    value=p3.get(f"tr_{tk}_total", default_total),
                    key=f"f_tr_{tk}_t"
                )
                p3[f"tr_{tk}_hs_cur"] = tc[1].number_input(
                    "H&S trained (Current)",
                    min_value=0,
                    value=p3.get(f"tr_{tk}_hs_cur", 0),
                    key=f"f_tr_{tk}_hc"
                )
                p3[f"tr_{tk}_sk_cur"] = tc[2].number_input(
                    "Skill trained (Current)",
                    min_value=0,
                    value=p3.get(f"tr_{tk}_sk_cur", 0),
                    key=f"f_tr_{tk}_sc"
                )
                p3[f"tr_{tk}_hs_prev"] = tc[3].number_input(
                    "H&S trained (Previous)",
                    min_value=0,
                    value=p3.get(f"tr_{tk}_hs_prev", 0),
                    key=f"f_tr_{tk}_hp"
                )
                p3[f"tr_{tk}_sk_prev"] = tc[4].number_input(
                    "Skill trained (Previous)",
                    min_value=0,
                    value=p3.get(f"tr_{tk}_sk_prev", 0),
                    key=f"f_tr_{tk}_sp"
                )

                total = p3[f"tr_{tk}_total"]
                hs_pct = safe_pct(p3[f"tr_{tk}_hs_cur"], total)
                sk_pct = safe_pct(p3[f"tr_{tk}_sk_cur"], total)
                show_calc(
                    f"{tlabel} — H&S: {hs_pct}% | Skill: {sk_pct}%"
                )
                st.markdown("")

        with st.container(border=True):
            st.markdown("#### Performance Reviews")
            show_example(
                "Annual appraisal, quarterly check-in, or even an informal "
                "conversation about the worker's performance counts."
            )

            for rk, rlabel in [("emp", "Employees"), ("wkr", "Workers")]:
                rc = st.columns(4)
                rc[0].markdown(f"**{rlabel}**")
                default_total = (
                    p3.get("tr_emp_total", 0) if rk == "emp"
                    else p3.get("tr_wkr_total", 0)
                )
                p3[f"rev_{rk}_total"] = rc[1].number_input(
                    "Total",
                    min_value=0,
                    value=p3.get(f"rev_{rk}_total", default_total),
                    key=f"f_rev_{rk}_t"
                )
                p3[f"rev_{rk}_done"] = rc[2].number_input(
                    "Reviews done",
                    min_value=0,
                    value=p3.get(f"rev_{rk}_done", 0),
                    key=f"f_rev_{rk}_d"
                )
                rev_pct = safe_pct(p3[f"rev_{rk}_done"], p3[f"rev_{rk}_total"])
                rc[3].metric("Coverage", f"{rev_pct}%")

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_full(); st.rerun()
        with c_next:
            if st.button("Next: Health & Safety →",
                         type="primary", use_container_width=True):
                next_full(); st.rerun()

    # ── FULL STEP 5: HEALTH & SAFETY ──────────────────────────────────────
    elif full_step == 5:
        st.header("🦺 Step 5 — Health & Safety")

        with st.container(border=True):
            st.markdown("#### Safety Management System")

            c1, c2 = st.columns(2)
            with c1:
                p3["ohs"] = st.radio(
                    "Do you have a formal safety management system?",
                    ["Yes", "No"],
                    horizontal=True,
                    index=0 if p3.get("ohs", "No") == "Yes" else 1,
                    key="f_ohs"
                )
                if p3["ohs"] == "Yes":
                    p3["ohs_coverage"] = st.text_input(
                        "Which areas does it cover?",
                        value=p3.get("ohs_coverage", ""),
                        placeholder="e.g. All factory floors",
                        key="f_ohs_cov"
                    )
                p3["worker_report"] = st.radio(
                    "Can workers report hazards without fear of punishment?",
                    ["Yes", "No"],
                    horizontal=True,
                    index=0 if p3.get("worker_report", "No") == "Yes" else 1,
                    key="f_wr"
                )
            with c2:
                p3["hazard_process"] = st.text_area(
                    "How do you identify workplace hazards?",
                    value=p3.get("hazard_process", ""),
                    height=80,
                    placeholder="e.g. Monthly safety walk by supervisor. "
                                "Workers report verbally to team leader.",
                    key="f_hp"
                )
                p3["non_occ_med"] = st.radio(
                    "Do workers have access to non-work medical services?",
                    ["Yes", "No"],
                    horizontal=True,
                    index=0 if p3.get("non_occ_med", "No") == "Yes" else 1,
                    key="f_nom"
                )

        with st.container(border=True):
            st.markdown("#### Jugaad Person-Hours Calculator")
            show_example(
                "15 workers × 300 days × 8 hours × 1 shift = 36,000 person-hours. "
                "We use this to calculate your LTIFR automatically."
            )

            total = p3.get("total_workforce", 1)
            jc = st.columns(4)
            days = jc[0].number_input(
                "Working days/year",
                min_value=1, max_value=365,
                value=p3.get("working_days", 300), key="f_j_days"
            )
            hours = jc[1].number_input(
                "Hours/day",
                min_value=1.0, max_value=24.0,
                value=float(p3.get("hours_per_day", 8.0)),
                step=0.5, key="f_j_hours"
            )
            shifts = jc[2].number_input(
                "Shifts/day",
                min_value=1, max_value=3,
                value=p3.get("shifts", 1), key="f_j_shifts"
            )

            p3["working_days"] = days
            p3["hours_per_day"] = hours
            p3["shifts"] = shifts
            person_hours = total * days * hours * shifts
            p3["person_hours"] = person_hours
            jc[3].metric("Person-Hours", f"{int(person_hours):,}")

        with st.container(border=True):
            st.markdown("#### Safety Incidents")
            show_example(
                "LTI = Lost Time Injury = someone missed work the NEXT day. "
                "High consequence = hospitalised for more than 24 hours or permanent disability."
            )

            inc_types = [
                ("lti",       "Lost Time Injuries (LTI)"),
                ("total_inj", "Total Recordable Injuries"),
                ("fatalities","Fatalities"),
                ("high_cons", "High Consequence Injuries"),
            ]

            for ikey, ilabel in inc_types:
                st.markdown(f"**{ilabel}**")
                row = st.columns(4)
                p3[f"{ikey}_ec"] = row[0].number_input(
                    "Employees (Cur)", min_value=0,
                    value=p3.get(f"{ikey}_ec", 0),
                    key=f"f_{ikey}_ec"
                )
                p3[f"{ikey}_wc"] = row[1].number_input(
                    "Workers (Cur)", min_value=0,
                    value=p3.get(f"{ikey}_wc", 0),
                    key=f"f_{ikey}_wc"
                )
                p3[f"{ikey}_ep"] = row[2].number_input(
                    "Employees (Prev)", min_value=0,
                    value=p3.get(f"{ikey}_ep", 0),
                    key=f"f_{ikey}_ep"
                )
                p3[f"{ikey}_wp"] = row[3].number_input(
                    "Workers (Prev)", min_value=0,
                    value=p3.get(f"{ikey}_wp", 0),
                    key=f"f_{ikey}_wp"
                )

            p3["lti_total"] = p3.get("lti_ec", 0) + p3.get("lti_wc", 0)

            # LTIFR
            ltifr_e = ltifr(p3.get("lti_ec", 0), person_hours)
            ltifr_w = ltifr(p3.get("lti_wc", 0), person_hours)
            p3["ltifr"] = ltifr_e

            st.markdown("")
            st.info(
                f"**Auto-calculated LTIFR:** "
                f"Employees = {ltifr_e if ltifr_e is not None else '—'} | "
                f"Workers = {ltifr_w if ltifr_w is not None else '—'} "
                f"(per 1,000,000 person-hours)"
            )

        with st.container(border=True):
            st.markdown("#### Safety Measures & Complaints")

            p3["safety_measures"] = st.text_area(
                "Describe your safety measures",
                value=p3.get("safety_measures", ""),
                height=80,
                placeholder="e.g. PPE provided to all workers, "
                            "monthly safety checks, first aid kits at workstations",
                key="f_sm"
            )

            st.markdown("**Complaints filed this year:**")
            cc = st.columns(4)
            p3["comp_wc_cur"] = cc[0].number_input(
                "Working conditions complaints",
                min_value=0,
                value=p3.get("comp_wc_cur", 0), key="f_comp_wc"
            )
            p3["comp_hs_cur"] = cc[1].number_input(
                "Health & safety complaints",
                min_value=0,
                value=p3.get("comp_hs_cur", 0), key="f_comp_hs"
            )
            p3["assessed_hs"] = cc[2].slider(
                "% of sites assessed for H&S",
                0, 100, p3.get("assessed_hs", 0), key="f_assessed"
            )

            p3["safety_corrective"] = st.text_area(
                "Corrective actions taken on safety issues (if any)",
                value=p3.get("safety_corrective", ""),
                height=60,
                placeholder="e.g. After injury in Q2, installed machine guards "
                            "and conducted mandatory safety training.",
                key="f_sc"
            )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_full(); st.rerun()
        with c_next:
            if st.button("Next: Leadership →",
                         type="primary", use_container_width=True):
                next_full(); st.rerun()

    # ── FULL STEP 6: LEADERSHIP ───────────────────────────────────────────
    elif full_step == 6:
        st.header("🏆 Step 6 — Leadership Indicators")
        st.info(
            "These are optional but show you go beyond minimum compliance. "
            "Large corporate buyers score vendors on these."
        )

        lt = st.tabs([
            "💀 Life Insurance",
            "💼 VC Dues",
            "🏥 Rehabilitation",
            "🚪 Transition",
            "🔍 VC Assessment",
            "🔧 VC Corrective"
        ])

        with lt[0]:
            c1, c2 = st.columns(2)
            with c1:
                p3["life_ins_emp"] = st.radio(
                    "Life insurance for employees on death?",
                    ["Yes", "No"],
                    horizontal=True,
                    index=0 if p3.get("life_ins_emp", "No") == "Yes" else 1,
                    key="f_li_e"
                )
            with c2:
                p3["life_ins_wkr"] = st.radio(
                    "Life insurance for workers on death?",
                    ["Yes", "No"],
                    horizontal=True,
                    index=0 if p3.get("life_ins_wkr", "No") == "Yes" else 1,
                    key="f_li_w"
                )

        with lt[1]:
            p3["vc_dues"] = st.text_area(
                "How do you ensure your suppliers deposit PF/ESI?",
                value=p3.get("vc_dues", ""),
                height=80,
                placeholder="e.g. All contractors must submit PF challan "
                            "receipts before invoice payment.",
                key="f_vcd"
            )

        with lt[2]:
            rc = st.columns(2)
            p3["rehab_emp"] = rc[0].number_input(
                "Employees rehabilitated after injury",
                min_value=0, value=p3.get("rehab_emp", 0), key="f_re"
            )
            p3["rehab_wkr"] = rc[1].number_input(
                "Workers rehabilitated after injury",
                min_value=0, value=p3.get("rehab_wkr", 0), key="f_rw"
            )

        with lt[3]:
            p3["transition"] = st.radio(
                "Do you provide transition assistance for retiring/leaving staff?",
                ["Yes", "No"],
                horizontal=True,
                index=0 if p3.get("transition", "No") == "Yes" else 1,
                key="f_trans"
            )
            if p3["transition"] == "Yes":
                p3["transition_desc"] = st.text_area(
                    "Describe briefly",
                    value=p3.get("transition_desc", ""),
                    height=60,
                    key="f_td"
                )

        with lt[4]:
            vc1, vc2 = st.columns(2)
            p3["vc_hs_pct"] = vc1.slider(
                "% of suppliers assessed for H&S",
                0, 100, p3.get("vc_hs_pct", 0), key="f_vc_hs"
            )
            p3["vc_wc_pct"] = vc2.slider(
                "% of suppliers assessed for Working Conditions",
                0, 100, p3.get("vc_wc_pct", 0), key="f_vc_wc"
            )

        with lt[5]:
            p3["vc_corrective"] = st.text_area(
                "Corrective actions from supplier assessments",
                value=p3.get("vc_corrective", ""),
                height=80,
                key="f_vcc"
            )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_full(); st.rerun()
        with c_next:
            if st.button("Next: Summary →",
                         type="primary", use_container_width=True):
                next_full(); st.rerun()

    # ── FULL STEP 7: SUMMARY ──────────────────────────────────────────────
    elif full_step == 7:
        st.header("✅ Principle 3 — Full Mode Summary")

        bank_score = calc_bank_score()
        p3["score"] = bank_score
        total = p3.get("total_workforce", 0)

        colour = ("green" if bank_score >= 70
                  else "orange" if bank_score >= 40 else "red")
        st.markdown(
            f"<h2 style='color:{colour}; text-align:center'>"
            f"{bank_score}/100</h2>"
            "<p style='text-align:center; color:gray'>Bank-Ready Score</p>",
            unsafe_allow_html=True
        )
        st.progress(bank_score / 100)

        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Workforce", total)
        m2.metric("Health Coverage",
                  f"{safe_pct(p3.get('health_covered', 0), total)}%")
        m3.metric("LTIFR", p3.get("ltifr", "—"))
        m4.metric("Safety Incidents", p3.get("lti_total", 0))

        st.markdown("---")
        with st.container(border=True):
            st.markdown("#### Recommendations")
            recs = 0
            health_pct = safe_pct(p3.get("health_covered", 0), total)
            if health_pct < 80 and total > 0:
                show_warn(f"Health coverage {health_pct}% — register with ESIC.")
                recs += 1
            if p3.get("pf_dep") == "N":
                show_bad("PF not deposited — legal violation.")
                recs += 1
            if recs == 0:
                show_good("No major compliance gaps in P3!")

        st.markdown("---")
        cf1, cf2, cf3 = st.columns([1, 2, 1])
        with cf2:
            if st.button("💾 Save P3 & Move to P4 →",
                         type="primary", use_container_width=True):
                st.session_state.c_p3 = p3
                st.balloons()
                st.success("✅ P3 saved! Next: Principle 4.")

        c_back2, _, _ = st.columns([1, 2, 1])
        with c_back2:
            if st.button("← Back", use_container_width=True):
                prev_full(); st.rerun()
                
# ─── BOTTOM NAVIGATION ──────────────────────────────────────────────────
from business_profile import render_section_navigation
render_section_navigation("Principle 3")