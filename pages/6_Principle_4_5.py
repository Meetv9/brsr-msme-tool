import streamlit as st
import pandas as pd
from sidebar_footer import render_sidebar_footer
render_sidebar_footer()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BRSR Section C Principle 4 & 5 | Stakeholders & Human Rights",
    page_icon="🤝",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; max-width: 820px; }
    .question-card {
        background: #fff;
        border: 1.5px solid #e0f2e9;
        border-radius: 16px;
        padding: 24px 28px;
        margin: 12px 0;
        box-shadow: 0 2px 8px rgba(46,125,50,0.06);
    }
    .why-box {
        background: #e8f5e9;
        border-left: 4px solid #43a047;
        padding: 8px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 13px;
        color: #2e7d32;
        margin: 10px 0;
    }
    .example-box {
        background: #fff8e1;
        border-left: 4px solid #ffc107;
        padding: 8px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 13px;
        color: #5d4037;
        margin: 8px 0;
    }
    .calc-box {
        background: #f0f4ff;
        border: 1px solid #c7d2fe;
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 15px;
        font-weight: 600;
        color: #3730a3;
        margin: 10px 0;
        text-align: center;
    }
    .good-box {
        background: #e8f5e9;
        border: 1px solid #a5d6a7;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 13px;
        color: #1b5e20;
        margin: 6px 0;
    }
    .warn-box {
        background: #fff3e0;
        border: 1px solid #ffcc80;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 13px;
        color: #e65100;
        margin: 6px 0;
    }
    .bad-box {
        background: #ffebee;
        border: 1px solid #ef9a9a;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 13px;
        color: #c62828;
        margin: 6px 0;
    }
    .stakeholder-btn {
        display: inline-block;
        background: #e8f5e9;
        border: 2px solid #a5d6a7;
        border-radius: 20px;
        padding: 6px 14px;
        font-size: 13px;
        margin: 4px;
        cursor: pointer;
    }
    .stakeholder-selected {
        background: #2e7d32;
        border-color: #2e7d32;
        color: white;
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
        text-align: center;
        margin: 8px;
    }
    .essential-badge {
        background: #ffebee; color: #c62828;
        border: 1px solid #ef9a9a; border-radius: 20px;
        padding: 2px 12px; font-size: 12px; font-weight: 600;
    }
    .leadership-badge {
        background: #fffde7; color: #f57f17;
        border: 1px solid #ffd54f; border-radius: 20px;
        padding: 2px 12px; font-size: 12px; font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "p45_mode" not in st.session_state:
    st.session_state.p45_mode = None

if "p45_quick_step" not in st.session_state:
    st.session_state.p45_quick_step = 1

if "p45_full_step" not in st.session_state:
    st.session_state.p45_full_step = 1

if "p45" not in st.session_state:
    st.session_state.p45 = {}

p = st.session_state.p45

# Pre-fill from Section A
sec_a = st.session_state.get("data", {})
if "total_workforce" not in p:
    total_from_a = (
        sec_a.get("total_perm_emp", 0) +
        sec_a.get("total_temp_emp", 0) +
        sec_a.get("total_perm_wkr", 0) +
        sec_a.get("total_temp_wkr", 0)
    )
    if total_from_a > 0:
        p["total_workforce"] = total_from_a

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def why(text):
    st.markdown(f'<div class="why-box">💰 {text}</div>', unsafe_allow_html=True)

def example(text):
    st.markdown(f'<div class="example-box">📌 Example: {text}</div>',
                unsafe_allow_html=True)

def calc(text):
    st.markdown(f'<div class="calc-box">🔢 {text}</div>', unsafe_allow_html=True)

def good(text):
    st.markdown(f'<div class="good-box">✅ {text}</div>', unsafe_allow_html=True)

def warn(text):
    st.markdown(f'<div class="warn-box">⚠️ {text}</div>', unsafe_allow_html=True)

def bad(text):
    st.markdown(f'<div class="bad-box">🚨 {text}</div>', unsafe_allow_html=True)

def badge_e():
    st.markdown('<span class="essential-badge">🔴 Essential</span>',
                unsafe_allow_html=True)

def badge_l():
    st.markdown('<span class="leadership-badge">🟡 Leadership</span>',
                unsafe_allow_html=True)

def safe_pct(n, d):
    try:
        n, d = float(n or 0), float(d or 0)
        return round((n / d) * 100, 1) if d > 0 else 0.0
    except:
        return 0.0

def next_q():
    st.session_state.p45_quick_step += 1

def prev_q():
    st.session_state.p45_quick_step -= 1

def next_f():
    st.session_state.p45_full_step += 1

def prev_f():
    st.session_state.p45_full_step -= 1

# ─────────────────────────────────────────────────────────────────────────────
# BANK SCORE
# ─────────────────────────────────────────────────────────────────────────────
def calc_bank_score():
    score = 0
    if p.get("stakeholders_selected"):      score += 15
    if p.get("engage_freq"):                score += 10
    if p.get("min_wage") == "Yes":          score += 20
    if p.get("focal_point") == "Yes":       score += 15
    if p.get("hr_in_contracts") == "Yes":   score += 10
    total = p.get("total_workforce", 1)
    tr_pct = safe_pct(p.get("hr_trained", 0), total)
    if tr_pct >= 80:   score += 20
    elif tr_pct >= 50: score += 10
    if (p.get("child_labour_complaints", 0) == 0 and
            p.get("forced_labour_complaints", 0) == 0): score += 10
    return min(score, 100)

# ─────────────────────────────────────────────────────────────────────────────
# MODE SELECTION
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.p45_mode is None:

    st.markdown("## 🤝 Principles 4 & 5")
    st.markdown("**Stakeholder Engagement** and **Human Rights**")
    st.markdown("")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="mode-card">
            <div style="font-size:40px">⚡</div>
            <div style="font-size:20px; font-weight:700; color:#2e7d32;">Quick Mode</div>
            <div style="font-size:14px; color:#555; margin-top:8px;">
                10 simple questions<br>
                P4 + P5 together<br>
                Under 10 minutes<br>
                No tables, no calculations
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Quick Mode ⚡",
                     use_container_width=True, type="primary"):
            st.session_state.p45_mode = "quick"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="mode-card">
            <div style="font-size:40px">📋</div>
            <div style="font-size:20px; font-weight:700; color:#1565c0;">Full Mode</div>
            <div style="font-size:14px; color:#555; margin-top:8px;">
                All Essential + Leadership<br>
                Complete SEBI tables<br>
                Auto-calculated percentages<br>
                For consultants or serious users
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Full Mode 📋",
                     use_container_width=True):
            st.session_state.p45_mode = "full"
            st.rerun()

    st.info("💡 Start with Quick Mode if you're filling this for the first time.")
    st.stop()

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    mode_label = "⚡ Quick Mode" if st.session_state.p45_mode == "quick" else "📋 Full Mode"
    st.markdown(f"## 🤝 Principles 4 & 5 &nbsp; `{mode_label}`")
with col_h2:
    if st.button("Switch Mode"):
        st.session_state.p45_mode = None
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# ████████████████████  QUICK MODE  ██████████████████████████████████████████
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.p45_mode == "quick":

    TOTAL = 10
    step = st.session_state.p45_quick_step

    st.markdown(f'<div style="font-size:13px;color:#666;">Question {min(step,TOTAL)} of {TOTAL}</div>',
                unsafe_allow_html=True)
    st.progress(min(step, TOTAL) / TOTAL)
    st.markdown("")

    # ── Q1: WHO DO YOU DEAL WITH ──────────────────────────────────────────
    if step == 1:
        st.markdown("### 👥 Who do you regularly deal with in your business?")
        why(
            "Knowing your stakeholders shows banks and buyers that you run "
            "a responsible, well-connected business."
        )
        example(
            "A small garment factory deals with: Workers (daily), "
            "Fabric suppliers (weekly), Customers (monthly), "
            "Local community (occasionally)."
        )

        st.markdown("**Tap to select all that apply:**")

        presets = [
            ("workers",   "👷 Workers / Employees"),
            ("customers", "🛒 Customers / Buyers"),
            ("suppliers", "🏭 Suppliers / Vendors"),
            ("community", "🏘️ Local Community"),
            ("banks",     "🏦 Banks / Lenders"),
            ("govt",      "🏛️ Government / Regulators"),
        ]

        selected = p.get("stakeholders_selected", [])

        cols = st.columns(3)
        for i, (key, label) in enumerate(presets):
            with cols[i % 3]:
                if st.checkbox(label, value=(key in selected), key=f"sh_{key}"):
                    if key not in selected:
                        selected.append(key)
                else:
                    if key in selected:
                        selected.remove(key)

        p["stakeholders_selected"] = selected

        others = st.text_input(
            "Any others not listed above?",
            value=p.get("stakeholders_other", ""),
            placeholder="e.g. NGOs, Industry associations"
        )
        p["stakeholders_other"] = others

        if selected:
            good(f"You deal with {len(selected)} stakeholder group(s) — good.")
        else:
            warn("Select at least one group to continue.")

        _, c_next = st.columns([1, 1])
        with c_next:
            if st.button("Next →", type="primary",
                         use_container_width=True,
                         disabled=not selected):
                next_q(); st.rerun()

    # ── Q2: HOW OFTEN DO YOU ENGAGE ───────────────────────────────────────
    elif step == 2:
        st.markdown("### 💬 How often do you communicate with the people in your business?")
        why(
            "Regular communication with workers, suppliers, and community "
            "shows responsible business conduct. "
            "This is checked by large buyers during vendor audits."
        )
        example(
            "You meet your workers daily on the shop floor. "
            "You call your top supplier once a month. "
            "You attend village meetings once a year."
        )

        selected = p.get("stakeholders_selected", [])
        preset_labels = {
            "workers": "👷 Workers",
            "customers": "🛒 Customers",
            "suppliers": "🏭 Suppliers",
            "community": "🏘️ Local Community",
            "banks": "🏦 Banks",
            "govt": "🏛️ Government",
        }

        freq_options = ["Daily", "Weekly", "Monthly",
                        "Quarterly", "Yearly", "Rarely / As needed"]
        engage_data = p.get("engage_data", {})

        for key in selected:
            label = preset_labels.get(key, key)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**{label}**")
            with col2:
                engage_data[key] = st.selectbox(
                    f"How often?",
                    freq_options,
                    index=freq_options.index(
                        engage_data.get(key, "Monthly")
                    ) if engage_data.get(key) in freq_options else 2,
                    key=f"freq_{key}"
                )

        p["engage_data"] = engage_data
        p["engage_freq"] = True

        good("Engagement frequency recorded — this goes directly into your BRSR report.")

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q3: ANY ISSUES RAISED ─────────────────────────────────────────────
    elif step == 3:
        st.markdown("### 🗣️ Did anyone raise any concerns or issues with your business this year?")
        why(
            "Knowing and addressing concerns shows you're a responsive business. "
            "Even if you resolve issues informally, documenting them helps your score."
        )
        example(
            "A supplier complained about delayed payments. "
            "Workers raised a concern about the canteen. "
            "A neighbour complained about noise from the factory."
        )

        p["issues_raised"] = st.radio(
            "Did any stakeholder raise a concern or issue this year?",
            ["No — no issues raised",
             "Yes — some concerns were raised and resolved",
             "Yes — some concerns are still being addressed"],
            index=["No — no issues raised",
                   "Yes — some concerns were raised and resolved",
                   "Yes — some concerns are still being addressed"].index(
                p.get("issues_raised", "No — no issues raised")
            )
        )

        if p["issues_raised"] != "No — no issues raised":
            p["issues_desc"] = st.text_area(
                "Briefly describe the concern and what you did about it",
                value=p.get("issues_desc", ""),
                height=80,
                placeholder="e.g. Two workers raised concern about overtime payment. "
                            "We reviewed and corrected the payroll within 30 days."
            )
            good("Documenting concerns and resolutions shows strong stakeholder management.")

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q4: MINIMUM WAGES ─────────────────────────────────────────────────
    elif step == 4:
        st.markdown("### 💰 Do you pay your workers at least the government minimum wage?")
        why(
            "Minimum wage compliance is a basic human rights requirement. "
            "Banks check this during loan processing. "
            "Failure to comply can result in labour department penalties."
        )
        example(
            "In Gujarat, the minimum wage for unskilled workers is approximately "
            "₹350-400 per day. If you pay ₹400 or above to all workers, "
            "the answer is Yes."
        )

        st.markdown(
            "💡 Check your state's current minimum wage at "
            "**labourcommissioner.gujarat.gov.in** or ask your CA."
        )

        p["min_wage"] = st.radio(
            "Do ALL your workers receive at least the state minimum wage?",
            ["Yes — all workers are paid minimum wage or above",
             "No — some workers are below minimum wage",
             "Not Sure — need to check"],
            index=["Yes — all workers are paid minimum wage or above",
                   "No — some workers are below minimum wage",
                   "Not Sure — need to check"].index(
                p.get("min_wage",
                      "Yes — all workers are paid minimum wage or above")
            )
        )

        if p["min_wage"].startswith("Yes"):
            good(
                "Minimum wage compliance confirmed — major positive for "
                "bank loans and large buyer vendor checks."
            )
        elif p["min_wage"].startswith("No"):
            bad(
                "Some workers below minimum wage — this is a legal violation. "
                "Review your payroll with your CA immediately."
            )
        else:
            warn(
                "Check your state government website or ask your CA for "
                "current minimum wage rates."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q5: FOCAL POINT FOR HUMAN RIGHTS ─────────────────────────────────
    elif step == 5:
        st.markdown("### 🎯 Is there one person in your business who handles worker complaints?")
        why(
            "Having a designated person for complaints shows workers have "
            "someone to go to. This is a basic human rights requirement. "
            "It can be the owner, HR person, or a senior supervisor."
        )
        example(
            "The owner handles all worker complaints directly. "
            "Or: The factory manager is the designated HR person for complaints. "
            "Either counts."
        )

        p["focal_point"] = st.radio(
            "Is there a specific person responsible for handling human rights "
            "issues and worker complaints?",
            ["Yes", "No"],
            horizontal=True,
            index=0 if p.get("focal_point", "No") == "Yes" else 1
        )

        if p["focal_point"] == "Yes":
            p["focal_person"] = st.text_input(
                "What is their name and designation?",
                value=p.get("focal_person", ""),
                placeholder="e.g. Ramesh Shah — Factory Manager / "
                            "The Owner handles all HR matters"
            )
            good("Focal point in place — this shows structured HR management.")
        else:
            warn(
                "Designate someone — even the owner — as the person "
                "responsible for worker complaints. Takes 1 minute."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q6: HUMAN RIGHTS TRAINING ─────────────────────────────────────────
    elif step == 6:
        st.markdown("### 📚 Did you hold any training on basic worker rights this year?")
        why(
            "Training workers on their rights and company policies reduces "
            "harassment and disputes. Large buyers require minimum 50% coverage."
        )
        example(
            "A 30-minute session explaining: no harassment, fair wages, "
            "right to raise complaints = valid training. "
            "Even a WhatsApp message to all workers about their rights counts."
        )

        total = p.get("total_workforce", 0)
        if total == 0:
            total = st.number_input(
                "How many people work at your business?",
                min_value=0, value=0
            )
            p["total_workforce"] = total

        hr_trained = st.number_input(
            "How many people attended training on worker rights, "
            "anti-harassment, or code of conduct this year?",
            min_value=0,
            max_value=max(total, 1),
            value=p.get("hr_trained", 0),
            help="Enter 0 if no training was conducted."
        )
        p["hr_trained"] = hr_trained

        if total > 0:
            tr_pct = safe_pct(hr_trained, total)
            calc(f"{hr_trained} out of {total} = {tr_pct}% training coverage")

            if tr_pct >= 80:
                good(
                    f"{tr_pct}% coverage — excellent. "
                    "This is a top positive for ESG ratings."
                )
            elif tr_pct >= 50:
                good(f"{tr_pct}% coverage — decent. Aim for 100%.")
            elif hr_trained > 0:
                warn(
                    f"Only {tr_pct}% trained. Schedule one all-staff "
                    "session to improve this significantly."
                )
            else:
                warn(
                    "No training recorded. Even a brief WhatsApp message "
                    "to all workers about their rights counts."
                )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q7: COMPLAINTS ────────────────────────────────────────────────────
    elif step == 7:
        st.markdown("### 📋 Any serious complaints from workers this year?")
        why(
            "Honest disclosure of complaints — and how you resolved them — "
            "builds more trust than claiming zero issues. "
            "Banks and auditors respect transparency."
        )
        example(
            "1 sexual harassment complaint received and resolved. "
            "0 child labour complaints. 2 wage dispute complaints — both settled."
        )

        st.markdown("Enter the number of complaints in each category. **Put 0 if none.**")

        complaint_types = [
            ("sexual_harassment",  "Sexual Harassment complaints"),
            ("discrimination",     "Discrimination complaints (caste, religion, gender)"),
            ("child_labour",       "Child Labour complaints"),
            ("forced_labour",      "Forced / Involuntary Labour complaints"),
            ("wage_disputes",      "Wage / Salary dispute complaints"),
            ("other_hr",           "Other human rights complaints"),
        ]

        total_complaints = 0
        for ckey, clabel in complaint_types:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.caption(clabel)
            with col2:
                val = st.number_input(
                    clabel,
                    min_value=0,
                    value=p.get(f"complaint_{ckey}", 0),
                    key=f"comp_{ckey}",
                    label_visibility="collapsed"
                )
                p[f"complaint_{ckey}"] = val
                total_complaints += val

        if total_complaints == 0:
            good("Zero complaints — clean record on worker rights.")
        else:
            warn(
                f"{total_complaints} complaint(s) filed. "
                "Document how each was resolved in Full Mode."
            )
            p["complaints_desc"] = st.text_area(
                "Briefly describe how complaints were handled",
                value=p.get("complaints_desc", ""),
                height=60,
                placeholder="e.g. 1 wage dispute raised in June. "
                            "Reviewed payroll records and corrected payment "
                            "within 15 days. Employee confirmed resolution."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q8: HR IN CONTRACTS ───────────────────────────────────────────────
    elif step == 8:
        st.markdown("### 📄 Do your supplier agreements mention worker rights?")
        why(
            "Having human rights clauses in supplier contracts protects "
            "you legally and shows buyers you have a responsible supply chain. "
            "This is increasingly checked by large corporates."
        )
        example(
            "A clause in your supplier agreement saying: "
            "'Supplier must not employ workers below the legal working age "
            "and must comply with all applicable labour laws.' — this counts."
        )

        p["hr_in_contracts"] = st.radio(
            "Do your business agreements or supplier contracts include "
            "any human rights or labour rights clauses?",
            ["Yes", "No", "We don't have formal written contracts"],
            index=["Yes", "No",
                   "We don't have formal written contracts"].index(
                p.get("hr_in_contracts", "No")
            )
        )

        if p["hr_in_contracts"] == "Yes":
            good(
                "Human rights in contracts — strong supply chain governance. "
                "This is a differentiator for large buyer vendor onboarding."
            )
        elif p["hr_in_contracts"] == "No":
            warn(
                "Add a simple clause to your supplier agreements. "
                "Even one sentence about no child labour counts."
            )
        else:
            warn(
                "Consider creating a simple written agreement even for "
                "regular suppliers. Your CA can draft a 1-page template."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q9: ASSESSMENTS ───────────────────────────────────────────────────
    elif step == 9:
        st.markdown("### 🔍 Has anyone checked your workplace for labour law compliance?")
        why(
            "Assessments show you are proactive about compliance. "
            "Even a self-check counts. Government inspections also qualify."
        )
        example(
            "A labour department inspector visited your factory = 100% assessed. "
            "You did a self-audit of your wage register = self-assessment. "
            "A buyer audited your factory as part of vendor check = third-party assessment."
        )

        assessment_types = [
            ("child_labour_assess",    "Child Labour check"),
            ("forced_labour_assess",   "Forced Labour check"),
            ("sexual_harass_assess",   "Sexual Harassment check"),
            ("discrimination_assess",  "Discrimination check"),
            ("wages_assess",           "Wages compliance check"),
        ]

        st.markdown("For each type, what % of your plants/offices were assessed?")

        for akey, alabel in assessment_types:
            p[akey] = st.slider(
                alabel,
                0, 100,
                p.get(akey, 0),
                key=f"assess_{akey}",
                help="0% = not checked at all. 100% = all locations checked."
            )

        any_assessed = any(p.get(akey, 0) > 0 for akey, _ in assessment_types)
        if any_assessed:
            good(
                "At least some assessments done. "
                "Even self-assessments are valuable for your BRSR report."
            )
        else:
            warn(
                "No assessments done yet. Conduct a simple self-check "
                "using your payroll register and attendance records."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q10: CORRECTIVE ACTIONS ───────────────────────────────────────────
    elif step == 10:
        st.markdown("### 🔧 Did you fix anything based on the above checks?")
        why(
            "Corrective actions show maturity. A business that finds an issue "
            "and fixes it is viewed more positively than one that claims perfection."
        )
        example(
            "After self-check found 2 workers paid below minimum wage — "
            "corrected payroll and back-paid the difference. "
            "Or: After buyer audit, installed a POSH complaint box."
        )

        p["corrective_actions"] = st.text_area(
            "Describe any corrective actions taken or planned "
            "(leave blank if nothing needed)",
            value=p.get("corrective_actions", ""),
            height=100,
            placeholder="e.g. After reviewing wage records in Q2, we found "
                        "3 contract workers were below minimum wage. "
                        "Corrected immediately and back-paid the difference. "
                        "Now reviewing payroll monthly."
        )

        if p.get("corrective_actions", "").strip():
            good(
                "Corrective actions documented — this shows strong "
                "self-governance and will be highlighted positively in your report."
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

    # ── QUICK SUMMARY ─────────────────────────────────────────────────────
    elif step > 10:

        st.balloons()

        st.markdown(
            '<div class="section-win">'
            '<div style="font-size:48px">🎉</div>'
            '<div style="font-size:22px; font-weight:700; color:#1b5e20;">'
            'P4 & P5 Quick Mode Complete!</div>'
            '<div style="font-size:14px; color:#2e7d32; margin-top:8px;">'
            'Stakeholder engagement and human rights disclosures done.'
            '</div></div>',
            unsafe_allow_html=True
        )

        bank_score = calc_bank_score()
        colour = ("green" if bank_score >= 70
                  else "orange" if bank_score >= 40 else "red")
        st.markdown(
            f"<h2 style='color:{colour}; text-align:center'>"
            f"{bank_score}/100</h2>"
            "<p style='text-align:center;color:gray'>Bank-Ready Score (P4+P5)</p>",
            unsafe_allow_html=True
        )
        st.progress(bank_score / 100)

        st.markdown("---")
        st.markdown("### Your Summary")

        total = p.get("total_workforce", 0)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Stakeholder Groups",
                  len(p.get("stakeholders_selected", [])))
        m2.metric("Min Wage Status",
                  "✅" if p.get("min_wage", "").startswith("Yes") else "❌")
        m3.metric("HR Training",
                  f"{safe_pct(p.get('hr_trained', 0), max(total, 1))}%")
        m4.metric("Total Complaints",
                  sum(p.get(f"complaint_{k}", 0) for k in [
                      "sexual_harassment", "discrimination",
                      "child_labour", "forced_labour",
                      "wage_disputes", "other_hr"
                  ]))

        st.markdown("---")
        st.markdown("### What To Do Next")
        recs = 0

        if not p.get("min_wage", "").startswith("Yes"):
            bad("Review wage payments — minimum wage compliance is critical.")
            recs += 1
        if p.get("focal_point") != "Yes":
            warn("Designate someone for HR complaints — takes 1 minute.")
            recs += 1
        if safe_pct(p.get("hr_trained", 0), max(total, 1)) < 50:
            warn("Schedule one all-staff training on worker rights.")
            recs += 1
        if p.get("hr_in_contracts") == "No":
            warn("Add a simple labour rights clause to supplier agreements.")
            recs += 1
        if recs == 0:
            good("No major gaps! Strong P4 & P5 compliance.")

        st.markdown("---")
        op1, op2 = st.columns(2)
        with op1:
            if st.button("📋 Switch to Full Mode",
                         use_container_width=True):
                st.session_state.p45_mode = "full"
                st.rerun()
        with op2:
            if st.button("💾 Save & Move to P6 →",
                         use_container_width=True, type="primary"):
                st.session_state.c_p45 = p
                st.success(
                    "✅ P4 & P5 saved! Next: Principle 6 — Environment."
                )

# ═════════════════════════════════════════════════════════════════════════════
# ████████████████████  FULL MODE  ████████████████████████████████████████████
# ═════════════════════════════════════════════════════════════════════════════
else:

    full_step = st.session_state.p45_full_step

    full_steps = {
        1: "👥 P4: Stakeholders",
        2: "🤝 P4: Engagement",
        3: "💰 P5: Wages",
        4: "📚 P5: Training",
        5: "📋 P5: Complaints",
        6: "🔍 P5: Assessments",
        7: "🏆 Leadership",
        8: "✅ Summary"
    }

    nav = st.columns(8)
    for i, (num, label) in enumerate(full_steps.items()):
        with nav[i]:
            t = "primary" if full_step == num else "secondary"
            if st.button(label, key=f"fn_{num}",
                         type=t, use_container_width=True):
                st.session_state.p45_full_step = num
                st.rerun()

    st.progress(full_step / len(full_steps))
    st.markdown("---")

    # ── FULL STEP 1: STAKEHOLDER IDENTIFICATION (P4 E1) ───────────────────
    if full_step == 1:
        st.header("👥 P4 Essential Q1 — Identifying Your Stakeholders")
        badge_e()

        with st.container(border=True):
            st.markdown("#### How do you identify who matters to your business?")
            example(
                "We look at who depends on us (workers, community), "
                "who we depend on (suppliers, banks), and who we serve (customers)."
            )

            p["identification_process"] = st.text_area(
                "Describe your process for identifying key stakeholders",
                value=p.get("identification_process", ""),
                height=100,
                placeholder="e.g. We identify stakeholders by mapping who directly "
                            "benefits from or is affected by our business operations. "
                            "This includes our permanent workers, contract staff, "
                            "raw material suppliers, end customers, the local community "
                            "around our factory, and the banks that provide our credit.",
                key="f_id_proc"
            )

            st.markdown("#### Now list your key stakeholder groups:")
            st.caption(
                "For each group tell us: Are they vulnerable? "
                "How do you communicate? How often? What do you discuss?"
            )

            presets = [
                ("workers",   "Workers / Employees",   False),
                ("customers", "Customers / Buyers",     False),
                ("suppliers", "Suppliers / Vendors",    False),
                ("community", "Local Community",        True),
                ("banks",     "Banks / Lenders",        False),
                ("govt",      "Government / Regulators",False),
            ]

            stakeholder_rows = p.get("stakeholder_full", {})
            channel_options = ["Email", "Phone / WhatsApp", "In-Person Meeting",
                               "Notice Board", "Community Meeting",
                               "Website", "Newsletter", "Other"]
            freq_options = ["Daily", "Weekly", "Monthly",
                            "Quarterly", "Half-Yearly", "Annually"]

            for key, label, default_vuln in presets:
                with st.expander(f"📌 {label}"):
                    row = stakeholder_rows.get(key, {})
                    sc = st.columns(2)
                    with sc[0]:
                        vuln = st.radio(
                            "Is this a vulnerable/marginalized group?",
                            ["No", "Yes"],
                            horizontal=True,
                            index=1 if row.get("vuln", "Yes" if default_vuln else "No") == "Yes" else 0,
                            key=f"f_vuln_{key}"
                        )
                        freq = st.selectbox(
                            "How often do you engage?",
                            freq_options,
                            index=freq_options.index(row.get("freq", "Monthly"))
                            if row.get("freq") in freq_options else 2,
                            key=f"f_freq_{key}"
                        )
                    with sc[1]:
                        channels = st.multiselect(
                            "How do you communicate?",
                            channel_options,
                            default=row.get("channels", ["Phone / WhatsApp"]),
                            key=f"f_chan_{key}"
                        )
                        purpose = st.text_area(
                            "Purpose and key topics discussed",
                            value=row.get("purpose", ""),
                            height=80,
                            placeholder="e.g. Discuss wages, working conditions, "
                                        "production targets, safety updates",
                            key=f"f_purp_{key}"
                        )
                    stakeholder_rows[key] = {
                        "label": label,
                        "vuln": vuln,
                        "freq": freq,
                        "channels": channels,
                        "purpose": purpose
                    }

            p["stakeholder_full"] = stakeholder_rows

        _, c_next = st.columns([1, 1])
        with c_next:
            if st.button("Next: Engagement Details →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 2: STAKEHOLDER ENGAGEMENT SUMMARY (P4 E2) ───────────────
    elif full_step == 2:
        st.header("🤝 P4 Essential Q2 — Stakeholder Engagement Summary")
        badge_e()

        with st.container(border=True):
            st.markdown("#### Stakeholder Engagement Table")

            rows = p.get("stakeholder_full", {})
            if rows:
                table_data = []
                for key, row in rows.items():
                    if row.get("purpose") or row.get("freq"):
                        table_data.append({
                            "Stakeholder Group": row.get("label", key),
                            "Vulnerable?": row.get("vuln", "No"),
                            "Channels": ", ".join(row.get("channels", [])),
                            "Frequency": row.get("freq", "—"),
                            "Purpose & Topics": row.get("purpose", "—")
                        })
                if table_data:
                    st.dataframe(pd.DataFrame(table_data),
                                 use_container_width=True)
                    good("Stakeholder table complete — this goes directly into your BRSR report.")
            else:
                warn("Go back to Step 1 and fill stakeholder details.")

        with st.container(border=True):
            badge_l()
            st.markdown("#### P4 Leadership — Board Consultation Process")
            example(
                "Most MSMEs: 'The owner reviews stakeholder feedback "
                "monthly and incorporates it into business decisions.'"
            )
            p["board_consultation"] = st.text_area(
                "How is stakeholder feedback shared with the owner/board?",
                value=p.get("board_consultation", ""),
                height=80,
                placeholder="e.g. Worker concerns are raised to the owner "
                            "in a monthly review meeting. Supplier issues "
                            "are addressed in quarterly supply chain reviews.",
                key="f_board_cons"
            )

            p["vc_consulted_for_esg"] = st.radio(
                "Do you use stakeholder feedback to improve your "
                "environmental and social practices?",
                ["Yes", "No"],
                horizontal=True,
                index=0 if p.get("vc_consulted_for_esg", "No") == "Yes" else 1,
                key="f_vc_esg"
            )
            if p["vc_consulted_for_esg"] == "Yes":
                p["vc_esg_example"] = st.text_area(
                    "Give one example of how feedback was used",
                    value=p.get("vc_esg_example", ""),
                    height=60,
                    placeholder="e.g. Workers raised concern about canteen hygiene. "
                                "We improved canteen facilities and added a wash station.",
                    key="f_vc_esg_ex"
                )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Wages →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 3: WAGES (P5 E2-E3) ─────────────────────────────────────
    elif full_step == 3:
        st.header("💰 P5 Essential Q2-Q3 — Wages & Minimum Wage Compliance")
        badge_e()

        with st.container(border=True):
            st.markdown("#### Minimum Wage Compliance")
            example(
                "Enter the number of workers paid EXACTLY minimum wage "
                "and those paid MORE than minimum wage. "
                "All should add up to your total."
            )

            categories = [
                ("perm_emp_m",  "Permanent Employees — Male"),
                ("perm_emp_f",  "Permanent Employees — Female"),
                ("contract_emp_m", "Contract Employees — Male"),
                ("contract_emp_f", "Contract Employees — Female"),
                ("perm_wkr_m",  "Permanent Workers — Male"),
                ("perm_wkr_f",  "Permanent Workers — Female"),
                ("contract_wkr_m", "Contract Workers — Male"),
                ("contract_wkr_f", "Contract Workers — Female"),
            ]

            wage_data = p.get("wage_data", {})

            wh = st.columns(4)
            wh[0].markdown("**Category**")
            wh[1].markdown("**Total**")
            wh[2].markdown("**= Min Wage**")
            wh[3].markdown("**> Min Wage**")

            for wkey, wlabel in categories:
                wr = st.columns(4)
                wr[0].markdown(f"*{wlabel}*")
                wd = wage_data.get(wkey, {})

                total_w = wr[1].number_input(
                    "Total", min_value=0,
                    value=wd.get("total", 0),
                    key=f"f_wt_{wkey}", label_visibility="collapsed"
                )
                equal_w = wr[2].number_input(
                    "Equal", min_value=0,
                    value=wd.get("equal", 0),
                    key=f"f_we_{wkey}", label_visibility="collapsed"
                )
                more_w = wr[3].number_input(
                    "More", min_value=0,
                    value=wd.get("more", 0),
                    key=f"f_wm_{wkey}", label_visibility="collapsed"
                )

                if total_w > 0 and (equal_w + more_w) != total_w:
                    st.caption(
                        f"⚠️ {wlabel}: Equal + More = "
                        f"{equal_w + more_w} but Total = {total_w}"
                    )

                wage_data[wkey] = {
                    "total": total_w, "equal": equal_w, "more": more_w
                }

            p["wage_data"] = wage_data

        with st.container(border=True):
            st.markdown("#### Median Salaries (Q3)")
            example(
                "Sort all salaries from lowest to highest. "
                "The middle one is the median. "
                "Example: 5 workers paid ₹8k, ₹10k, ₹12k, ₹15k, ₹20k. "
                "Median = ₹12k."
            )

            mc = st.columns(2)
            p["median_male"] = mc[0].number_input(
                "Median salary — Male employees/workers (₹/month)",
                min_value=0, value=p.get("median_male", 0), key="f_med_m"
            )
            p["median_female"] = mc[1].number_input(
                "Median salary — Female employees/workers (₹/month)",
                min_value=0, value=p.get("median_female", 0), key="f_med_f"
            )

            if p["median_male"] > 0 and p["median_female"] > 0:
                diff = safe_pct(
                    p["median_male"] - p["median_female"],
                    p["median_male"]
                )
                if diff > 20:
                    warn(
                        f"Gender pay gap: Men earn {diff}% more than women on median. "
                        "Large buyers check this."
                    )
                elif diff > 0:
                    good(f"Moderate gender pay gap of {diff}%.")
                else:
                    good("No gender pay gap — excellent.")

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Training →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 4: TRAINING & FOCAL POINT (P5 E1, E4, E5) ──────────────
    elif full_step == 4:
        st.header("📚 P5 Essential Q1, Q4, Q5 — Training & Grievance Setup")
        badge_e()

        with st.container(border=True):
            st.markdown("#### Human Rights Training (Q1)")
            example(
                "Any session on: worker rights, anti-harassment, "
                "code of conduct, sexual harassment awareness = valid training."
            )

            tr_cats = [
                ("perm_emp",     "Permanent Employees"),
                ("contract_emp", "Contract Employees"),
                ("perm_wkr",     "Permanent Workers"),
                ("contract_wkr", "Contract Workers"),
            ]

            tr_data = p.get("hr_training_data", {})

            th = st.columns(5)
            th[0].markdown("**Category**")
            th[1].markdown("**Total (Current)**")
            th[2].markdown("**Trained (Current)**")
            th[3].markdown("**Total (Previous)**")
            th[4].markdown("**Trained (Previous)**")

            for tkey, tlabel in tr_cats:
                tr = st.columns(5)
                tr[0].markdown(f"*{tlabel}*")
                td = tr_data.get(tkey, {})

                total_cur = tr[1].number_input(
                    "Total cur", min_value=0,
                    value=td.get("total_cur", 0),
                    key=f"f_trt_{tkey}_c", label_visibility="collapsed"
                )
                trained_cur = tr[2].number_input(
                    "Trained cur", min_value=0,
                    value=td.get("trained_cur", 0),
                    key=f"f_trtr_{tkey}_c", label_visibility="collapsed"
                )
                total_prev = tr[3].number_input(
                    "Total prev", min_value=0,
                    value=td.get("total_prev", 0),
                    key=f"f_trt_{tkey}_p", label_visibility="collapsed"
                )
                trained_prev = tr[4].number_input(
                    "Trained prev", min_value=0,
                    value=td.get("trained_prev", 0),
                    key=f"f_trtr_{tkey}_p", label_visibility="collapsed"
                )

                pct_cur = safe_pct(trained_cur, total_cur)
                if total_cur > 0:
                    st.caption(
                        f"  {tlabel}: {trained_cur}/{total_cur} = {pct_cur}% trained"
                    )

                tr_data[tkey] = {
                    "total_cur": total_cur, "trained_cur": trained_cur,
                    "total_prev": total_prev, "trained_prev": trained_prev
                }

            p["hr_training_data"] = tr_data

        with st.container(border=True):
            st.markdown("#### Focal Point for Human Rights (Q4)")
            c1, c2 = st.columns(2)
            with c1:
                p["focal_point"] = st.radio(
                    "Is there a designated person for human rights issues?",
                    ["Yes", "No"],
                    horizontal=True,
                    index=0 if p.get("focal_point", "No") == "Yes" else 1,
                    key="f_focal"
                )
            with c2:
                if p["focal_point"] == "Yes":
                    p["focal_person"] = st.text_input(
                        "Name and designation",
                        value=p.get("focal_person", ""),
                        placeholder="e.g. Ramesh Shah, Factory Manager",
                        key="f_focal_name"
                    )

        with st.container(border=True):
            st.markdown("#### Internal Grievance Mechanism (Q5)")
            p["grievance_mechanism"] = st.text_area(
                "Describe your internal mechanism for human rights grievances",
                value=p.get("grievance_mechanism", ""),
                height=80,
                placeholder="e.g. Workers can raise complaints verbally to their "
                            "supervisor or directly to the factory manager. "
                            "All complaints are recorded in a register and "
                            "resolved within 30 days.",
                key="f_griev_mech"
            )

            p["retaliation_prevention"] = st.text_area(
                "How do you ensure complainants are not punished for raising issues? (Q7)",
                value=p.get("retaliation_prevention", ""),
                height=60,
                placeholder="e.g. We maintain confidentiality of complaints and "
                            "have a zero-retaliation policy. Any supervisor found "
                            "retaliating against a complainant faces disciplinary action.",
                key="f_ret_prev"
            )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Complaints →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 5: COMPLAINTS & CONTRACTS (P5 E6, E8) ───────────────────
    elif full_step == 5:
        st.header("📋 P5 Essential Q6, Q8 — Complaints & Contracts")
        badge_e()

        with st.container(border=True):
            st.markdown("#### Complaints Filed This Year (Q6)")
            example("Put 0 in every category if no complaints were filed.")

            complaint_types = [
                ("sexual_harassment", "Sexual Harassment"),
                ("discrimination",    "Discrimination at Workplace"),
                ("child_labour",      "Child Labour"),
                ("forced_labour",     "Forced / Involuntary Labour"),
                ("wages",             "Wage Disputes"),
                ("other_hr",          "Other Human Rights Issues"),
            ]

            ch = st.columns(5)
            ch[0].markdown("**Type**")
            ch[1].markdown("**Filed (Current)**")
            ch[2].markdown("**Pending (Current)**")
            ch[3].markdown("**Filed (Previous)**")
            ch[4].markdown("**Pending (Previous)**")

            comp_data = p.get("complaint_data", {})

            for ckey, clabel in complaint_types:
                cr = st.columns(5)
                cr[0].markdown(f"*{clabel}*")
                cd = comp_data.get(ckey, {})

                filed_cur = cr[1].number_input(
                    "Filed cur", min_value=0,
                    value=cd.get("filed_cur", 0),
                    key=f"f_cf_{ckey}", label_visibility="collapsed"
                )
                pending_cur = cr[2].number_input(
                    "Pending cur", min_value=0,
                    value=cd.get("pending_cur", 0),
                    key=f"f_cp_{ckey}", label_visibility="collapsed"
                )
                filed_prev = cr[3].number_input(
                    "Filed prev", min_value=0,
                    value=cd.get("filed_prev", 0),
                    key=f"f_cfp_{ckey}", label_visibility="collapsed"
                )
                pending_prev = cr[4].number_input(
                    "Pending prev", min_value=0,
                    value=cd.get("pending_prev", 0),
                    key=f"f_cpp_{ckey}", label_visibility="collapsed"
                )

                comp_data[ckey] = {
                    "filed_cur": filed_cur,
                    "pending_cur": pending_cur,
                    "filed_prev": filed_prev,
                    "pending_prev": pending_prev
                }

            p["complaint_data"] = comp_data

            total_complaints = sum(
                comp_data.get(k, {}).get("filed_cur", 0)
                for k, _ in complaint_types
            )
            if total_complaints == 0:
                good("Zero complaints this year — clean record.")

        with st.container(border=True):
            st.markdown("#### Human Rights in Business Agreements (Q8)")
            p["hr_in_contracts"] = st.radio(
                "Do your supplier/business agreements include human rights clauses?",
                ["Yes", "No"],
                horizontal=True,
                index=0 if p.get("hr_in_contracts", "No") == "Yes" else 1,
                key="f_hric"
            )
            if p["hr_in_contracts"] == "No":
                warn(
                    "Add a simple clause: 'Supplier must comply with all "
                    "applicable labour laws and must not employ child labour.'"
                )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Assessments →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 6: ASSESSMENTS & CORRECTIVE (P5 E9-E10) ────────────────
    elif full_step == 6:
        st.header("🔍 P5 Essential Q9-Q10 — Assessments & Corrective Actions")
        badge_e()

        with st.container(border=True):
            st.markdown("#### % of Plants/Offices Assessed (Q9)")
            example(
                "A labour department inspection = 100% assessed for wages. "
                "Your own self-check = also counts."
            )

            assessment_types = [
                ("child_labour",   "Child Labour"),
                ("forced_labour",  "Forced/Involuntary Labour"),
                ("sexual_harass",  "Sexual Harassment"),
                ("discrimination", "Discrimination at Workplace"),
                ("wages",          "Wages Compliance"),
            ]

            assess_data = p.get("assess_data", {})

            for akey, alabel in assessment_types:
                ac = st.columns([3, 1])
                with ac[0]:
                    val = st.slider(
                        f"{alabel} — % of locations assessed",
                        0, 100,
                        assess_data.get(akey, 0),
                        key=f"f_assess_{akey}"
                    )
                with ac[1]:
                    st.markdown(f"**{val}%**")
                assess_data[akey] = val

            p["assess_data"] = assess_data

        with st.container(border=True):
            st.markdown("#### Corrective Actions (Q10)")
            p["p5_corrective"] = st.text_area(
                "Corrective actions taken or underway based on assessments",
                value=p.get("p5_corrective", ""),
                height=80,
                placeholder="e.g. Assessment found 2 contract workers below "
                            "minimum wage. Corrected immediately. "
                            "Now reviewing all contractor wage slips monthly.",
                key="f_p5_corr"
            )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Leadership →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 7: LEADERSHIP (P4 L1-L3, P5 L1-L5) ─────────────────────
    elif full_step == 7:
        st.header("🏆 Leadership Indicators — P4 & P5")
        badge_l()

        st.info(
            "These are voluntary. Filling them shows advanced ESG maturity "
            "and helps you score higher with large corporate buyers."
        )

        lt = st.tabs([
            "P4 L1-L3: Stakeholder",
            "P5 L1: Process Changes",
            "P5 L2: HR Due Diligence",
            "P5 L3: Accessibility",
            "P5 L4-L5: VC Assessment"
        ])

        with lt[0]:
            badge_l()
            st.markdown("### P4 Leadership — Stakeholder Consultation at Board Level")

            p["p4_l1_desc"] = st.text_area(
                "How do you consult stakeholders on economic, environmental, "
                "and social topics? How is this feedback given to the owner/board?",
                value=p.get("p4_l1_desc", ""),
                height=80,
                placeholder="e.g. We hold quarterly supplier meetings where "
                            "environmental concerns are discussed. Outcomes are "
                            "reviewed by the MD monthly.",
                key="f_p4l1"
            )

            p["p4_l2_used"] = st.radio(
                "Is stakeholder consultation used to identify and manage "
                "ESG risks and opportunities?",
                ["Yes", "No"],
                horizontal=True,
                index=0 if p.get("p4_l2_used", "No") == "Yes" else 1,
                key="f_p4l2"
            )

            if p["p4_l2_used"] == "Yes":
                p["p4_l2_example"] = st.text_area(
                    "Give one example",
                    value=p.get("p4_l2_example", ""),
                    height=60, key="f_p4l2_ex"
                )

            p["p4_l3_vulnerable"] = st.text_area(
                "Any actions taken to address concerns of vulnerable groups "
                "(women workers, migrant workers, differently abled)?",
                value=p.get("p4_l3_vulnerable", ""),
                height=60,
                placeholder="e.g. Female workers given separate rest room and "
                            "transport facilities for night shift.",
                key="f_p4l3"
            )

        with lt[1]:
            badge_l()
            st.markdown("### P5 L1 — Business Process Changes from HR Grievances")
            p["p5_l1_changes"] = st.text_area(
                "Have you changed any business process based on a human rights "
                "grievance or complaint?",
                value=p.get("p5_l1_changes", ""),
                height=80,
                placeholder="e.g. After a sexual harassment complaint in FY23, "
                            "we introduced a POSH committee and conduct annual "
                            "anti-harassment training for all staff.",
                key="f_p5l1"
            )

        with lt[2]:
            badge_l()
            st.markdown("### P5 L2 — Human Rights Due Diligence")
            p["p5_l2_scope"] = st.text_area(
                "Describe the scope and coverage of any human rights "
                "due diligence conducted (who reviewed, what was covered)",
                value=p.get("p5_l2_scope", ""),
                height=80,
                placeholder="e.g. We conducted an internal HR due diligence "
                            "covering all permanent and contract workers across "
                            "our 2 factory units in Bhavnagar.",
                key="f_p5l2"
            )

        with lt[3]:
            badge_l()
            st.markdown("### P5 L3 — Accessibility for Differently Abled Visitors")
            p["p5_l3_accessible"] = st.radio(
                "Are your premises accessible to differently abled visitors "
                "as per the Rights of Persons with Disabilities Act 2016?",
                ["Yes", "No", "Work in Progress"],
                index=["Yes", "No", "Work in Progress"].index(
                    p.get("p5_l3_accessible", "No")
                ),
                key="f_p5l3"
            )
            if p["p5_l3_accessible"] == "No":
                p["p5_l3_steps"] = st.text_area(
                    "What steps are you taking?",
                    value=p.get("p5_l3_steps", ""),
                    height=60,
                    placeholder="e.g. Planning to install ramp at main entrance by Dec 2025.",
                    key="f_p5l3_steps"
                )

        with lt[4]:
            badge_l()
            st.markdown("### P5 L4-L5 — Value Chain Partner Assessments")

            vc_assess_types = [
                ("sexual_harass",  "Sexual Harassment"),
                ("discrimination", "Discrimination"),
                ("child_labour",   "Child Labour"),
                ("forced_labour",  "Forced Labour"),
                ("wages",          "Wages"),
            ]

            vc_assess_data = p.get("vc_assess_data", {})
            st.markdown("**% of suppliers assessed for each issue:**")

            for vakey, valabel in vc_assess_types:
                vc_assess_data[vakey] = st.slider(
                    valabel,
                    0, 100,
                    vc_assess_data.get(vakey, 0),
                    key=f"f_vca_{vakey}"
                )

            p["vc_assess_data"] = vc_assess_data

            p["vc_corrective"] = st.text_area(
                "Corrective actions from supplier assessments (L5)",
                value=p.get("vc_corrective", ""),
                height=60,
                key="f_vc_corr"
            )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Summary →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 8: SUMMARY ──────────────────────────────────────────────
    elif full_step == 8:
        st.header("✅ P4 & P5 — Full Mode Summary")

        bank_score = calc_bank_score()
        colour = ("green" if bank_score >= 70
                  else "orange" if bank_score >= 40 else "red")
        st.markdown(
            f"<h2 style='color:{colour}; text-align:center'>"
            f"{bank_score}/100</h2>"
            "<p style='text-align:center;color:gray'>Bank-Ready Score (P4+P5)</p>",
            unsafe_allow_html=True
        )
        st.progress(bank_score / 100)

        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Stakeholder Groups",
                  len(p.get("stakeholder_full", {})))
        m2.metric("Min Wage",
                  "✅" if p.get("min_wage", "").startswith("Yes") else "—")
        m3.metric("HR Contracts",
                  "✅" if p.get("hr_in_contracts") == "Yes" else "❌")
        m4.metric("Focal Point",
                  "✅" if p.get("focal_point") == "Yes" else "❌")

        st.markdown("---")
        recs = 0
        if not p.get("min_wage", "").startswith("Yes"):
            bad("Minimum wage compliance needed.")
            recs += 1
        if p.get("focal_point") != "Yes":
            warn("Designate a focal point for HR complaints.")
            recs += 1
        if p.get("hr_in_contracts") == "No":
            warn("Add human rights clause to supplier contracts.")
            recs += 1
        if recs == 0:
            good("No major gaps in P4 & P5!")

        st.markdown("---")
        cf1, cf2, cf3 = st.columns([1, 2, 1])
        with cf2:
            if st.button("💾 Save P4 & P5 & Move to P6 →",
                         type="primary", use_container_width=True):
                st.session_state.c_p45 = p
                st.balloons()
                st.success(
                    "✅ P4 & P5 saved! Next: Principle 6 — Environment."
                )

        c_back2, _, _ = st.columns([1, 2, 1])
        with c_back2:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
                
# ─── BOTTOM NAVIGATION ──────────────────────────────────────────────────
from business_profile import render_section_navigation
render_section_navigation("Principle 4+5")
from business_profile import (
    init_business_profile, show_tier_badge, show_sidebar_logo,
    get_business_type, is_sole_prop, is_partnership,
    has_board, is_listed
)
init_business_profile()
show_sidebar_logo()
show_tier_badge()