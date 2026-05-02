import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BRSR P7-9 | Policy, Community & Customers",
    page_icon="🤝",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; max-width: 820px; }
    .why-box {
        background: #e8f5e9; border-left: 4px solid #43a047;
        padding: 8px 14px; border-radius: 0 8px 8px 0;
        font-size: 13px; color: #2e7d32; margin: 10px 0;
    }
    .example-box {
        background: #fff8e1; border-left: 4px solid #ffc107;
        padding: 8px 14px; border-radius: 0 8px 8px 0;
        font-size: 13px; color: #5d4037; margin: 8px 0;
    }
    .calc-box {
        background: #f0f4ff; border: 1px solid #c7d2fe;
        border-radius: 10px; padding: 12px 16px;
        font-size: 15px; font-weight: 600;
        color: #3730a3; margin: 10px 0; text-align: center;
    }
    .good-box {
        background: #e8f5e9; border: 1px solid #a5d6a7;
        border-radius: 10px; padding: 10px 14px;
        font-size: 13px; color: #1b5e20; margin: 6px 0;
    }
    .warn-box {
        background: #fff3e0; border: 1px solid #ffcc80;
        border-radius: 10px; padding: 10px 14px;
        font-size: 13px; color: #e65100; margin: 6px 0;
    }
    .bad-box {
        background: #ffebee; border: 1px solid #ef9a9a;
        border-radius: 10px; padding: 10px 14px;
        font-size: 13px; color: #c62828; margin: 6px 0;
    }
    .mode-card {
        border: 2px solid #e0e0e0; border-radius: 14px;
        padding: 20px; text-align: center; margin: 8px;
    }
    .section-win {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border: 2px solid #66bb6a; border-radius: 14px;
        padding: 20px; text-align: center; margin: 16px 0;
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
    .principle-tag {
        display: inline-block;
        background: #1565c0; color: white;
        padding: 2px 10px; border-radius: 12px;
        font-size: 11px; font-weight: 600;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE — All keys initialized (prevents future bugs)
# ─────────────────────────────────────────────────────────────────────────────
if "p789_mode" not in st.session_state:
    st.session_state.p789_mode = None
if "p789_quick_step" not in st.session_state:
    st.session_state.p789_quick_step = 1
if "p789_full_step" not in st.session_state:
    st.session_state.p789_full_step = 1
if "p789" not in st.session_state:
    st.session_state.p789 = {
        # P7 — Policy & Associations
        "is_association_member": "No",
        "associations_text": "",
        "associations_list": [],
        "policy_advocacy": "No",
        "policy_advocacy_examples": "",
        "anti_competitive": "No",
        "anti_competitive_details": "",
        # P8 — Community & Inclusive Growth
        "local_hiring_pct": 0,
        "local_sourcing_used": "No",
        "local_sourcing_pct": 0,
        "community_support": "No",
        "community_support_details": "",
        "community_grievance": "No formal way",
        "pref_vulnerable_proc": "No",
        "pref_vulnerable_details": "",
        # P9 — Customer Responsibility
        "customer_channels": [],
        "complaint_record": "No record",
        "complaints_received_yr": 0,
        "complaints_resolved_yr": 0,
        "product_info_clear": "Yes",
        "product_info_details": "",
        "stores_customer_data": "No",
        "data_privacy_rule": "No",
        "product_recalls": "No",
        "product_recalls_details": "",
        # Meta
        "score": 0,
    }

p789 = st.session_state.p789

# Auto-pull from Section A
sec_a = st.session_state.get("data", {})
total_workforce_from_a = (
    sec_a.get("total_perm_emp", 0) +
    sec_a.get("total_perm_wkr", 0)
)

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

def principle_tag(num):
    return f'<span class="principle-tag">P{num}</span>'

def next_q():
    st.session_state.p789_quick_step += 1

def prev_q():
    st.session_state.p789_quick_step -= 1

def next_f():
    st.session_state.p789_full_step += 1

def prev_f():
    st.session_state.p789_full_step -= 1

def safe_pct(n, d):
    try:
        n, d = float(n or 0), float(d or 0)
        return round((n / d) * 100, 1) if d > 0 else 0.0
    except:
        return 0.0

# ─────────────────────────────────────────────────────────────────────────────
# BANK SCORE — P7:20 / P8:40 / P9:40
# ─────────────────────────────────────────────────────────────────────────────
def calc_p789_score():
    score = 0
    # P7 (20)
    if p789.get("is_association_member") == "Yes":
        score += 10
    if p789.get("policy_advocacy") == "Yes":
        score += 5
    if p789.get("anti_competitive") == "No":
        score += 5

    # P8 (40)
    lh = p789.get("local_hiring_pct", 0)
    if lh >= 70: score += 12
    elif lh >= 40: score += 8
    elif lh > 0: score += 4

    ls = p789.get("local_sourcing_pct", 0)
    if ls >= 50: score += 10
    elif ls >= 25: score += 6
    elif ls > 0: score += 3

    if p789.get("community_support") != "No":
        score += 8
    if p789.get("community_grievance") != "No formal way":
        score += 5
    if p789.get("pref_vulnerable_proc") == "Yes":
        score += 5

    # P9 (40)
    if p789.get("customer_channels"):
        score += 10
    if p789.get("complaint_record") != "No record":
        score += 8

    resolution = safe_pct(
        p789.get("complaints_resolved_yr", 0),
        p789.get("complaints_received_yr", 0)
    )
    if p789.get("complaints_received_yr", 0) == 0:
        score += 7  # no complaints = good
    elif resolution >= 80:
        score += 7
    elif resolution >= 50:
        score += 4

    if p789.get("product_info_clear") == "Yes":
        score += 5

    if p789.get("stores_customer_data") == "Yes":
        if p789.get("data_privacy_rule") == "Yes":
            score += 5
    else:
        score += 5  # no data = no risk

    if p789.get("product_recalls") == "No":
        score += 5

    return min(score, 100)

def build_recommendations():
    recs = []
    if p789.get("is_association_member") == "No":
        recs.append(
            "Consider joining a local industry association like GIDC "
            "Association or Saurashtra Chamber of Commerce. Members get "
            "access to advocacy, training, and buyer networks."
        )
    if p789.get("complaint_record") == "No record":
        recs.append(
            "Start a simple complaint register today — a notebook or "
            "Excel sheet with Date | Customer Name | Issue | Action Taken | "
            "Date Resolved. Auditors love to see this."
        )
    if p789.get("stores_customer_data") == "Yes" and \
       p789.get("data_privacy_rule") == "No":
        recs.append(
            "Write one simple rule: 'We do not share customer data with "
            "outsiders.' Tell your staff to follow it. This satisfies basic "
            "data privacy requirements."
        )
    if p789.get("community_support") == "No":
        recs.append(
            "Even small contributions count — a ₹5,000 donation to a local "
            "school, sponsoring a Gaushala, or supporting a Navratri event "
            "can all be documented as community initiatives."
        )
    if p789.get("local_sourcing_pct", 0) < 25:
        recs.append(
            "Try to source at least 25% of your raw materials or services "
            "from local small businesses. This boosts your ESG profile "
            "and helps the local economy."
        )
    return recs[:5]

# ─────────────────────────────────────────────────────────────────────────────
# MODE SELECTION
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.p789_mode is None:

    st.markdown("## 🤝 Principles 7, 8 & 9 Combined")
    st.markdown(
        "Because P7, P8, and P9 are each smaller than other principles, "
        "we fill them together:"
    )
    st.markdown(
        "- **P7 — Policy:** Are you part of any business group? Do you speak up on policy?\n"
        "- **P8 — Community:** Do you support your local area and hire locally?\n"
        "- **P9 — Customers:** How do you handle customer complaints and data?"
    )
    st.markdown("")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="mode-card">
            <div style="font-size:40px">⚡</div>
            <div style="font-size:20px;font-weight:700;color:#2e7d32;">Quick Mode</div>
            <div style="font-size:14px;color:#555;margin-top:8px;">
                13 simple questions<br>
                All 3 principles together<br>
                Plain English only<br>
                Under 10 minutes
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Quick Mode ⚡",
                     use_container_width=True, type="primary"):
            st.session_state.p789_mode = "quick"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="mode-card">
            <div style="font-size:40px">📋</div>
            <div style="font-size:20px;font-weight:700;color:#1565c0;">Full Mode</div>
            <div style="font-size:14px;color:#555;margin-top:8px;">
                All SEBI Essential + Leadership<br>
                Complete tables for P7, P8, P9<br>
                BRSR-ready output<br>
                For consultants or serious users
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Full Mode 📋",
                     use_container_width=True):
            st.session_state.p789_mode = "full"
            st.rerun()

    st.info(
        "💡 **You already do most of this** — handling customer complaints, "
        "hiring locally, donating to community. We just capture it in the "
        "right format for the BRSR report."
    )
    st.stop()

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    mode_label = "⚡ Quick Mode" if st.session_state.p789_mode == "quick" else "📋 Full Mode"
    st.markdown(f"## 🤝 Principles 7, 8 & 9 &nbsp; `{mode_label}`")
with col_h2:
    if st.button("Switch Mode"):
        st.session_state.p789_mode = None
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# QUICK MODE — 13 questions
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.p789_mode == "quick":

    TOTAL = 13
    step = st.session_state.p789_quick_step

    st.markdown(
        f'<div style="font-size:13px;color:#666;">'
        f'Question {min(step, TOTAL)} of {TOTAL}</div>',
        unsafe_allow_html=True
    )
    st.progress(min(step, TOTAL) / TOTAL)
    st.markdown("")

    # ── Q1: ASSOCIATION MEMBERSHIP (P7) ──────────────────────────────────
    if step == 1:
        st.markdown(f'{principle_tag(7)} ', unsafe_allow_html=True)
        st.markdown("### 🏛️ Are you a member of any business association or chamber?")
        why(
            "Business associations help raise common issues (electricity, GST, "
            "pollution approvals) together. Banks and buyers like to see you "
            "are connected to formal industry networks."
        )
        example(
            "Saurashtra Chamber of Commerce, GIDC Bhavnagar Association, "
            "FOGMA (Gujarat), Textile Association, Plastic Manufacturers "
            "Association."
        )

        with st.expander("📖 What is 'Policy Advocacy' in SEBI terms?"):
            st.markdown("""
**SEBI Language:** "Businesses should influence public and regulatory policy
in a responsible and transparent manner."

**What it means for you:**
If you're part of an association (like GIDC Association), and the association
raises issues with the government (like GST rules or pollution rules) on
behalf of its members — that counts as policy advocacy.

**For most MSMEs:** You don't lobby directly. Your association does it for
you. So we only need to know if you are a member.
            """)

        options = ["No", "Yes"]
        current = p789.get("is_association_member", "No")
        if current not in options:
            current = "No"

        member = st.radio(
            "Are you a member of any business association / chamber?",
            options,
            index=options.index(current),
            horizontal=True
        )
        p789["is_association_member"] = member

        if member == "Yes":
            assoc_text = st.text_input(
                "Name the associations (comma separated)",
                value=p789.get("associations_text", ""),
                placeholder="e.g. GIDC Bhavnagar, Saurashtra Chamber of Commerce"
            )
            p789["associations_text"] = assoc_text
            p789["associations_list"] = [
                a.strip() for a in assoc_text.split(",") if a.strip()
            ]
            good("Good — this is a positive indicator for your BRSR report.")
        else:
            p789["associations_list"] = []
            warn(
                "Not mandatory. But joining a local association costs little "
                "and gives you access to training, advocacy, and buyer networks."
            )

        _, c_next = st.columns([1, 1])
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q2: POLICY ADVOCACY (P7) ─────────────────────────────────────────
    elif step == 2:
        st.markdown(f'{principle_tag(7)} ', unsafe_allow_html=True)
        st.markdown("### 🗣️ Have you raised any issues through your association?")
        why(
            "SEBI calls this 'policy advocacy' — it shows you engage "
            "responsibly with regulators through collective action."
        )

        if p789.get("is_association_member") == "No":
            st.info(
                "Since you are not part of any association, we auto-mark "
                "most P7 questions as **Not Applicable**. This is correct "
                "for most MSMEs."
            )
            p789["policy_advocacy"] = "Not Applicable"
            p789["policy_advocacy_examples"] = ""
            p789["anti_competitive"] = "No"
            good("Smart — no advocacy = no risk. Moving on.")
        else:
            example(
                "Your association wrote to GPCB asking for simpler consent "
                "renewal. Or: wrote to DISCOM about power quality issues."
            )

            options = ["No", "Yes"]
            current = p789.get("policy_advocacy", "No")
            if current not in options:
                current = "No"

            pa = st.radio(
                "Has your association raised issues (electricity, GST, "
                "pollution, infrastructure) on behalf of members?",
                options,
                index=options.index(current),
                horizontal=True
            )
            p789["policy_advocacy"] = pa

            if pa == "Yes":
                ex = st.text_area(
                    "Briefly describe (1-2 examples)",
                    value=p789.get("policy_advocacy_examples", ""),
                    placeholder="e.g. GIDC Association wrote to state govt "
                                "asking for faster industrial plot approval.",
                    height=80
                )
                p789["policy_advocacy_examples"] = ex
                good("Good — this shows responsible collective engagement.")

            st.markdown("---")
            st.markdown("**Have you ever been penalised for unfair competition?**")
            ac_options = ["No", "Yes"]
            current_ac = p789.get("anti_competitive", "No")
            if current_ac not in ac_options:
                current_ac = "No"

            ac = st.radio(
                "Any penalties or adverse orders for anti-competitive "
                "behaviour (like price-fixing, cartels)?",
                ac_options,
                index=ac_options.index(current_ac),
                horizontal=True
            )
            p789["anti_competitive"] = ac

            if ac == "Yes":
                p789["anti_competitive_details"] = st.text_area(
                    "Brief description and corrective action taken",
                    value=p789.get("anti_competitive_details", ""),
                    height=60
                )
                bad("Document corrective actions clearly for the BRSR report.")
            else:
                good("Clean record — this is important for bank audits.")

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q3: LOCAL HIRING (P8) ────────────────────────────────────────────
    elif step == 3:
        st.markdown(f'{principle_tag(8)} ', unsafe_allow_html=True)
        st.markdown("### 👥 Do you hire people from your local area?")
        why(
            "Local hiring supports inclusive growth and is a strong ESG "
            "indicator. Large corporate buyers specifically check this "
            "during vendor onboarding."
        )
        example(
            "Your factory is in Bhavnagar and most of your 25 workers live "
            "in Bhavnagar or nearby villages. That means ~100% local hiring."
        )

        if total_workforce_from_a > 0:
            st.success(
                f"✅ From Section A, we see you have {total_workforce_from_a} "
                "people in your workforce. Estimate what % are local."
            )

        default_pct = p789.get("local_hiring_pct", 80)

        pct = st.slider(
            "Roughly what % of your workers are from your local city or district?",
            0, 100, int(default_pct),
            help="Most MSMEs have 70-100% local workers. Be honest."
        )
        p789["local_hiring_pct"] = pct

        if pct >= 80:
            good(
                f"{pct}% local hiring — excellent. This is a top positive "
                "for inclusive growth disclosures."
            )
        elif pct >= 50:
            good(f"{pct}% local hiring — solid. You can mention this in ESG reports.")
        elif pct > 0:
            warn(
                f"{pct}% local hiring. Consider prioritising local candidates "
                "for new hires — it helps your score."
            )
        else:
            warn("0% local hiring is unusual for MSMEs. Double-check this number.")

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q4: LOCAL SOURCING (P8) ──────────────────────────────────────────
    elif step == 4:
        st.markdown(f'{principle_tag(8)} ', unsafe_allow_html=True)
        st.markdown("### 🧱 Do you buy from local small businesses?")
        why(
            "Sourcing from local MSMEs is a direct BRSR indicator. "
            "It shows you help grow the local economy and reduces "
            "your transport-related emissions."
        )
        example(
            "You buy packaging from a nearby unit, transport from local "
            "truckers, and some components from another Bhavnagar MSME. "
            "That's local sourcing."
        )

        options = ["No", "Yes"]
        current = p789.get("local_sourcing_used", "No")
        if current not in options:
            current = "No"

        uses_local = st.radio(
            "Do you buy raw materials or services from local small businesses?",
            options,
            index=options.index(current),
            horizontal=True
        )
        p789["local_sourcing_used"] = uses_local

        if uses_local == "Yes":
            default_sp = p789.get("local_sourcing_pct", 30)
            pct = st.slider(
                "Approximate % of your total purchases from local small businesses",
                0, 100, int(default_sp)
            )
            p789["local_sourcing_pct"] = pct

            if pct >= 50:
                good(f"{pct}% local sourcing — strong performance.")
            elif pct >= 25:
                good(f"{pct}% local sourcing — good. Try to increase gradually.")
            else:
                warn(
                    f"{pct}% local sourcing. Even small shifts towards local "
                    "suppliers help your ESG profile."
                )
        else:
            p789["local_sourcing_pct"] = 0
            warn(
                "No local sourcing noted. Consider local MSMEs for at "
                "least some inputs — packaging, transport, services."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q5: COMMUNITY SUPPORT (P8) ───────────────────────────────────────
    elif step == 5:
        st.markdown(f'{principle_tag(8)} ', unsafe_allow_html=True)
        st.markdown("### 🏘️ Do you support your local community?")
        why(
            "SEBI calls this 'CSR' or 'inclusive growth'. For MSMEs, "
            "informal support counts too — donations, event sponsorships, "
            "helping schools or hospitals."
        )

        with st.expander("📖 But what about formal CSR? Don't I need that?"):
            st.markdown("""
**Formal CSR (under Companies Act Section 135)** is mandatory only for
companies with:
- Net worth ≥ ₹500 crore, OR
- Turnover ≥ ₹1,000 crore, OR
- Net profit ≥ ₹5 crore

**For most MSMEs, this does not apply.** But informal community support
(donations, sponsorships) still counts positively in your BRSR report —
so document what you do.
            """)

        options = [
            "No",
            "Small donations (temple, school, Gaushala, NGO)",
            "Sponsoring local events (Navratri, sports, cultural)",
            "Helping schools / hospitals / community projects",
            "Other support"
        ]
        current = p789.get("community_support", "No")
        if current not in options:
            current = "No"

        ctype = st.selectbox(
            "In the last year, how did you support your local community?",
            options,
            index=options.index(current)
        )
        p789["community_support"] = ctype

        if ctype != "No":
            details = st.text_area(
                "Describe briefly (amount, activity, beneficiaries)",
                value=p789.get("community_support_details", ""),
                placeholder="e.g. Donated ₹15,000 to local primary school "
                            "for uniforms. Sponsored Ganpati event for ₹5,000. "
                            "Free masks distributed during COVID.",
                height=80
            )
            p789["community_support_details"] = details
            good(
                "This is exactly the kind of story that strengthens your "
                "BRSR report. Large buyers notice these details."
            )
        else:
            warn(
                "Even small, genuine contributions matter. Consider one "
                "small community action in the coming year."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q6: COMMUNITY GRIEVANCE MECHANISM (P8) ──────────────────────────
    elif step == 6:
        st.markdown(f'{principle_tag(8)} ', unsafe_allow_html=True)
        st.markdown("### 📣 How can nearby people contact you with complaints?")
        why(
            "If neighbours have issues (noise, dust, traffic, smoke), "
            "SEBI expects a way for them to reach you. "
            "Having this prevents small issues from becoming big legal problems."
        )
        example(
            "Most common for MSMEs: the owner's phone number is posted at "
            "the factory gate. Or the security guard maintains a complaint "
            "register."
        )

        options = [
            "No formal way",
            "Neighbours call owner/manager directly",
            "Security gate keeps a register",
            "Written complaint box at factory entrance",
            "Other"
        ]
        current = p789.get("community_grievance", "No formal way")
        if current not in options:
            current = "No formal way"

        mech = st.selectbox(
            "If nearby people have complaints, how do they reach you?",
            options,
            index=options.index(current)
        )
        p789["community_grievance"] = mech

        if mech == "No formal way":
            warn(
                "Consider posting a simple board near your factory gate "
                "with owner/manager phone number for complaints. Takes 5 minutes."
            )
        else:
            good(
                "Good — this is exactly what SEBI wants. Document it "
                "in your BRSR report."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q7: PREFERENTIAL PROCUREMENT (P8 Leadership) ─────────────────────
    elif step == 7:
        st.markdown(f'{principle_tag(8)} ', unsafe_allow_html=True)
        st.markdown("### 🎯 Do you give preference to suppliers from weaker sections?")
        why(
            "This is what SEBI calls 'preferential procurement from "
            "vulnerable groups'. It's a leadership indicator — not "
            "mandatory, but a strong positive."
        )
        example(
            "Buying canteen food from a women's self-help group. "
            "Using a SC/ST-owned transport company. "
            "Hiring a differently-abled-run packaging unit."
        )

        options = ["No", "Yes"]
        current = p789.get("pref_vulnerable_proc", "No")
        if current not in options:
            current = "No"

        pref = st.radio(
            "Do you prefer buying from women-owned, minority-owned, or "
            "weaker section suppliers?",
            options,
            index=options.index(current),
            horizontal=True
        )
        p789["pref_vulnerable_proc"] = pref

        if pref == "Yes":
            details = st.text_area(
                "Which groups? Give examples",
                value=p789.get("pref_vulnerable_details", ""),
                placeholder="e.g. Women self-help group supplies our factory canteen. "
                            "Local Dalit-owned transport for deliveries.",
                height=60
            )
            p789["pref_vulnerable_details"] = details
            good(
                "Excellent — this is a strong leadership indicator that "
                "large corporate buyers specifically look for."
            )
        else:
            warn(
                "Not mandatory. If you ever start sourcing from such groups, "
                "it significantly improves your ESG profile."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q8: CUSTOMER COMPLAINT CHANNELS (P9) ────────────────────────────
    elif step == 8:
        st.markdown(f'{principle_tag(9)} ', unsafe_allow_html=True)
        st.markdown("### 📞 How do customers contact you if they have a problem?")
        why(
            "Having clear complaint channels is the #1 thing large buyers "
            "check. Even WhatsApp or phone counts — you don't need a "
            "formal customer care department."
        )
        example(
            "Customers save your shop's WhatsApp number. Phone rings at the "
            "owner's desk. Customers walk in directly for returns. Any of "
            "these count."
        )

        channels = st.multiselect(
            "Select all ways customers can complain:",
            [
                "Phone call",
                "WhatsApp",
                "In-person at shop/factory",
                "Email / Website",
                "Through dealer / distributor",
                "Other"
            ],
            default=p789.get("customer_channels", ["Phone call", "WhatsApp"])
        )
        p789["customer_channels"] = channels

        if len(channels) >= 2:
            good(
                f"{len(channels)} channels available — customers have "
                "multiple ways to reach you. Good."
            )
        elif len(channels) == 1:
            warn(
                "Only one channel. Add WhatsApp or a phone number — "
                "it's free and covers most customer needs."
            )
        else:
            bad(
                "No clear channels means customers can't easily complain. "
                "This is a risk — add at least phone or WhatsApp."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q9: COMPLAINT RECORD + VOLUME + RESOLUTION (P9) ─────────────────
    elif step == 9:
        st.markdown(f'{principle_tag(9)} ', unsafe_allow_html=True)
        st.markdown("### 📓 How do you track customer complaints?")
        why(
            "A simple register — notebook, Excel, or CRM — is what "
            "auditors and buyers want to see. Even a basic notebook counts."
        )
        example(
            "Notebook with columns: Date | Customer Name | Phone | Issue | "
            "Action Taken | Resolved Date. Takes 30 seconds per entry."
        )

        options = [
            "No record",
            "Notebook register",
            "Excel / Google Sheet",
            "Software / CRM system"
        ]
        current = p789.get("complaint_record", "No record")
        if current not in options:
            current = "No record"

        record = st.selectbox(
            "How do you track customer complaints?",
            options,
            index=options.index(current)
        )
        p789["complaint_record"] = record

        if record == "No record":
            bad(
                "Start today. Even a ₹20 notebook is enough. This single "
                "step significantly improves your BRSR score."
            )
        else:
            good(f"Good — you track complaints via {record}.")

        # Complaint volume
        st.markdown("---")
        st.markdown("**Complaint numbers this year:**")
        cc1, cc2 = st.columns(2)
        with cc1:
            received = st.number_input(
                "Total complaints received this year",
                min_value=0,
                value=int(p789.get("complaints_received_yr", 0))
            )
            p789["complaints_received_yr"] = received

        with cc2:
            resolved = st.number_input(
                "How many were resolved?",
                min_value=0,
                max_value=max(received, 0),
                value=int(p789.get("complaints_resolved_yr", 0))
            )
            p789["complaints_resolved_yr"] = resolved

        if received > 0:
            rate = safe_pct(resolved, received)
            calc(
                f"Resolution rate: {resolved}/{received} = {rate}%"
            )
            if rate == 100:
                good("100% resolution — outstanding.")
            elif rate >= 80:
                good(f"{rate}% resolution — strong performance.")
            elif rate >= 50:
                warn(f"{rate}% resolution. Try to resolve pending cases faster.")
            else:
                bad(
                    f"Only {rate}% resolved. Focus on closing pending "
                    "complaints — this is a major audit red flag."
                )
        else:
            good(
                "Zero complaints this year. Possible if you handle "
                "issues informally on the spot."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q10: PRODUCT INFORMATION (P9) ───────────────────────────────────
    elif step == 10:
        st.markdown(f'{principle_tag(9)} ', unsafe_allow_html=True)
        st.markdown("### 🏷️ Do you clearly tell customers about your product?")
        why(
            "SEBI wants to know if customers get clear information about "
            "price, safe usage, and disposal. Even simple labels or bills count."
        )
        example(
            "Price on the bill, usage instructions on the packet, "
            "expiry date printed, 'handle with care' sticker on fragile items."
        )

        options = ["Yes", "No"]
        current = p789.get("product_info_clear", "Yes")
        if current not in options:
            current = "Yes"

        pi = st.radio(
            "Do you provide clear product/service information to customers?",
            options,
            index=options.index(current),
            horizontal=True
        )
        p789["product_info_clear"] = pi

        if pi == "Yes":
            details = st.text_area(
                "How do you share this info? (labels, bills, WhatsApp, etc.)",
                value=p789.get("product_info_details", ""),
                placeholder="e.g. Price and usage printed on packaging. "
                            "WhatsApp catalogue shared with customers. "
                            "Safety stickers on machine parts.",
                height=80
            )
            p789["product_info_details"] = details
            good("Good — clear information reduces disputes and builds trust.")
        else:
            warn(
                "Consider adding basic info on bills, labels, or a "
                "WhatsApp broadcast. Takes minimal effort, big impact."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q11: CUSTOMER DATA STORAGE + PRIVACY (P9) ───────────────────────
    elif step == 11:
        st.markdown(f'{principle_tag(9)} ', unsafe_allow_html=True)
        st.markdown("### 🔐 Do you store customer data? Is it safe?")
        why(
            "SEBI calls this 'data privacy and cybersecurity'. "
            "For MSMEs, this means: if you save customer phone numbers, "
            "GST numbers, or addresses — don't share them with outsiders."
        )

        with st.expander("📖 What counts as 'customer data' for an MSME?"):
            st.markdown("""
**Customer data includes:**
- Phone numbers saved in your phone/Tally
- GST numbers / Aadhaar copies you keep on file
- Addresses and email IDs
- Past order history
- Credit / payment information

**Good practice for MSMEs:**
- Keep Tally / CRM password-protected
- Don't share customer lists with other businesses
- Delete old data you no longer need
- Tell staff: 'we do not share customer info with outsiders'
            """)

        options = ["No", "Yes"]
        current = p789.get("stores_customer_data", "No")
        if current not in options:
            current = "No"

        store = st.radio(
            "Do you store customer phone numbers, GST details, addresses, etc.?",
            options,
            index=options.index(current),
            horizontal=True
        )
        p789["stores_customer_data"] = store

        if store == "Yes":
            rule_options = ["No", "Yes"]
            current_rule = p789.get("data_privacy_rule", "No")
            if current_rule not in rule_options:
                current_rule = "No"

            rule = st.radio(
                "Do you have a basic rule like 'we don't share customer "
                "data with outsiders'?",
                rule_options,
                index=rule_options.index(current_rule),
                horizontal=True
            )
            p789["data_privacy_rule"] = rule

            if rule == "Yes":
                good(
                    "Great — even a simple internal rule counts as data "
                    "privacy policy for BRSR purposes."
                )
            else:
                warn(
                    "Adopt this one rule today and tell your staff. "
                    "It satisfies basic data privacy requirements at zero cost."
                )
        else:
            p789["data_privacy_rule"] = "Not Applicable"
            good("No customer data stored = low privacy risk. Simple.")

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q12: PRODUCT RECALLS (P9) ───────────────────────────────────────
    elif step == 12:
        st.markdown(f'{principle_tag(9)} ', unsafe_allow_html=True)
        st.markdown("### ⚠️ Have you ever had to recall or replace unsafe products?")
        why(
            "Product recalls are serious. SEBI wants honest disclosure. "
            "Hiding past issues is worse than disclosing them with "
            "corrective actions."
        )
        example(
            "A food packet had a contamination issue — you recalled that "
            "batch. Or a machine part was faulty — you replaced it for "
            "all customers."
        )

        options = ["No", "Yes"]
        current = p789.get("product_recalls", "No")
        if current not in options:
            current = "No"

        pr = st.radio(
            "In the last 3 years, did you ever recall or replace products "
            "due to safety or quality issues?",
            options,
            index=options.index(current),
            horizontal=True
        )
        p789["product_recalls"] = pr

        if pr == "Yes":
            details = st.text_area(
                "Briefly describe what happened and what you did",
                value=p789.get("product_recalls_details", ""),
                placeholder="e.g. In 2024, one batch of packaging had a "
                            "defect. We recalled 50 units from 12 customers "
                            "and replaced them free. Process now includes "
                            "double QC check.",
                height=100
            )
            p789["product_recalls_details"] = details
            warn(
                "Document honestly. Showing corrective action is better "
                "than hiding issues — auditors respect transparency."
            )
        else:
            good(
                "No recalls — shows good quality control. Keep this "
                "record clean by documenting your QC processes."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q13: SUMMARY / FINISH ──────────────────────────────────────────
    elif step == 13:
        st.markdown(f'{principle_tag(9)} ', unsafe_allow_html=True)
        st.markdown("### 🎉 Final Check — Ready to See Your Score?")

        st.info(
            "You've answered all 13 questions covering P7, P8, and P9. "
            "Click 'Finish' to see your combined score and recommendations."
        )

        # Show a mini-preview
        st.markdown("**Your answers at a glance:**")
        preview_data = [
            ("Association Member", p789.get("is_association_member", "—")),
            ("Local Hiring", f"{p789.get('local_hiring_pct', 0)}%"),
            ("Local Sourcing", f"{p789.get('local_sourcing_pct', 0)}%"),
            ("Community Support", p789.get("community_support", "—")),
            ("Customer Channels", ", ".join(p789.get("customer_channels", [])) or "—"),
            ("Complaint Tracking", p789.get("complaint_record", "—")),
            ("Data Privacy", "Protected" if p789.get("data_privacy_rule") == "Yes"
             else "Not Applicable" if p789.get("stores_customer_data") == "No"
             else "Needs attention"),
        ]
        df = pd.DataFrame(preview_data, columns=["Area", "Your Answer"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Finish & See Results 🎉",
                         type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── FINAL SUMMARY ──────────────────────────────────────────────────
    elif step > 13:
        st.balloons()

        st.markdown(
            '<div class="section-win">'
            '<div style="font-size:48px">🎉</div>'
            '<div style="font-size:22px;font-weight:700;color:#1b5e20;">'
            'P7, P8 & P9 Quick Mode Complete!</div>'
            '<div style="font-size:14px;color:#2e7d32;margin-top:8px;">'
            'Policy, Community, and Customer disclosures done.'
            '</div></div>',
            unsafe_allow_html=True
        )

        score = calc_p789_score()
        p789["score"] = score
        colour = ("green" if score >= 70
                  else "orange" if score >= 40 else "red")
        st.markdown(
            f"<h2 style='color:{colour};text-align:center'>{score}/100</h2>"
            "<p style='text-align:center;color:gray'>"
            "Combined P7 + P8 + P9 Score</p>",
            unsafe_allow_html=True
        )
        st.progress(score / 100)

        # Breakdown
        st.markdown("---")
        st.markdown("### Score Breakdown")
        m1, m2, m3 = st.columns(3)

        p7_s = 0
        if p789.get("is_association_member") == "Yes": p7_s += 10
        if p789.get("policy_advocacy") == "Yes": p7_s += 5
        if p789.get("anti_competitive") == "No": p7_s += 5

        p8_s = 0
        lh = p789.get("local_hiring_pct", 0)
        if lh >= 70: p8_s += 12
        elif lh >= 40: p8_s += 8
        elif lh > 0: p8_s += 4
        ls = p789.get("local_sourcing_pct", 0)
        if ls >= 50: p8_s += 10
        elif ls >= 25: p8_s += 6
        elif ls > 0: p8_s += 3
        if p789.get("community_support") != "No": p8_s += 8
        if p789.get("community_grievance") != "No formal way": p8_s += 5
        if p789.get("pref_vulnerable_proc") == "Yes": p8_s += 5

        p9_s = score - p7_s - p8_s

        m1.metric("P7 — Policy", f"{p7_s}/20")
        m2.metric("P8 — Community", f"{p8_s}/40")
        m3.metric("P9 — Customers", f"{p9_s}/40")

        # Recommendations
        st.markdown("---")
        st.markdown("### 🎯 Smart Recommendations")
        recs = build_recommendations()
        if recs:
            for r in recs:
                warn(r)
        else:
            good("No major gaps — your P7, P8, P9 profile looks strong!")

        # Final actions
        st.markdown("---")
        op1, op2 = st.columns(2)
        with op1:
            if st.button("📋 Switch to Full Mode",
                         use_container_width=True):
                st.session_state.p789_mode = "full"
                st.rerun()
        with op2:
            if st.button("💾 Save & Finish BRSR Section C →",
                         use_container_width=True, type="primary"):
                st.session_state.c_p789 = p789
                st.success(
                    "✅ All 9 Principles of Section C complete! "
                    "You can now generate the final BRSR PDF report."
                )

# ═════════════════════════════════════════════════════════════════════════════
# FULL MODE — All SEBI indicators with tabs
# ═════════════════════════════════════════════════════════════════════════════
else:

    full_step = st.session_state.p789_full_step

    full_steps = {
        1: "🏛️ P7: Policy",
        2: "🏘️ P8: Community",
        3: "📞 P9: Customers",
        4: "✅ Summary"
    }

    nav = st.columns(4)
    for i, (num, label) in enumerate(full_steps.items()):
        with nav[i]:
            t = "primary" if full_step == num else "secondary"
            if st.button(label, key=f"fn789_{num}",
                         type=t, use_container_width=True):
                st.session_state.p789_full_step = num
                st.rerun()

    st.progress(full_step / len(full_steps))
    st.markdown("---")

    # ── FULL STEP 1: P7 ──────────────────────────────────────────────────
    if full_step == 1:
        st.header("🏛️ Principle 7 — Policy & Advocacy")

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q1 — Trade/Industry Associations")

            num_aff = st.number_input(
                "Number of trade/industry associations you are affiliated with",
                min_value=0,
                value=len(p789.get("associations_list", [])),
                key="f_num_aff"
            )

            st.markdown("**Top 10 associations you are a member of:**")
            st.caption("Fill only those you are actually a member of. Leave blank otherwise.")

            assoc_data = p789.get("p7_assoc_full", {})
            for i in range(1, 11):
                ac = st.columns([1, 4, 2])
                ac[0].markdown(f"**{i}.**")
                name = ac[1].text_input(
                    "Association name",
                    value=assoc_data.get(f"name_{i}", ""),
                    key=f"f_assoc_name_{i}",
                    label_visibility="collapsed",
                    placeholder="e.g. GIDC Bhavnagar Association"
                )
                reach = ac[2].selectbox(
                    "Reach",
                    ["—", "State", "National"],
                    index=["—", "State", "National"].index(
                        assoc_data.get(f"reach_{i}", "—")
                    ),
                    key=f"f_assoc_reach_{i}",
                    label_visibility="collapsed"
                )
                assoc_data[f"name_{i}"] = name
                assoc_data[f"reach_{i}"] = reach

            p789["p7_assoc_full"] = assoc_data

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q2 — Anti-Competitive Conduct")
            st.caption(
                "Any adverse orders from CCI or other regulators for "
                "anti-competitive behaviour (price-fixing, cartels, etc.)?"
            )

            p789["anti_competitive"] = st.radio(
                "Any adverse orders related to anti-competitive conduct?",
                ["No", "Yes"],
                horizontal=True,
                index=["No", "Yes"].index(
                    p789.get("anti_competitive", "No")
                    if p789.get("anti_competitive") in ["No", "Yes"] else "No"
                ),
                key="f_ac"
            )

            if p789["anti_competitive"] == "Yes":
                st.markdown("**Detail the cases:**")
                ac_data = p789.get("p7_ac_cases", {})
                for i in range(1, 4):
                    st.markdown(f"**Case {i}**")
                    ac = st.columns(3)
                    ac_data[f"auth_{i}"] = ac[0].text_input(
                        "Authority", value=ac_data.get(f"auth_{i}", ""),
                        key=f"f_ac_auth_{i}"
                    )
                    ac_data[f"brief_{i}"] = ac[1].text_area(
                        "Brief", value=ac_data.get(f"brief_{i}", ""),
                        key=f"f_ac_brief_{i}", height=80
                    )
                    ac_data[f"action_{i}"] = ac[2].text_area(
                        "Corrective action",
                        value=ac_data.get(f"action_{i}", ""),
                        key=f"f_ac_action_{i}", height=80
                    )
                p789["p7_ac_cases"] = ac_data

        with st.container(border=True):
            badge_l()
            st.markdown("#### Leadership — Public Policy Positions")
            st.caption(
                "Policies your business has advocated for publicly. "
                "Most MSMEs leave this blank."
            )

            pol_data = p789.get("p7_pol_advocacy", {})
            for i in range(1, 4):
                st.markdown(f"**Policy position {i}**")
                ac = st.columns(2)
                pol_data[f"policy_{i}"] = ac[0].text_input(
                    "Policy advocated",
                    value=pol_data.get(f"policy_{i}", ""),
                    key=f"f_pol_{i}"
                )
                pol_data[f"method_{i}"] = ac[0].text_input(
                    "Method (meeting, letter, petition)",
                    value=pol_data.get(f"method_{i}", ""),
                    key=f"f_pol_m_{i}"
                )
                pol_data[f"public_{i}"] = ac[1].selectbox(
                    "In public domain?",
                    ["—", "Yes", "No"],
                    index=["—", "Yes", "No"].index(
                        pol_data.get(f"public_{i}", "—")
                    ),
                    key=f"f_pol_pub_{i}"
                )
                pol_data[f"link_{i}"] = ac[1].text_input(
                    "Web link (if any)",
                    value=pol_data.get(f"link_{i}", ""),
                    key=f"f_pol_link_{i}"
                )

            p789["p7_pol_advocacy"] = pol_data

        _, c_next = st.columns([1, 1])
        with c_next:
            if st.button("Next: P8 →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 2: P8 ──────────────────────────────────────────────────
    elif full_step == 2:
        st.header("🏘️ Principle 8 — Inclusive Growth & Community")

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q1 — Social Impact Assessments (SIA)")
            st.info(
                "SIAs apply only to large infrastructure projects requiring "
                "land acquisition. **For most MSMEs this is Not Applicable.**"
            )
            p789["sia_applicable"] = st.radio(
                "Do any SIAs apply to your business?",
                ["Not Applicable", "Yes"],
                horizontal=True,
                index=0 if p789.get("sia_applicable", "Not Applicable") == "Not Applicable" else 1,
                key="f_sia_app"
            )
            if p789["sia_applicable"] == "Yes":
                sia_data = p789.get("p8_sia", {})
                for i in range(1, 3):
                    st.markdown(f"**SIA Project {i}**")
                    ac = st.columns(3)
                    sia_data[f"name_{i}"] = ac[0].text_input(
                        "Project name & brief",
                        value=sia_data.get(f"name_{i}", ""),
                        key=f"f_sia_n_{i}"
                    )
                    sia_data[f"notif_{i}"] = ac[1].text_input(
                        "SIA Notification No.",
                        value=sia_data.get(f"notif_{i}", ""),
                        key=f"f_sia_no_{i}"
                    )
                    sia_data[f"ext_{i}"] = ac[2].selectbox(
                        "External agency?",
                        ["—", "Yes", "No"],
                        index=["—", "Yes", "No"].index(
                            sia_data.get(f"ext_{i}", "—")
                        ),
                        key=f"f_sia_e_{i}"
                    )
                p789["p8_sia"] = sia_data

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q2 — Rehabilitation & Resettlement")
            st.info(
                "R&R applies only to projects that displaced families. "
                "**For most MSMEs this is Not Applicable.**"
            )
            p789["rr_applicable"] = st.radio(
                "Does R&R apply to your business?",
                ["Not Applicable", "Yes"],
                horizontal=True,
                index=0 if p789.get("rr_applicable", "Not Applicable") == "Not Applicable" else 1,
                key="f_rr_app"
            )

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q3 — Community Grievance Mechanism")
            p789["community_grievance_desc"] = st.text_area(
                "How can community members raise grievances?",
                value=p789.get("community_grievance_desc", ""),
                height=100,
                placeholder="e.g. Neighbours can call the factory manager directly. "
                            "Security gate maintains a complaint register. "
                            "Monthly review of complaints by the owner.",
                key="f_cg_desc"
            )

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q4 — Local Sourcing (% of inputs)")
            example(
                "If 30% of your ₹10 lakh purchases were from local small "
                "suppliers = 30%."
            )

            sr = st.columns(2)
            with sr[0]:
                st.markdown("**Current FY**")
                p789["src_msme_cur"] = st.number_input(
                    "% directly from MSMEs / small producers",
                    min_value=0, max_value=100,
                    value=int(p789.get("src_msme_cur", p789.get("local_sourcing_pct", 0))),
                    key="f_sm_cur"
                )
                p789["src_district_cur"] = st.number_input(
                    "% from within district / neighbouring districts",
                    min_value=0, max_value=100,
                    value=int(p789.get("src_district_cur", 0)),
                    key="f_sd_cur"
                )
            with sr[1]:
                st.markdown("**Previous FY**")
                p789["src_msme_prev"] = st.number_input(
                    "% from MSMEs (Prev FY)",
                    min_value=0, max_value=100,
                    value=int(p789.get("src_msme_prev", 0)),
                    key="f_sm_prev"
                )
                p789["src_district_prev"] = st.number_input(
                    "% from local districts (Prev FY)",
                    min_value=0, max_value=100,
                    value=int(p789.get("src_district_prev", 0)),
                    key="f_sd_prev"
                )

        with st.container(border=True):
            badge_l()
            st.markdown("#### Leadership — Preferential Procurement, CSR, Traditional Knowledge")

            lt = st.tabs([
                "🎯 L3: Preferential Procurement",
                "🗺️ L2: Aspirational Districts",
                "🎨 L4-L5: Traditional Knowledge IP",
                "👥 L6: CSR Beneficiaries"
            ])

            with lt[0]:
                p789["pref_vulnerable_proc"] = st.radio(
                    "Do you prefer vulnerable group suppliers?",
                    ["No", "Yes"],
                    horizontal=True,
                    index=["No", "Yes"].index(
                        p789.get("pref_vulnerable_proc", "No")
                        if p789.get("pref_vulnerable_proc") in ["No", "Yes"] else "No"
                    ),
                    key="f_pref"
                )
                if p789["pref_vulnerable_proc"] == "Yes":
                    p789["pref_groups"] = st.text_input(
                        "Which groups?",
                        value=p789.get("pref_groups", ""),
                        placeholder="e.g. Women self-help groups, SC/ST-owned businesses",
                        key="f_pref_g"
                    )
                    p789["pref_pct"] = st.number_input(
                        "% of total procurement",
                        min_value=0, max_value=100,
                        value=int(p789.get("pref_pct", 0)),
                        key="f_pref_p"
                    )

            with lt[1]:
                st.caption(
                    "Aspirational districts are 112 districts identified by NITI "
                    "Aayog as lagging. Most MSMEs don't operate there."
                )
                p789["asp_applicable"] = st.radio(
                    "Any CSR projects in aspirational districts?",
                    ["Not Applicable", "Yes"],
                    horizontal=True,
                    index=0 if p789.get("asp_applicable", "Not Applicable") == "Not Applicable" else 1,
                    key="f_asp"
                )

            with lt[2]:
                st.caption(
                    "Applies if your business uses traditional designs, "
                    "recipes, or formulas (e.g., Ayurvedic, local crafts)."
                )
                p789["ip_trad_applicable"] = st.radio(
                    "Do you use IP based on traditional knowledge?",
                    ["Not Applicable", "Yes"],
                    horizontal=True,
                    index=0 if p789.get("ip_trad_applicable", "Not Applicable") == "Not Applicable" else 1,
                    key="f_ip_trad"
                )

            with lt[3]:
                st.caption(
                    "Applies if you've run any community projects."
                )
                p789["csr_benef"] = st.text_area(
                    "CSR projects and number of people benefitted",
                    value=p789.get("csr_benef", ""),
                    height=80,
                    placeholder="e.g. Supported 50 students at local school "
                                "with uniforms and books. 30 from vulnerable families.",
                    key="f_csr_b"
                )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: P9 →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 3: P9 ──────────────────────────────────────────────────
    elif full_step == 3:
        st.header("📞 Principle 9 — Customer Responsibility")

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q1 — Customer Complaint Mechanism")
            p789["p9_mechanism_desc"] = st.text_area(
                "Describe your customer complaint handling process",
                value=p789.get("p9_mechanism_desc", ""),
                height=100,
                placeholder="e.g. Customers can call our WhatsApp business number "
                            "or directly come to the factory. All complaints are "
                            "logged in an Excel register. Resolved within 2 working days.",
                key="f_p9_mech"
            )

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q2 — Product Information Coverage")
            st.caption("% of turnover where customers receive info on:")

            info_data = p789.get("p9_info_pct", {})
            for label, key in [
                ("Environmental & social parameters", "env_soc"),
                ("Safe and responsible usage", "safe_usage"),
                ("Recycling / safe disposal", "recycling")
            ]:
                ic = st.columns([3, 1])
                ic[0].markdown(f"**{label}**")
                info_data[key] = ic[1].number_input(
                    label, min_value=0, max_value=100,
                    value=info_data.get(key, 0),
                    key=f"f_info_{key}",
                    label_visibility="collapsed"
                )
            p789["p9_info_pct"] = info_data

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q3 — Complaints by Category")

            complaint_cats = [
                "Data privacy",
                "Advertising",
                "Cyber-security",
                "Delivery of essential services",
                "Restrictive Trade Practices",
                "Unfair Trade Practices",
                "Other"
            ]

            cd = p789.get("p9_complaint_data", {})

            ch = st.columns(5)
            ch[0].markdown("**Category**")
            ch[1].markdown("**Cur: Received**")
            ch[2].markdown("**Cur: Pending**")
            ch[3].markdown("**Prev: Received**")
            ch[4].markdown("**Prev: Pending**")

            for cat in complaint_cats:
                cr = st.columns(5)
                cr[0].markdown(f"*{cat}*")
                cd[f"{cat}_cur_rec"] = cr[1].number_input(
                    f"{cat} cr", min_value=0,
                    value=cd.get(f"{cat}_cur_rec", 0),
                    key=f"f_cp_{cat}_cr", label_visibility="collapsed"
                )
                cd[f"{cat}_cur_pen"] = cr[2].number_input(
                    f"{cat} cp", min_value=0,
                    value=cd.get(f"{cat}_cur_pen", 0),
                    key=f"f_cp_{cat}_cp", label_visibility="collapsed"
                )
                cd[f"{cat}_prev_rec"] = cr[3].number_input(
                    f"{cat} pr", min_value=0,
                    value=cd.get(f"{cat}_prev_rec", 0),
                    key=f"f_cp_{cat}_pr", label_visibility="collapsed"
                )
                cd[f"{cat}_prev_pen"] = cr[4].number_input(
                    f"{cat} pp", min_value=0,
                    value=cd.get(f"{cat}_prev_pen", 0),
                    key=f"f_cp_{cat}_pp", label_visibility="collapsed"
                )

            p789["p9_complaint_data"] = cd

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q4 — Product Recalls")
            rc = st.columns(2)
            with rc[0]:
                st.markdown("**Voluntary Recalls**")
                p789["vol_recalls_num"] = st.number_input(
                    "Number", min_value=0,
                    value=int(p789.get("vol_recalls_num", 0)),
                    key="f_vol_n"
                )
                p789["vol_recalls_reason"] = st.text_area(
                    "Reasons",
                    value=p789.get("vol_recalls_reason", ""),
                    height=80, key="f_vol_r"
                )
            with rc[1]:
                st.markdown("**Forced Recalls**")
                p789["forced_recalls_num"] = st.number_input(
                    "Number",
                    min_value=0,
                    value=int(p789.get("forced_recalls_num", 0)),
                    key="f_for_n"
                )
                p789["forced_recalls_reason"] = st.text_area(
                    "Reasons",
                    value=p789.get("forced_recalls_reason", ""),
                    height=80, key="f_for_r"
                )

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q5 — Cybersecurity & Data Privacy Policy")
            p789["cyber_policy"] = st.radio(
                "Do you have a formal framework/policy on cybersecurity "
                "and data privacy?",
                ["No", "Yes"],
                horizontal=True,
                index=["No", "Yes"].index(
                    p789.get("cyber_policy", "No")
                    if p789.get("cyber_policy") in ["No", "Yes"] else "No"
                ),
                key="f_cyber"
            )
            if p789["cyber_policy"] == "Yes":
                p789["cyber_link"] = st.text_input(
                    "Web link to policy (if available)",
                    value=p789.get("cyber_link", ""),
                    key="f_cyber_link"
                )

        with st.container(border=True):
            badge_e()
            st.markdown("#### Essential Q6 — Corrective Actions")
            p789["p9_corrective"] = st.text_area(
                "Corrective actions on advertising, essential services, "
                "cybersecurity, data privacy, recalls, or regulatory penalties",
                value=p789.get("p9_corrective", ""),
                height=100,
                key="f_p9_corr"
            )

        with st.container(border=True):
            badge_l()
            st.markdown("#### Leadership Indicators")

            lt = st.tabs([
                "📢 L1: Info Channels",
                "📚 L2: Safe Usage Education",
                "⚠️ L3: Service Disruption",
                "📊 L4: Extra Info & Surveys",
                "🔒 L5: Data Breaches"
            ])

            with lt[0]:
                p789["info_channels"] = st.text_area(
                    "Channels where product info is available",
                    value=p789.get("info_channels", ""),
                    placeholder="e.g. Website, WhatsApp catalogue, dealer network, brochures",
                    height=80, key="f_info_ch"
                )

            with lt[1]:
                p789["safe_usage_education"] = st.text_area(
                    "How you educate customers on safe product use",
                    value=p789.get("safe_usage_education", ""),
                    placeholder="e.g. Printed labels, WhatsApp video demos, "
                                "dealer training sessions",
                    height=80, key="f_safe_edu"
                )

            with lt[2]:
                p789["service_disruption"] = st.text_area(
                    "How you inform customers of service disruption",
                    value=p789.get("service_disruption", ""),
                    placeholder="e.g. WhatsApp broadcast, website notice, "
                                "direct phone call to key customers",
                    height=80, key="f_serv_dis"
                )

            with lt[3]:
                p789["extra_info_display"] = st.radio(
                    "Do you display product info beyond legal requirements?",
                    ["No", "Yes", "Not Applicable"],
                    horizontal=True,
                    index=["No", "Yes", "Not Applicable"].index(
                        p789.get("extra_info_display", "No")
                        if p789.get("extra_info_display") in ["No", "Yes", "Not Applicable"] else "No"
                    ),
                    key="f_extra_info"
                )
                p789["surveys_done"] = st.radio(
                    "Did you conduct customer satisfaction surveys?",
                    ["No", "Yes"],
                    horizontal=True,
                    index=["No", "Yes"].index(
                        p789.get("surveys_done", "No")
                        if p789.get("surveys_done") in ["No", "Yes"] else "No"
                    ),
                    key="f_surveys"
                )

            with lt[4]:
                p789["data_breaches_num"] = st.number_input(
                    "Number of data breaches this year",
                    min_value=0,
                    value=int(p789.get("data_breaches_num", 0)),
                    key="f_db_num"
                )
                p789["data_breaches_pii_pct"] = st.number_input(
                    "% of breaches involving personal customer info",
                    min_value=0, max_value=100,
                    value=int(p789.get("data_breaches_pii_pct", 0)),
                    key="f_db_pii"
                )
                if p789["data_breaches_num"] > 0:
                    bad(
                        "Document breach details, corrective actions, "
                        "and customer notifications in your BRSR report."
                    )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Summary →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 4: SUMMARY ─────────────────────────────────────────────
    elif full_step == 4:
        st.header("✅ Principles 7, 8, 9 — Full Mode Summary")

        score = calc_p789_score()
        p789["score"] = score
        colour = ("green" if score >= 70
                  else "orange" if score >= 40 else "red")
        st.markdown(
            f"<h2 style='color:{colour};text-align:center'>{score}/100</h2>"
            "<p style='text-align:center;color:gray'>Combined P7+P8+P9 Score</p>",
            unsafe_allow_html=True
        )
        st.progress(score / 100)

        st.markdown("---")

        # BRSR-ready summary
        with st.container(border=True):
            st.markdown("#### BRSR-Ready Summary Table")

            summary_data = [
                ["P7 — Trade associations",
                 str(len(p789.get("associations_list", []))), "number"],
                ["P7 — Anti-competitive orders",
                 p789.get("anti_competitive", "—"), "—"],
                ["P8 — Local hiring",
                 f"{p789.get('local_hiring_pct', 0)}%", "—"],
                ["P8 — Local MSME sourcing",
                 f"{p789.get('src_msme_cur', p789.get('local_sourcing_pct', 0))}%", "—"],
                ["P8 — Community support",
                 p789.get("community_support", "—"), "—"],
                ["P8 — Preferential procurement",
                 p789.get("pref_vulnerable_proc", "—"), "—"],
                ["P9 — Customer complaints (current)",
                 str(p789.get("complaints_received_yr", 0)), "number"],
                ["P9 — Resolution rate",
                 f"{safe_pct(p789.get('complaints_resolved_yr', 0), p789.get('complaints_received_yr', 0))}%", "—"],
                ["P9 — Product recalls",
                 p789.get("product_recalls", "—"), "—"],
                ["P9 — Cybersecurity policy",
                 p789.get("cyber_policy", "—"), "—"],
            ]
            df = pd.DataFrame(
                summary_data,
                columns=["Parameter", "Value", "Unit"]
            )
            st.dataframe(df, use_container_width=True, hide_index=True)

        # Recommendations
        st.markdown("---")
        st.markdown("### 🎯 Recommendations")
        recs = build_recommendations()
        if recs:
            for r in recs:
                warn(r)
        else:
            good("No major gaps — your P7, P8, P9 profile is solid!")

        st.markdown("---")
        cf1, cf2, cf3 = st.columns([1, 2, 1])
        with cf2:
            if st.button("💾 Save & Finish Section C →",
                         type="primary", use_container_width=True):
                st.session_state.c_p789 = p789
                st.balloons()
                st.success(
                    "✅ Section C fully complete! Ready for final PDF generation."
                )

        c_back2, _, _ = st.columns([1, 2, 1])
        with c_back2:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()