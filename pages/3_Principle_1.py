import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BRSR Section C | Principle 1",
    page_icon="⚖️",
    layout="centered"
)

from sidebar_footer import render_whatsapp_fab, render_pagehead
render_whatsapp_fab()

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    .benefit-box {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border-left: 5px solid #2e7d32;
        padding: 14px 18px;
        border-radius: 0 10px 10px 0;
        margin: 10px 0 16px 0;
    }
    .benefit-box b { color: #1b5e20; font-size: 15px; }
    .benefit-box p { color: #2e7d32; margin: 4px 0 0 0; font-size: 14px; }

    .essential-badge {
        background: #ffebee;
        color: #c62828;
        border: 1px solid #ef9a9a;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 12px;
        font-weight: 600;
    }
    .recommended-badge {
        background: #fff8e1;
        color: #e65100;
        border: 1px solid #ffcc02;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 12px;
        font-weight: 600;
    }
    .advanced-badge {
        background: #f3f4f6;
        color: #6b7280;
        border: 1px solid #d1d5db;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 12px;
        font-weight: 600;
    }

    .tip-box {
        background: #fff8e1;
        border-left: 4px solid #ffc107;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 13px;
        margin: 6px 0;
    }
    .how-to-box {
        background: #e3f2fd;
        border-left: 4px solid #1976d2;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 13px;
        margin: 6px 0;
    }
    .reaction-good {
        background: #e8f5e9;
        border: 1px solid #a5d6a7;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        color: #1b5e20;
        margin: 6px 0;
    }
    .reaction-warn {
        background: #fff3e0;
        border: 1px solid #ffcc80;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        color: #e65100;
        margin: 6px 0;
    }
    .reaction-bad {
        background: #ffebee;
        border: 1px solid #ef9a9a;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 13px;
        color: #c62828;
        margin: 6px 0;
    }
    .auto-calc {
        background: #f0f4ff;
        border: 1px solid #c7d2fe;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 14px;
        font-weight: 600;
        color: #3730a3;
        margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "c_p1" not in st.session_state:
    st.session_state.c_p1 = {}

if "step_c_p1" not in st.session_state:
    st.session_state.step_c_p1 = 1

p1 = st.session_state.c_p1
# ─── TIER LOGIC (NEW) ──────────────────────────────────────────
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from business_profile import (
    init_business_profile, show_tier_badge, show_sidebar_logo,
    get_business_type, has_board
)

init_business_profile()
show_tier_badge()
show_sidebar_logo()

# ─── END TIER LOGIC ────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def benefit(title, text):
    st.markdown(
        f'<div class="benefit-box"><b>💰 {title}</b><p>{text}</p></div>',
        unsafe_allow_html=True
    )

def tip(text):
    st.markdown(f'<div class="tip-box">💡 {text}</div>', unsafe_allow_html=True)

def how_to(text):
    st.markdown(f'<div class="how-to-box">📖 How to find this data: {text}</div>',
                unsafe_allow_html=True)

def auto_calc(text):
    st.markdown(f'<div class="auto-calc">🔢 {text}</div>', unsafe_allow_html=True)

def react_good(text):
    st.markdown(f'<div class="reaction-good">✅ {text}</div>', unsafe_allow_html=True)

def react_warn(text):
    st.markdown(f'<div class="reaction-warn">⚠️ {text}</div>', unsafe_allow_html=True)

def react_bad(text):
    st.markdown(f'<div class="reaction-bad">🚨 {text}</div>', unsafe_allow_html=True)

def badge(level):
    badges = {
        "essential":    '<span class="essential-badge">🔴 Essential</span>',
        "recommended":  '<span class="recommended-badge">🟡 Recommended</span>',
        "advanced":     '<span class="advanced-badge">⚪ Advanced</span>'
    }
    st.markdown(badges.get(level, ""), unsafe_allow_html=True)

def pct(num, den):
    try:
        if den and den > 0:
            return round((num / den) * 100, 1)
        return 0.0
    except:
        return 0.0

def go(step):
    st.session_state.step_c_p1 = step

# ─────────────────────────────────────────────────────────────────────────────
# SCORE CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────
def calc_p1_score():
    score = 0
    # Anti-bribery policy in place — real answer.
    if p1.get("anti_bribery_policy") == "Yes": score += 20
    # Anti-corruption training actually delivered.
    if p1.get("training_covered", 0) > 0: score += 20

    # Ethics disclosures (fines / disciplinary / conflict of interest):
    # credit genuine engagement, not merely landing on the step. The
    # *_answered flags were set on render, so a click-through scored +45.
    fines_clean = p1.get("has_fines") == "No — zero fines this year"
    fines_listed = (
        str(p1.get("has_fines", "")).startswith("Yes")
        and any((f or {}).get("authority") for f in p1.get("fines_list", []))
    )
    disc_total = (p1.get("disc_directors_cur", 0) + p1.get("disc_kmp_cur", 0) +
                  p1.get("disc_emp_cur", 0) + p1.get("disc_wkr_cur", 0))
    coi_total = p1.get("coi_dir_cur", 0) + p1.get("coi_kmp_cur", 0)
    ethics_engaged = (fines_clean or fines_listed or
                      disc_total > 0 or coi_total > 0)

    # Fines: clean record explicitly stated, or fines fully listed.
    if fines_clean or fines_listed: score += 15
    # Disciplinary & conflict-of-interest disclosures, once the user has
    # genuinely engaged with the ethics step.
    if ethics_engaged:
        score += 15   # disciplinary disclosure
        score += 15   # conflict-of-interest disclosure
    # Corrective-action narrative actually written.
    if p1.get("corrective_action"): score += 15
    return min(score, 100)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚖️ P1 Progress")
    score = calc_p1_score()
    p1["score"] = score
    st.progress(score / 100)
    st.metric("P1 Completion", f"{score}%")

    if score < 40:
        st.caption("🔴 Just getting started")
    elif score < 70:
        st.caption("🟡 Good progress")
    else:
        st.caption("🟢 Looking strong")

    st.divider()
    st.markdown("**Field Guide**")
    st.markdown("""
    🔴 **Essential** — Must fill  
    🟡 **Recommended** — Fill if possible  
    ⚪ **Advanced** — Large companies only
    """)

    st.divider()
    st.markdown("**📌 P1 In Plain English**")
    st.caption(
        "Principle 1 asks: Does your business operate honestly? "
        "Do you train your staff on ethics? Have you paid any fines? "
        "Do you have an anti-bribery policy? "
        "Banks and large buyers check this first."
    )

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
render_pagehead(
    "Step 3 of 9 · Principle 1",
    "Ethics & Transparency",
    "Show that your business runs with integrity — ethics training, "
    "anti-bribery measures, and how you handle any fines or complaints."
)

# Step nav
steps = {
    1: "📚 Training",
    2: "⚖️ Fines & Penalties",
    3: "🛡️ Anti-Bribery",
    4: "🚨 Disciplinary",
    5: "✅ Summary"
}
nav = st.columns(5)
for i, (num, label) in enumerate(steps.items()):
    with nav[i]:
        t = "primary" if st.session_state.step_c_p1 == num else "secondary"
        if st.button(label, key=f"nav_p1_{num}",
                     type=t, use_container_width=True):
            go(num)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# STEP 1: TRAINING & AWARENESS
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.step_c_p1 == 1:

    st.header("📚 Training & Awareness Programmes")

    benefit(
        "Why this matters for your business",
        "Businesses that train staff on ethics get faster approvals on "
        "government tenders, PSU contracts, and export certifications. "
        "Even one documented training session improves your score significantly."
    )

    # ── ESSENTIAL ─────────────────────────────────────────────────────────
    with st.container(border=True):
        badge("essential")
        st.markdown("#### How many training/awareness sessions did you conduct this year?")
        tip("A 'training session' can be as simple as a 30-minute staff meeting "
            "where you discussed honesty, anti-bribery, or company values. "
            "Even a WhatsApp message sent to all staff counts if it was awareness-focused.")

        # Data Not Available toggle
        dna_training = st.toggle(
            "I don't have this data",
            value=p1.get("dna_training", False),
            key="dna_training"
        )
        p1["dna_training"] = dna_training

        if dna_training:
            st.markdown('<div class="how-to-box">📖 How to find/estimate this:<br>'
                        '• Check WhatsApp groups — any awareness messages = 1 session<br>'
                        '• Check meeting minutes or attendance registers<br>'
                        '• Any induction/onboarding session for new staff counts<br>'
                        '• Even an informal daily briefing on work ethics counts</div>',
                        unsafe_allow_html=True)
            p1["total_training_sessions"] = 0
        else:
            p1["total_training_sessions"] = st.number_input(
                "Total number of training/awareness sessions held this year",
                min_value=0, value=p1.get("total_training_sessions", 0),
                help="Count every session — formal or informal"
            )

            if p1["total_training_sessions"] > 0:
                topics = st.text_input(
                    "What topics were covered?",
                    value=p1.get("training_topics", ""),
                    placeholder="e.g. Anti-bribery, Code of Conduct, Workplace Ethics, "
                                "Environmental Responsibility"
                )
                p1["training_topics"] = topics

        st.markdown("")
        st.markdown("**Coverage by staff category** — "
                    "how many people from each group attended?")
        how_to("Check attendance registers, meeting minutes, or WhatsApp group "
               "member lists. Divide attendees by total in that category × 100.")

        # Pull employee data from Section A if available
        total_emp = st.session_state.get("data", {}).get("total_perm_emp", 0)

        # Tier-aware column layout
        if has_board():
            c1, c2, c3, c4 = st.columns(4)
        else:
            c3, c4 = st.columns(2)

        if has_board():
            with c1:
                board_trained = st.number_input(
                    "Board / Directors trained",
                    min_value=0, value=p1.get("board_trained", 0),
                    key="board_trained"
                )
                board_total = st.number_input(
                    "Total directors",
                    min_value=0, value=p1.get("board_total", 1),
                    key="board_total_p1"
                )
                p1["board_trained"] = board_trained
                p1["board_total_train"] = board_total
                board_pct = pct(board_trained, board_total)
                auto_calc(f"Board coverage: {board_pct}%")

            with c2:
                kmp_trained = st.number_input(
                    "KMPs trained",
                    min_value=0, value=p1.get("kmp_trained", 0),
                    key="kmp_trained"
                )
                kmp_total = st.number_input(
                    "Total KMPs",
                    min_value=0, value=p1.get("kmp_total", 1),
                    key="kmp_total_p1"
                )
                p1["kmp_trained"] = kmp_trained
                p1["kmp_total_train"] = kmp_total
                kmp_pct = pct(kmp_trained, kmp_total)
                auto_calc(f"KMP coverage: {kmp_pct}%")
        else:
            # Sole prop / partnership - auto-fill zeros
            p1["board_trained"] = 0
            p1["board_total_train"] = 0
            p1["kmp_trained"] = 0
            p1["kmp_total_train"] = 0
            st.info(
                f"📌 Board & KMP training fields skipped for "
                f"**{get_business_type()}**. Continue with Employee and Worker training below."
            )

        with c3:
            emp_trained = st.number_input(
                "Employees trained",
                min_value=0, value=p1.get("emp_trained", 0),
                key="emp_trained"
            )
            emp_total = st.number_input(
                "Total employees",
                min_value=0,
                value=p1.get("emp_total_train", total_emp if total_emp else 0),
                key="emp_total_p1"
            )
            p1["emp_trained"] = emp_trained
            p1["emp_total_train"] = emp_total
            emp_pct = pct(emp_trained, emp_total)
            auto_calc(f"Employee coverage: {emp_pct}%")

            if emp_pct >= 80:
                react_good("Excellent training coverage — "
                           "this is a strong positive for loan applications.")
            elif emp_pct >= 50:
                react_warn("Decent coverage. Try to reach 80%+ "
                           "for maximum ESG score benefit.")
            elif emp_total > 0:
                react_bad("Low training coverage. Even one documented "
                          "all-staff meeting will improve this significantly.")

        with c4:
            wkr_trained = st.number_input(
                "Workers trained",
                min_value=0, value=p1.get("wkr_trained", 0),
                key="wkr_trained"
            )
            wkr_total = st.number_input(
                "Total workers",
                min_value=0, value=p1.get("wkr_total_train", 0),
                key="wkr_total_p1"
            )
            p1["wkr_trained"] = wkr_trained
            p1["wkr_total_train"] = wkr_total
            wkr_pct = pct(wkr_trained, wkr_total)
            auto_calc(f"Worker coverage: {wkr_pct}%")

        # Use 0 if board/kmp fields were hidden (non-board businesses)
        p1["training_covered"] = emp_trained + wkr_trained + p1.get("board_trained", 0) + p1.get("kmp_trained", 0)

    # ── RECOMMENDED — Value Chain Training ────────────────────────────────
    with st.container(border=True):
        badge("recommended")
        st.markdown("#### Did you conduct awareness sessions for your suppliers/partners?")
        tip("This is called 'Value Chain Training'. Even sharing a one-page ethics "
            "document with your top 3 suppliers qualifies.")

        p1["vc_training"] = st.radio(
            "Did you conduct any awareness programmes for your suppliers or "
            "business partners this year?",
            ["Yes", "No", "Not Applicable"],
            index=["Yes", "No", "Not Applicable"].index(
                p1.get("vc_training", "No")
            ),
            horizontal=True,
            key="vc_training_radio"
        )

        if p1["vc_training"] == "Yes":
            c5, c6 = st.columns(2)
            with c5:
                p1["vc_sessions"] = st.number_input(
                    "Number of sessions held",
                    min_value=1, value=p1.get("vc_sessions", 1)
                )
                p1["vc_topics"] = st.text_input(
                    "Topics covered",
                    value=p1.get("vc_topics", ""),
                    placeholder="e.g. Ethical sourcing, No child labour policy"
                )
            with c6:
                p1["vc_coverage_pct"] = st.slider(
                    "% of suppliers covered (by value of business)",
                    0, 100, p1.get("vc_coverage_pct", 0)
                )
                react_good(f"✅ {p1['vc_coverage_pct']}% of your supply chain "
                           "is covered by ethics awareness — excellent for export buyers.")

    # ── NAV ───────────────────────────────────────────────────────────────
    _, _, c_next = st.columns([1, 2, 1])
    with c_next:
        if st.button("Next: Fines & Penalties →",
                     type="primary", use_container_width=True):
            go(2); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 2: FINES & PENALTIES
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_c_p1 == 2:

    st.header("⚖️ Fines, Penalties & Legal Actions")

    benefit(
        "Why honest disclosure here helps you",
        "Disclosing zero fines or minor resolved fines actually builds MORE trust "
        "than not disclosing at all. Banks and buyers respect transparency. "
        "Hiding a penalty that later surfaces is far more damaging."
    )

    # ── ESSENTIAL — Monetary Fines ────────────────────────────────────────
    with st.container(border=True):
        badge("essential")
        st.markdown("#### Monetary Fines & Penalties This Year")
        how_to("Check your bank statements for payments to government accounts. "
               "Common sources: GST late fees, labour law penalties, "
               "pollution board fines, municipal notices, court orders.")

        has_fines = st.radio(
            "Did your business pay any monetary fines or penalties to any "
            "government authority or court this year?",
            ["No — zero fines this year", "Yes — we paid some fines"],
            index=0 if p1.get("has_fines", "No") == "No — zero fines this year" else 1,
            key="has_fines_radio"
        )
        p1["has_fines"] = has_fines

        if has_fines == "No — zero fines this year":
            react_good("Zero fines — this is excellent. "
                       "It shows clean regulatory compliance.")
            p1["fines_total"] = 0
        else:
            st.markdown("")
            num_fines = st.number_input(
                "How many separate fines/penalties?",
                min_value=1, max_value=20, value=p1.get("num_fines", 1)
            )
            p1["num_fines"] = int(num_fines)

            fines_list = p1.get("fines_list", [{}] * int(num_fines))
            if len(fines_list) < int(num_fines):
                fines_list += [{}] * (int(num_fines) - len(fines_list))

            total_fine_amount = 0
            for i in range(int(num_fines)):
                st.markdown(f"**Fine {i+1}**")
                ff1, ff2, ff3, ff4 = st.columns([2, 2, 2, 1])
                with ff1:
                    authority = st.text_input(
                        "Regulatory authority",
                        value=fines_list[i].get("authority", ""),
                        key=f"fine_auth_{i}",
                        placeholder="e.g. GST Department, Labour Office, CPCB"
                    )
                with ff2:
                    brief = st.text_input(
                        "Brief reason",
                        value=fines_list[i].get("brief", ""),
                        key=f"fine_brief_{i}",
                        placeholder="e.g. Late GST filing, Labour law violation"
                    )
                with ff3:
                    amount = st.number_input(
                        "Amount paid (₹)",
                        min_value=0,
                        value=fines_list[i].get("amount", 0),
                        key=f"fine_amt_{i}"
                    )
                with ff4:
                    appeal = st.radio(
                        "Appeal filed?",
                        ["No", "Yes"],
                        key=f"fine_appeal_{i}",
                        horizontal=True,
                        index=0 if fines_list[i].get("appeal", "No") == "No" else 1
                    )
                fines_list[i] = {
                    "authority": authority,
                    "brief": brief,
                    "amount": amount,
                    "appeal": appeal
                }
                total_fine_amount += amount

            p1["fines_list"] = fines_list
            p1["fines_total"] = total_fine_amount
            auto_calc(f"Total fines paid this year: ₹{total_fine_amount:,}")

            if total_fine_amount > 100000:
                react_bad("Total fines above ₹1 lakh. Add corrective action "
                          "details in Step 5 — this reassures banks and buyers "
                          "that you have fixed the issue.")
            elif total_fine_amount > 0:
                react_warn("Some fines paid. As long as they are resolved and "
                           "corrective actions are taken, this is manageable.")

        p1["fines_answered"] = True

    # ── RECOMMENDED — Non-Monetary ────────────────────────────────────────
    with st.container(border=True):
        badge("recommended")
        st.markdown("#### Non-Monetary Actions (Warnings, Show-cause notices)")
        tip("Non-monetary means no fine was paid but official action was taken — "
            "like a show-cause notice, warning letter, or official inspection.")

        has_nonmon = st.radio(
            "Did your business receive any non-monetary actions from any authority?",
            ["No", "Yes"],
            index=0 if p1.get("has_nonmon", "No") == "No" else 1,
            horizontal=True,
            key="has_nonmon_radio"
        )
        p1["has_nonmon"] = has_nonmon

        if has_nonmon == "Yes":
            p1["nonmon_desc"] = st.text_area(
                "Brief description",
                value=p1.get("nonmon_desc", ""),
                placeholder="e.g. Received show-cause notice from labour office "
                            "regarding contract worker registration. "
                            "Resolved within 30 days.",
                height=80
            )

    # ── ADVANCED — Imprisonment ───────────────────────────────────────────
    with st.expander("⚪ Advanced — For larger businesses only"):
        badge("advanced")
        st.markdown("#### Imprisonment or serious legal punishments")
        st.caption("Most MSMEs will never face this. Only fill if applicable.")

        p1["has_imprisonment"] = st.radio(
            "Has any director or KMP faced imprisonment related to business conduct?",
            ["No", "Yes"],
            horizontal=True,
            index=0 if p1.get("has_imprisonment", "No") == "No" else 1,
            key="imprisonment_radio"
        )

        if p1["has_imprisonment"] == "Yes":
            p1["imprisonment_desc"] = st.text_area(
                "Brief details",
                value=p1.get("imprisonment_desc", ""),
                height=80
            )

    # ── NAV ───────────────────────────────────────────────────────────────
    c_back, _, c_next = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go(1); st.rerun()
    with c_next:
        if st.button("Next: Anti-Bribery Policy →",
                     type="primary", use_container_width=True):
            go(3); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 3: ANTI-BRIBERY & CONFLICT OF INTEREST
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_c_p1 == 3:

    st.header("🛡️ Anti-Bribery Policy & Conflict of Interest")

    benefit(
        "This single policy unlocks major opportunities",
        "Having a written anti-bribery policy makes you a 'Preferred Vendor' "
        "for government tenders and PSU contracts. Most large Indian corporates "
        "now ask for this in their vendor onboarding checklist. "
        "It takes 30 minutes to create and lasts forever."
    )

    # ── ESSENTIAL — Anti-Bribery Policy ──────────────────────────────────
    with st.container(border=True):
        badge("essential")
        st.markdown("#### Do you have an Anti-Corruption / Anti-Bribery Policy?")
        tip("This can be a one-paragraph written statement that says your business "
            "does not give or accept bribes. It does not need to be a 10-page document.")

        p1["anti_bribery_policy"] = st.radio(
            "Do you have a written anti-corruption or anti-bribery policy?",
            ["Yes", "No", "In Progress"],
            index=["Yes", "No", "In Progress"].index(
                p1.get("anti_bribery_policy", "No")
            ),
            key="anti_bribery_radio"
        )

        if p1["anti_bribery_policy"] == "Yes":
            react_good("Excellent — having this policy significantly improves "
                       "your vendor eligibility for large companies and government.")
            p1["anti_bribery_link"] = st.text_input(
                "Link to policy on your website (optional)",
                value=p1.get("anti_bribery_link", ""),
                placeholder="e.g. www.yourbusiness.com/anti-bribery-policy"
            )
            p1["anti_bribery_summary"] = st.text_area(
                "Brief summary of the policy",
                value=p1.get("anti_bribery_summary", ""),
                height=80,
                placeholder="e.g. Our company strictly prohibits giving or receiving "
                            "bribes in any form. Any employee found in violation will "
                            "face immediate disciplinary action."
            )

        elif p1["anti_bribery_policy"] == "No":
            react_bad("No anti-bribery policy yet. Use the generator below "
                      "to create one in 1 click — it takes 30 seconds.")

            if st.button("✨ Generate Anti-Bribery Policy Statement", type="primary"):
                company = st.session_state.get(
                    "data", {}
                ).get("company_name", "Our Company")
                p1["generated_policy"] = (
                    f"{company} is committed to conducting all business with "
                    f"integrity and in compliance with applicable laws. "
                    f"We strictly prohibit offering, giving, soliciting, or "
                    f"receiving any bribe or corrupt payment in any form — "
                    f"whether in cash, gifts, hospitality, or any other benefit. "
                    f"Any employee, worker, or partner found in violation of this "
                    f"policy will face immediate disciplinary action, including "
                    f"termination of employment or contract. "
                    f"This policy applies to all staff, contractors, and value "
                    f"chain partners of {company}."
                )

            if p1.get("generated_policy"):
                st.markdown("**📄 Your Auto-Generated Policy — Copy, Print and Sign:**")
                st.markdown(
                    f'<div style="background:#f0fff4; border:1px dashed #2e7d32; '
                    f'border-radius:8px; padding:16px; font-size:13px; '
                    f'line-height:1.7;">{p1["generated_policy"]}</div>',
                    unsafe_allow_html=True
                )
                st.caption("Print this, sign it as the business owner, "
                           "and file it. You now have an anti-bribery policy.")

        else:
            react_warn("Policy in progress — mark it complete once it's written "
                       "and signed. Even a draft improves your score.")

    # ── ESSENTIAL — Disciplinary Actions ─────────────────────────────────
    with st.container(border=True):
        badge("essential")
        st.markdown("#### Disciplinary Actions for Bribery/Corruption")
        how_to("Check your HR records or warning letters issued this year. "
               "If none were issued, that is a positive answer.")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Current Financial Year**")
            p1["disc_directors_cur"] = st.number_input(
                "Directors disciplined", min_value=0,
                value=p1.get("disc_directors_cur", 0), key="disc_dir_cur"
            )
            p1["disc_kmp_cur"] = st.number_input(
                "KMPs disciplined", min_value=0,
                value=p1.get("disc_kmp_cur", 0), key="disc_kmp_cur"
            )
            p1["disc_emp_cur"] = st.number_input(
                "Employees disciplined", min_value=0,
                value=p1.get("disc_emp_cur", 0), key="disc_emp_cur"
            )
            p1["disc_wkr_cur"] = st.number_input(
                "Workers disciplined", min_value=0,
                value=p1.get("disc_wkr_cur", 0), key="disc_wkr_cur"
            )

        with c2:
            st.markdown("**Previous Financial Year**")
            p1["disc_directors_prev"] = st.number_input(
                "Directors disciplined", min_value=0,
                value=p1.get("disc_directors_prev", 0), key="disc_dir_prev"
            )
            p1["disc_kmp_prev"] = st.number_input(
                "KMPs disciplined", min_value=0,
                value=p1.get("disc_kmp_prev", 0), key="disc_kmp_prev"
            )
            p1["disc_emp_prev"] = st.number_input(
                "Employees disciplined", min_value=0,
                value=p1.get("disc_emp_prev", 0), key="disc_emp_prev"
            )
            p1["disc_wkr_prev"] = st.number_input(
                "Workers disciplined", min_value=0,
                value=p1.get("disc_wkr_prev", 0), key="disc_wkr_prev"
            )

        total_disc = (p1["disc_directors_cur"] + p1["disc_kmp_cur"] +
                      p1["disc_emp_cur"] + p1["disc_wkr_cur"])

        if total_disc == 0:
            react_good("Zero disciplinary actions — clean record on ethics enforcement.")
        else:
            react_warn(f"{total_disc} disciplinary action(s) taken. "
           "Go to Step 4 to document what corrective steps you took.")

        p1["disciplinary_answered"] = True

    # ── ESSENTIAL — Conflict of Interest ─────────────────────────────────
    with st.container(border=True):
        badge("essential")
        st.markdown("#### Conflict of Interest Complaints")
        tip("A 'conflict of interest' means a director or senior manager made a "
            "decision that personally benefited them at the company's expense. "
            "Example: a director awarding a contract to their own family business "
            "without disclosing the relationship.")

        c3, c4 = st.columns(2)
        with c3:
            st.markdown("**Current Financial Year**")
            p1["coi_dir_cur"] = st.number_input(
                "COI complaints against Directors",
                min_value=0, value=p1.get("coi_dir_cur", 0), key="coi_dir_c"
            )
            p1["coi_kmp_cur"] = st.number_input(
                "COI complaints against KMPs",
                min_value=0, value=p1.get("coi_kmp_cur", 0), key="coi_kmp_c"
            )
        with c4:
            st.markdown("**Previous Financial Year**")
            p1["coi_dir_prev"] = st.number_input(
                "COI complaints against Directors",
                min_value=0, value=p1.get("coi_dir_prev", 0), key="coi_dir_p"
            )
            p1["coi_kmp_prev"] = st.number_input(
                "COI complaints against KMPs",
                min_value=0, value=p1.get("coi_kmp_prev", 0), key="coi_kmp_p"
            )

        total_coi = p1["coi_dir_cur"] + p1["coi_kmp_cur"]
        if total_coi == 0:
            react_good("No conflict of interest complaints — "
                       "strong governance signal.")
        else:
            react_bad(f"{total_coi} COI complaints filed. "
                      "Add resolution details in the Summary step.")

        p1["conflict_answered"] = True

    # ── ADVANCED — COI Management Process ────────────────────────────────
    with st.expander("⚪ Advanced — For larger businesses only"):
        badge("advanced")
        st.markdown("#### Do you have a formal process to manage conflicts of interest "
                    "at Board level?")
        st.caption("Most MSMEs handle this informally. "
                   "Only fill if you have a documented process.")
        p1["coi_process"] = st.radio(
            "Do you have a formal COI management process for Board members?",
            ["Yes", "No"],
            horizontal=True,
            index=0 if p1.get("coi_process", "No") == "Yes" else 1,
            key="coi_process_radio"
        )
        if p1["coi_process"] == "Yes":
            p1["coi_process_desc"] = st.text_area(
                "Describe the process briefly",
                value=p1.get("coi_process_desc", ""),
                height=80,
                placeholder="e.g. Directors must declare interests annually. "
                            "Conflicted directors recuse from relevant votes."
            )

    # ── NAV ───────────────────────────────────────────────────────────────
    c_back, _, c_next = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go(2); st.rerun()
    with c_next:
        if st.button("Next: Disciplinary & Corrective Actions →",
                     type="primary", use_container_width=True):
            go(4); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 4: CORRECTIVE ACTIONS
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_c_p1 == 4:

    st.header("🔧 Corrective Actions & Appeals")

    benefit(
        "Corrective actions show maturity — not weakness",
        "Showing that you identified a problem AND fixed it is more impressive "
        "to banks and auditors than claiming zero issues. "
        "It shows your business has strong self-governance."
    )

    # ── ESSENTIAL ─────────────────────────────────────────────────────────
    with st.container(border=True):
        badge("essential")
        st.markdown("#### Have you taken any corrective actions for fines, "
                    "penalties, or corruption-related issues this year?")
        tip("Corrective action = what you did to prevent the same problem "
            "from happening again. Example: After a GST penalty for late filing, "
            "you hired an accountant to handle monthly filings.")

        has_corrective = st.radio(
            "Did you take any corrective action related to fines, penalties, "
            "or ethics violations this year?",
            ["No issues requiring corrective action",
             "Yes — we took corrective action"],
            index=0 if p1.get(
                "has_corrective", "No issues requiring corrective action"
            ) == "No issues requiring corrective action" else 1,
            key="corrective_radio"
        )
        p1["has_corrective"] = has_corrective

        if has_corrective == "Yes — we took corrective action":
            p1["corrective_action"] = st.text_area(
                "Describe the corrective action taken",
                value=p1.get("corrective_action", ""),
                height=120,
                placeholder="e.g. After disciplinary action against an employee for accepting "
                            "a gift from a vendor:\n"
                            "1. Issued formal warning and updated code of conduct\n"
                            "2. Conducted all-staff ethics training session\n"
            "3. Implemented gift declaration policy going forward"
            )
            react_good("Documented corrective actions show strong governance. "
                       "This will be highlighted positively in your BRSR report.")
        else:
            p1["corrective_action"] = ""
            react_good("No corrective actions needed — clean compliance record.")

        p1["corrective_action"] = p1.get("corrective_action", "")

    # ── RECOMMENDED — Appeals ─────────────────────────────────────────────
    with st.container(border=True):
        badge("recommended")
        st.markdown("#### Any appeals filed against penalties?")
        tip("If you disagreed with a fine and filed an appeal with the court "
            "or appellate authority, mention it here.")

        has_appeal = st.radio(
            "Did you file any appeal against a regulatory penalty this year?",
            ["No", "Yes"],
            horizontal=True,
            index=0 if p1.get("has_appeal", "No") == "No" else 1,
            key="appeal_radio"
        )
        p1["has_appeal"] = has_appeal

        if has_appeal == "Yes":
            p1["appeal_desc"] = st.text_area(
                "Brief details of the appeal",
                value=p1.get("appeal_desc", ""),
                height=80,
                placeholder="e.g. Filed appeal against GST penalty of ₹45,000 "
                            "with GST Appellate Authority. Case pending."
            )

    # ── NAV ───────────────────────────────────────────────────────────────
    c_back, _, c_next = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go(3); st.rerun()
    with c_next:
        if st.button("Next: P1 Summary →",
                     type="primary", use_container_width=True):
            go(5); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 5: P1 SUMMARY
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_c_p1 == 5:

    st.header("✅ Principle 1 — Summary & Score")

    final_score = calc_p1_score()

    # ── SCORE ─────────────────────────────────────────────────────────────
    sc1, sc2 = st.columns([1, 2])
    with sc1:
        colour = "green" if final_score >= 70 else "orange" if final_score >= 40 else "red"
        st.markdown(
            f"<h1 style='color:{colour}; text-align:center'>{final_score}%</h1>"
            "<p style='text-align:center; color:gray'>P1 Completion Score</p>",
            unsafe_allow_html=True
        )
        st.progress(final_score / 100)
    with sc2:
        if final_score >= 70:
            react_good("Strong P1 disclosure. Your ethics and governance "
                       "section will impress banks and large buyers.")
        elif final_score >= 40:
            react_warn("Good start. Complete the missing fields below "
                       "to strengthen your P1 score.")
        else:
            react_bad("Several essential fields are incomplete. "
                      "Go back and fill the highlighted sections.")

    # ── SUMMARY TABLE ─────────────────────────────────────────────────────
    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### Your P1 Data Summary")

        st.markdown("**Training & Awareness**")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sessions Held",
                  p1.get("total_training_sessions", 0))
        c2.metric("Board Coverage",
                  f"{pct(p1.get('board_trained',0), p1.get('board_total_train',1))}%")
        c3.metric("Employee Coverage",
                  f"{pct(p1.get('emp_trained',0), p1.get('emp_total_train',1))}%")
        c4.metric("Worker Coverage",
                  f"{pct(p1.get('wkr_trained',0), p1.get('wkr_total_train',1))}%")

        st.markdown("**Ethics & Compliance**")
        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Anti-Bribery Policy",
                  p1.get("anti_bribery_policy", "Not filled"))
        c6.metric("Total Fines Paid",
                  f"₹{p1.get('fines_total', 0):,}")
        c7.metric("Disciplinary Actions",
                  p1.get("disc_emp_cur", 0) + p1.get("disc_wkr_cur", 0))
        c8.metric("COI Complaints",
                  p1.get("coi_dir_cur", 0) + p1.get("coi_kmp_cur", 0))

    # ── SMART RECOMMENDATIONS ─────────────────────────────────────────────
    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### 💡 Recommendations to Improve P1")

        recs = 0
        if p1.get("anti_bribery_policy") != "Yes":
            react_bad("Create your anti-bribery policy today. "
                      "Use the generator in Step 3. It takes 5 minutes.")
            recs += 1

        emp_cov = pct(p1.get("emp_trained", 0), p1.get("emp_total_train", 1))
        if emp_cov < 50:
            react_warn(f"Employee training coverage is {emp_cov}%. "
                       "Schedule one all-staff meeting and document attendance. "
                       "That alone will bring this to 100%.")
            recs += 1

        if p1.get("has_fines") == "Yes — we paid some fines" and \
                not p1.get("corrective_action"):
            react_warn("You reported fines but no corrective actions. "
                       "Go back to Step 4 and document what you fixed. "
                       "This is critical for credibility.")
            recs += 1

        if not p1.get("dna_training") and p1.get("total_training_sessions", 0) == 0:
            react_warn("No training sessions recorded. Even informal awareness "
                       "activities count. Document them.")
            recs += 1

        if recs == 0:
            react_good("No major gaps in P1! "
                       "Proceed to Principle 2 — Sustainable Products.")

    # ── BANK BENEFIT SCORE ────────────────────────────────────────────────
    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### 🏦 Bank-Ready Score for P1")
        tip("This shows how your P1 disclosure looks to a bank loan officer "
            "reviewing your BRSR report.")

        bank_score = 0
        bank_items = []

        if p1.get("anti_bribery_policy") == "Yes":
            bank_score += 30
            bank_items.append(("✅ Anti-bribery policy in place", "+30"))
        else:
            bank_items.append(("❌ No anti-bribery policy", "+0"))

        if p1.get("fines_total", 0) == 0:
            bank_score += 25
            bank_items.append(("✅ Zero regulatory fines", "+25"))
        elif p1.get("corrective_action"):
            bank_score += 15
            bank_items.append(("🔄 Fines paid but corrective action taken", "+15"))
        else:
            bank_items.append(("⚠️ Fines paid, no corrective action documented", "+0"))

        emp_cov2 = pct(p1.get("emp_trained", 0), p1.get("emp_total_train", 1))
        if emp_cov2 >= 80:
            bank_score += 25
            bank_items.append((f"✅ {emp_cov2}% staff trained on ethics", "+25"))
        elif emp_cov2 >= 50:
            bank_score += 15
            bank_items.append((f"🔄 {emp_cov2}% staff trained — needs improvement", "+15"))
        else:
            bank_items.append((f"❌ Only {emp_cov2}% staff trained", "+0"))

        if p1.get("coi_dir_cur", 0) == 0 and p1.get("coi_kmp_cur", 0) == 0:
            bank_score += 20
            bank_items.append(("✅ No conflict of interest complaints", "+20"))
        else:
            bank_items.append(("⚠️ COI complaints on record", "+0"))

        for item, pts in bank_items:
            st.markdown(f"{item} &nbsp;&nbsp; `{pts} points`")

        st.markdown("")
        bank_colour = "green" if bank_score >= 70 else \
                      "orange" if bank_score >= 40 else "red"
        st.markdown(
            f"**Bank-Ready Score: "
            f"<span style='color:{bank_colour}'>{bank_score}/100</span>**",
            unsafe_allow_html=True
        )

        if bank_score >= 70:
            st.success("🏦 Strong governance profile. You are likely to get "
                       "faster approvals on MSME loans and PSU vendor registration.")
        elif bank_score >= 40:
            st.warning("🏦 Moderate profile. Completing the anti-bribery policy "
                       "and training documentation will significantly improve this.")
        else:
            st.error("🏦 Weak governance profile currently. "
                     "Banks and large buyers will flag this. "
                     "Fix the anti-bribery policy first — it's the biggest item.")

    # ── SAVE & PROCEED ────────────────────────────────────────────────────
    st.markdown("---")
    cf1, cf2, cf3 = st.columns([1, 2, 1])
    with cf2:
        if st.button("💾 Save P1 & Move to Principle 2 →",
                     type="primary", use_container_width=True):
            st.session_state.c_p1 = p1
            st.balloons()
            st.success("✅ Principle 1 saved! "
                       "Next: Principle 2 — Sustainable Products & Services.")

    c_back, _, _ = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back to Corrective Actions", use_container_width=True):
            go(4); st.rerun()
            
# ─── BOTTOM NAVIGATION ──────────────────────────────────────────────────
from business_profile import render_section_navigation
render_section_navigation("Principle 1")