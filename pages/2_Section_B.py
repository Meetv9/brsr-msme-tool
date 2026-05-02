import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BRSR Section B | MSME Tool",
    page_icon="📋",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS — matches Section A style
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    div[data-testid="metric-container"] {
        background: #f0f4ff;
        border: 1px solid #d0dcff;
        border-radius: 10px;
        padding: 12px 16px;
    }
    .tip-box {
        background: #f0faf4;
        border-left: 4px solid #2ecc71;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 14px;
        margin: 8px 0;
    }
    .warn-box {
        background: #fffbf0;
        border-left: 4px solid #f39c12;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        font-size: 14px;
        margin: 8px 0;
    }
    .principle-card {
        background: #ffffff;
        border: 1px solid #e0e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .policy-box {
        background: #f0fff4;
        border: 1px dashed #2ecc71;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 13px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS — 9 NGRBC PRINCIPLES
# ─────────────────────────────────────────────────────────────────────────────
PRINCIPLES = {
    "P1": {
        "title": "Ethics & Transparency",
        "simple": "Run your business honestly. No bribes, no fraud, no misleading anyone.",
        "example": "Example: You have a clear pricing policy and never pay bribes to get contracts.",
        "policy_template": "Our business commits to conducting all operations with honesty and transparency. We will not engage in bribery, corruption, or unfair trade practices. All financial records will be maintained accurately and made available to relevant authorities on request."
    },
    "P2": {
        "title": "Safe & Sustainable Products",
        "simple": "Your products/services should be safe to use and not harm the environment.",
        "example": "Example: Your food product uses safe ingredients and is properly labelled with expiry dates.",
        "policy_template": "Our business commits to providing products and services that are safe, reliable, and environmentally responsible. We will clearly label our products, follow all safety standards, and continuously work to reduce environmental impact across our supply chain."
    },
    "P3": {
        "title": "Employee Wellbeing",
        "simple": "Take care of your workers — fair pay, safe workplace, no exploitation.",
        "example": "Example: You pay minimum wage or above, provide safety equipment, and give leave as per law.",
        "policy_template": "Our business treats all employees and contract workers with dignity and respect. We commit to providing safe working conditions, fair wages as per applicable law, equal opportunities, and freedom from discrimination or harassment in the workplace."
    },
    "P4": {
        "title": "Stakeholder Engagement",
        "simple": "Listen to and communicate with everyone your business affects — customers, suppliers, neighbours.",
        "example": "Example: You inform the local community before starting noisy construction work.",
        "policy_template": "Our business recognises the importance of engaging with all stakeholders — including employees, customers, suppliers, communities, and government. We commit to maintaining open communication channels and addressing concerns raised by any stakeholder group."
    },
    "P5": {
        "title": "Human Rights",
        "simple": "Treat every person with dignity. No child labour, no forced labour, no discrimination.",
        "example": "Example: You do not employ anyone under 18 years of age and do not discriminate based on caste, gender, or religion.",
        "policy_template": "Our business respects the human rights of all individuals connected to our operations. We commit to zero tolerance for child labour, forced labour, or any form of discrimination. We will take steps to ensure our suppliers also respect these principles."
    },
    "P6": {
        "title": "Environmental Care",
        "simple": "Reduce your pollution, use resources carefully, don't damage nature.",
        "example": "Example: You have reduced plastic packaging, or installed a rainwater harvesting system.",
        "policy_template": "Our business is committed to minimising our environmental footprint. We will work to reduce energy consumption, water usage, and waste generation. We will comply with all applicable environmental laws and continuously improve our environmental performance."
    },
    "P7": {
        "title": "Responsible Policy Engagement",
        "simple": "If you engage with government or industry associations, do it fairly and transparently.",
        "example": "Example: You are a member of a trade association and participate in industry consultations honestly.",
        "policy_template": "Our business will engage with government bodies, regulators, and industry associations in a transparent and ethical manner. We will not use unfair means to influence policy decisions and will disclose any such engagements as required."
    },
    "P8": {
        "title": "Inclusive Growth",
        "simple": "Support the local community and include small suppliers and marginalised groups.",
        "example": "Example: You source raw materials from local small farmers or employ people from economically weaker sections.",
        "policy_template": "Our business is committed to contributing to inclusive economic growth. We will prioritise local sourcing where possible, support skill development in our community, and ensure our business practices benefit not just shareholders but also the broader community."
    },
    "P9": {
        "title": "Customer Responsibility",
        "simple": "Be honest with customers — no false advertising, handle complaints fairly, protect their data.",
        "example": "Example: Your product labels are accurate, you have a return/refund policy, and you protect customer information.",
        "policy_template": "Our business commits to responsible customer engagement. We will provide accurate product information, handle customer complaints promptly and fairly, protect customer data, and never engage in misleading advertising or unfair trade practices."
    }
}

REVIEW_FREQUENCY = ["Annually", "Half-Yearly", "Quarterly", "Not reviewed yet"]
CERTIFICATIONS_LIST = [
    "None",
    "ISO 9001 (Quality Management)",
    "ISO 14001 (Environmental Management)",
    "ISO 45001 (Occupational Health & Safety)",
    "SA 8000 (Social Accountability)",
    "OHSAS 18001 (Health & Safety)",
    "BIS / ISI Mark",
    "FSSAI (Food Safety)",
    "Fairtrade Certified",
    "Other"
]

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "step_b" not in st.session_state:
    st.session_state.step_b = 1

if "data_b" not in st.session_state:
    st.session_state.data_b = {}

db = st.session_state.data_b
# ─── TIER LOGIC (NEW) ──────────────────────────────────────────
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from business_profile import (
    init_business_profile, show_tier_badge,
    get_business_type, has_board, requires_formal_policies
)

init_business_profile()
show_tier_badge()
# ─── END TIER LOGIC ────────────────────────────────────────────

# Initialize principle data if not present
for code in PRINCIPLES:
    if f"{code}_policy" not in db:
        db[f"{code}_policy"] = "Not yet done"
    if f"{code}_approved" not in db:
        db[f"{code}_approved"] = "No"
    if f"{code}_translated" not in db:
        db[f"{code}_translated"] = "No"
    if f"{code}_value_chain" not in db:
        db[f"{code}_value_chain"] = "No"
    if f"{code}_certs" not in db:
        db[f"{code}_certs"] = ["None"]
    if f"{code}_commitment" not in db:
        db[f"{code}_commitment"] = ""
    if f"{code}_performance" not in db:
        db[f"{code}_performance"] = ""
    if f"{code}_gap_reason" not in db:
        db[f"{code}_gap_reason"] = []

# ─────────────────────────────────────────────────────────────────────────────
# SCORING FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def calc_policy_score():
    score = 0
    max_score = len(PRINCIPLES) * 5

    for code in PRINCIPLES:
        policy = db.get(f"{code}_policy", "Not yet done")
        approved = db.get(f"{code}_approved", "No")
        translated = db.get(f"{code}_translated", "No")
        value_chain = db.get(f"{code}_value_chain", "No")
        commitment = db.get(f"{code}_commitment", "")

        if policy == "Yes":
            score += 2
        elif policy == "In Progress":
            score += 1
        if approved == "Yes" and policy == "Yes":
            score += 1
        if translated == "Yes":
            score += 1
        if value_chain == "Yes":
            score += 0.5
        if commitment:
            score += 0.5

    return min(100, int((score / max_score) * 100))

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def tip(text):
    st.markdown(f'<div class="tip-box">💡 {text}</div>', unsafe_allow_html=True)

def warn(text):
    st.markdown(f'<div class="warn-box">⚠️ {text}</div>', unsafe_allow_html=True)

def go_b(step):
    st.session_state.step_b = step

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 Section B Progress")
    st.progress(st.session_state.step_b / 5)
    st.caption(f"Step {st.session_state.step_b} of 5")

    st.divider()

    score = calc_policy_score()
    st.metric("Policy Readiness Score", f"{score}%")

    if score < 30:
        st.caption("🔴 Low — most policies not yet in place")
    elif score < 60:
        st.caption("🟡 Medium — some policies in place")
    else:
        st.caption("🟢 High — strong policy coverage")

    st.divider()

    # Count policies in place
    policies_yes = sum(1 for c in PRINCIPLES if db.get(f"{c}_policy") == "Yes")
    policies_wip = sum(1 for c in PRINCIPLES if db.get(f"{c}_policy") == "In Progress")
    policies_no  = sum(1 for c in PRINCIPLES if db.get(f"{c}_policy") == "Not yet done")

    st.markdown("**📊 Policy Status**")
    st.caption(f"✅ Confirmed: {policies_yes}/9")
    st.caption(f"🔄 In Progress: {policies_wip}/9")
    st.caption(f"❌ Not yet done: {policies_no}/9")

    st.divider()
    st.markdown("**📖 What is Section B?**")
    st.caption(
        "Section B asks whether your business follows the 9 National Guidelines on "
        "Responsible Business Conduct (NGRBC). You do not need formal written policies "
        "to answer — answer honestly based on how you currently operate."
    )

# ─────────────────────────────────────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("## 📋 BRSR Section B — Management & Process Disclosures")
st.caption("Based on 9 National Guidelines for Responsible Business Conduct (NGRBC) | Simplified for MSMEs")

# ─────────────────────────────────────────────────────────────────────────────
# STEP NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
step_labels = {
    1: "📖 Introduction",
    2: "✅ Principles P1–P5",
    3: "✅ Principles P6–P9",
    4: "🏛️ Governance",
    5: "📊 Summary & Gaps"
}

nav_cols = st.columns(5)
for i, (num, label) in enumerate(step_labels.items()):
    with nav_cols[i]:
        btn_type = "primary" if st.session_state.step_b == num else "secondary"
        if st.button(label, key=f"nav_b_{num}",
                     type=btn_type, use_container_width=True):
            go_b(num)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# REUSABLE PRINCIPLE FORM — must be defined before all steps
# ─────────────────────────────────────────────────────────────────────────────
def principle_form(code):
    info = PRINCIPLES[code]
    with st.container(border=True):
        h1, h2 = st.columns([1, 5])
        with h1:
            st.markdown(f"## {code}")
        with h2:
            st.markdown(f"### {info['title']}")
            st.caption(info["simple"])
        st.caption(f"📌 {info['example']}")
        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            policy_options = ["Yes", "In Progress", "Not yet done"]
            saved_policy = db.get(f"{code}_policy", "Not yet done")
            policy_idx = policy_options.index(saved_policy) if saved_policy in policy_options else 2
            db[f"{code}_policy"] = st.radio(
                f"Do you have a policy or rule for **{info['title']}**?",
                policy_options, index=policy_idx, key=f"radio_policy_{code}",
                help="A 'policy' can be as simple as a written statement or even a consistent practice you follow."
            )
        with col2:
            if db[f"{code}_policy"] == "Yes":
                if has_board():
                    approved_options = ["Yes", "No"]
                    saved_approved = db.get(f"{code}_approved", "No")
                    if saved_approved not in approved_options:
                        saved_approved = "No"
                    db[f"{code}_approved"] = st.radio(
                        "Has the owner / board approved this policy?",
                        approved_options,
                        index=approved_options.index(saved_approved),
                        key=f"radio_approved_{code}",
                        help="For small businesses, 'approved by owner' is sufficient."
                    )
                else:
                    # Sole prop / partnership - no board exists
                    db[f"{code}_approved"] = "Yes"  # owner = approval
                    st.caption(
                        f"✅ Owner-approved (automatic for {get_business_type()})"
                    )
                db[f"{code}_link"] = st.text_input(
                    "Link to policy on your website (optional)",
                    value=db.get(f"{code}_link", ""),
                    key=f"link_{code}",
                    placeholder="e.g. www.yourbusiness.com/ethics-policy"
                )
            elif db[f"{code}_policy"] == "In Progress":
                st.info("Good — you are working on it. Select 'Yes' once formally written and approved.")
            else:
                warn("No policy yet — that's okay. Use the policy generator below to create one in one click.")
        st.markdown("")
        db[f"{code}_translated"] = st.radio(
            "Have you turned this policy into actual day-to-day steps or procedures?",
            ["Yes", "No", "Partially"],
            index=["Yes","No","Partially"].index(db.get(f"{code}_translated","No")) if db.get(f"{code}_translated") in ["Yes","No","Partially"] else 1,
            key=f"radio_trans_{code}", horizontal=True,
            help="For example: a checklist your staff follows, an SOP document, or a training session."
        )
        tip_text = {"Yes": f"Great — your {code} policy is operational.",
                    "Partially": "That's a start. Try to document the remaining steps.",
                    "No": "Recommendation: Even a 1-page checklist counts as a procedure."}
        st.caption(tip_text.get(db[f"{code}_translated"], ""))
        db[f"{code}_value_chain"] = st.radio(
            "Do you expect your suppliers and business partners to follow this too?",
            ["Yes", "No", "Planning to"],
            index=["Yes","No","Planning to"].index(db.get(f"{code}_value_chain","No")) if db.get(f"{code}_value_chain") in ["Yes","No","Planning to"] else 1,
            key=f"radio_vc_{code}", horizontal=True,
            help="This is called 'Value Chain Extension'. Large buyers increasingly check this."
        )
        db[f"{code}_certs"] = st.multiselect(
            "Any certifications or standards related to this principle?",
            CERTIFICATIONS_LIST,
            default=db.get(f"{code}_certs", ["None"]),
            key=f"certs_{code}"
        )
        cc1, cc2 = st.columns(2)
        with cc1:
            db[f"{code}_commitment"] = st.text_area(
                "Any specific targets or commitments for this year? (optional)",
                value=db.get(f"{code}_commitment", ""), key=f"commit_{code}", height=80,
                placeholder=f"e.g. For {code}: Train all staff on this by December 2025."
            )
        with cc2:
            db[f"{code}_performance"] = st.text_area(
                "How did you perform against last year's targets? (optional)",
                value=db.get(f"{code}_performance", ""), key=f"perf_{code}", height=80,
                placeholder="e.g. Completed training for 80% of staff. Remaining 20% planned for Q1."
            )
        if db[f"{code}_policy"] != "Yes":
            st.markdown("")
            if st.button(f"✨ Generate Simple Policy for {code}", key=f"gen_{code}"):
                db[f"{code}_generated"] = info["policy_template"]
        if db.get(f"{code}_generated"):
            st.markdown("")
            st.markdown("**📄 Auto-Generated Policy Statement — Copy and adopt this:**")
            st.markdown(f'<div class="policy-box">{db[f"{code}_generated"]}</div>', unsafe_allow_html=True)
            st.caption("You can copy this, print it, sign it, and it becomes your official policy.")
        st.markdown("")

# ═════════════════════════════════════════════════════════════════════════════
# STEP 1: INTRODUCTION
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.step_b == 1:

    st.header("📖 What is Section B About?")

    st.markdown("""
    Section B asks one simple question: **Does your business follow responsible practices
    across 9 key areas?**

    These 9 areas are called the **NGRBC Principles** (National Guidelines on Responsible
    Business Conduct). The government uses these to check if Indian businesses are operating
    ethically and sustainably.

    **The good news:** You do NOT need expensive consultants or ISO certifications to answer
    this section. Most MSMEs answer honestly — even if some areas are "not yet done."
    """)

    st.info("📌 Answering 'Not yet done' is completely fine and honest. The report just asks "
            "where you are today — not where you need to be tomorrow.")

    st.markdown("---")
    st.markdown("### The 9 Principles — In Plain Language")

    # Show all 9 principles as simple cards
    for code, info in PRINCIPLES.items():
        with st.container(border=True):
            c1, c2 = st.columns([1, 4])
            with c1:
                st.markdown(f"### {code}")
                st.caption(info["title"])
            with c2:
                st.markdown(f"**{info['simple']}**")
                st.caption(info["example"])

    st.markdown("---")
    st.markdown("### How This Section Works")
    tip("We will go through each principle one by one. For each one, we ask: "
        "Do you have a policy? Is it approved? Do your suppliers follow it too? "
        "Then we generate a simple policy statement you can adopt if you don't have one.")

    _, _, c3 = st.columns([1, 2, 1])
    with c3:
        if st.button("Start Section B →", type="primary", use_container_width=True):
            go_b(2)
            st.rerun()

elif st.session_state.step_b == 2:

    st.header("✅ Principles P1 to P5")
    st.write("Answer honestly for each principle. Use the policy generator if you don't have one yet.")

    for code in ["P1", "P2", "P3", "P4", "P5"]:
        principle_form(code)
        st.markdown("")

    _, _, c3 = st.columns([1, 2, 1])
    c_back, _, c_next = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go_b(1); st.rerun()
    with c_next:
        if st.button("Next: P6 to P9 →", type="primary", use_container_width=True):
            go_b(3); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 3: PRINCIPLES P6 — P9
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_b == 3:

    st.header("✅ Principles P6 to P9")
    st.write("Four more principles to go. Almost done with the policy section.")

    for code in ["P6", "P7", "P8", "P9"]:
        principle_form(code)
        st.markdown("")

    c_back, _, c_next = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go_b(2); st.rerun()
    with c_next:
        if st.button("Next: Governance →", type="primary", use_container_width=True):
            go_b(4); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 4: GOVERNANCE
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_b == 4:

    st.header("🏛️ Step 4: Who Is In Charge?")
    st.write("This section is about governance — who oversees sustainability in your business "
             "and how often you review it.")

    # ── BLOCK 1: Responsible Person ───────────────────────────────────────
    with st.container(border=True):
        st.markdown("#### 1️⃣ Person Responsible for BRSR / Sustainability")
        tip("This is the person who owns the responsibility of making sure your business "
            "follows responsible practices. For most MSMEs this is the owner or MD.")

        c1, c2 = st.columns(2)
        with c1:
            db["gov_person_name"] = st.text_input(
                "⚠️ Name of Responsible Person",
                value=db.get("gov_person_name", ""),
                placeholder="e.g. Meet Vaghani"
            )
            db["gov_person_designation"] = st.text_input(
                "⚠️ Their Designation",
                value=db.get("gov_person_designation", ""),
                placeholder="e.g. Managing Director / Owner"
            )
        with c2:
            db["gov_committee"] = st.radio(
                "Do you have a specific committee or person formally assigned "
                "for sustainability decisions?",
                ["Yes", "No — the owner handles it directly",
                 "Planning to appoint one"],
                index=["Yes",
                       "No — the owner handles it directly",
                       "Planning to appoint one"].index(
                    db.get("gov_committee",
                           "No — the owner handles it directly")
                )
            )

        db["gov_director_statement"] = st.text_area(
            "Brief statement from the business owner / director on ESG challenges "
            "and goals (optional but recommended)",
            value=db.get("gov_director_statement", ""),
            height=100,
            placeholder="e.g. As the Managing Director of Vaghani Exports, I am committed to building "
                        "a responsible business that protects our environment, supports our workers, "
                        "and creates value for our community. Our key challenge this year is reducing "
                        "energy costs while maintaining production output."
        )
        tip("This statement appears directly in your BRSR report. Even 2-3 sentences from "
            "the owner adds credibility to the report.")

    # ── BLOCK 2: Review Process ───────────────────────────────────────────
    with st.container(border=True):
        st.markdown("#### 2️⃣ How Often Do You Review These Policies?")
        tip("A 'review' means sitting down once a year (or more often) and asking: "
            "are we still following our policies? What needs to change?")

        c3, c4 = st.columns(2)
        with c3:
            db["gov_review_freq"] = st.selectbox(
                "⚠️ How often do you review your responsible business policies?",
                REVIEW_FREQUENCY,
                index=REVIEW_FREQUENCY.index(
                    db.get("gov_review_freq", "Not reviewed yet")
                )
            )

            db["gov_review_by"] = st.selectbox(
                "Who conducts this review?",
                ["Business Owner / Director",
                 "Senior Management Team",
                 "Board of Directors",
                 "External Consultant / Auditor",
                 "Not reviewed yet"],
                index=0
            )

        with c4:
            if db["gov_review_freq"] == "Not reviewed yet":
                warn("Recommendation: Start with an annual review. Schedule 2 hours "
                     "once a year to review your BRSR policies. This is enough for most MSMEs.")
            else:
                st.success(f"✅ Review frequency: {db['gov_review_freq']} — good practice.")

            db["gov_compliance_review"] = st.radio(
                "Do you review compliance with statutory/legal requirements "
                "related to responsible business?",
                ["Yes", "No", "Informally"],
                horizontal=True,
                index=["Yes", "No", "Informally"].index(
                    db.get("gov_compliance_review", "No")
                ) if db.get("gov_compliance_review") in ["Yes", "No", "Informally"] else 1
            )

    # ── BLOCK 3: External Assessment ─────────────────────────────────────
    with st.container(border=True):
        st.markdown("#### 3️⃣ External Assessment")
        tip("An external assessment means hiring an outside agency — like a CA firm, "
            "consultant, or certification body — to check whether your policies are "
            "actually being followed. This is optional for MSMEs.")

        c5, c6 = st.columns(2)
        with c5:
            db["gov_external"] = st.radio(
                "Has an external agency checked your responsible business policies?",
                ["Yes", "No", "Planning to"],
                index=["Yes", "No", "Planning to"].index(
                    db.get("gov_external", "No")
                ) if db.get("gov_external") in ["Yes", "No", "Planning to"] else 1,
                horizontal=True
            )
        with c6:
            if db["gov_external"] == "Yes":
                db["gov_external_agency"] = st.text_input(
                    "Name of the agency",
                    value=db.get("gov_external_agency", ""),
                    placeholder="e.g. Deloitte / Local CA Firm / SGS India"
                )

        if db["gov_external"] == "No":
            st.caption("That's fine — external assessment is not mandatory for MSMEs. "
                       "Your own internal review is sufficient to start.")

    c_back, _, c_next = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go_b(3); st.rerun()
    with c_next:
        if st.button("Next: Summary & Gaps →", type="primary", use_container_width=True):
            go_b(5); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 5: SUMMARY, GAP ANALYSIS & RECOMMENDATIONS
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_b == 5:

    st.header("📊 Section B — Summary, Gap Analysis & Recommendations")

    # ── POLICY STATUS OVERVIEW TABLE ──────────────────────────────────────
    with st.container(border=True):
        st.markdown("#### Policy Coverage Summary")

        cols = st.columns([1, 2, 1, 1, 1, 2])
        headers = ["Code", "Principle", "Policy?", "Approved?",
                   "Procedures?", "Value Chain?"]
        for col, h in zip(cols, headers):
            col.markdown(f"**{h}**")

        st.markdown("---")

        for code, info in PRINCIPLES.items():
            policy  = db.get(f"{code}_policy", "Not yet done")
            approved = db.get(f"{code}_approved", "No")
            trans   = db.get(f"{code}_translated", "No")
            vc      = db.get(f"{code}_value_chain", "No")

            status_icon = {
                "Yes": "✅", "In Progress": "🔄", "Not yet done": "❌"
            }

            row = st.columns([1, 2, 1, 1, 1, 2])
            row[0].write(f"**{code}**")
            row[1].write(info["title"])
            row[2].write(status_icon.get(policy, "❌"))
            row[3].write("✅" if approved == "Yes" else "—")
            row[4].write("✅" if trans == "Yes" else ("🔄" if trans == "Partially" else "—"))
            row[5].write("✅" if vc == "Yes" else ("🔄" if vc == "Planning to" else "—"))

    # ── ESG SCORE ─────────────────────────────────────────────────────────
    st.markdown("---")
    final_score = calc_policy_score()

    sc1, sc2 = st.columns([1, 2])
    with sc1:
        colour = "green" if final_score >= 60 else "orange" if final_score >= 30 else "red"
        st.markdown(
            f"<h1 style='color:{colour}; text-align:center'>{final_score}%</h1>"
            "<p style='text-align:center; color:gray'>Policy Readiness Score</p>",
            unsafe_allow_html=True
        )
        st.progress(final_score / 100)
    with sc2:
        if final_score >= 60:
            st.success("🎉 Strong policy coverage. Your Section B is looking good.")
        elif final_score >= 30:
            st.warning("📈 Some policies in place. Focus on the gaps identified below.")
        else:
            st.error("📋 Most policies not yet formalised. Use the policy generator "
                     "on each principle to create simple statements quickly.")

    # ── GAP ANALYSIS — Q12 ────────────────────────────────────────────────
    missing = [code for code in PRINCIPLES
               if db.get(f"{code}_policy", "Not yet done") == "Not yet done"]

    if missing:
        st.markdown("---")
        with st.container(border=True):
            st.markdown("#### ⚠️ Gap Analysis — Principles Without Policies")
            st.write(f"You currently have no policy for: "
                     f"**{', '.join(missing)}**")
            st.write("BRSR Question 12 requires you to state **why** these are not covered. "
                     "Select the reason for each:")

            GAP_REASONS = [
                "Not material to our specific business",
                "We don't have the financial resources yet",
                "We don't have technical knowledge yet",
                "Planned to be done next financial year",
                "Other reason"
            ]

            for code in missing:
                with st.expander(f"❌ {code} — {PRINCIPLES[code]['title']}"):
                    db[f"{code}_gap_reason"] = st.multiselect(
                        f"Why is there no policy for {code}?",
                        GAP_REASONS,
                        default=db.get(f"{code}_gap_reason", ["Planned to be done next financial year"]),
                        key=f"gap_{code}"
                    )
                    if "Other reason" in db.get(f"{code}_gap_reason", []):
                        db[f"{code}_gap_other"] = st.text_input(
                            "Describe other reason:",
                            value=db.get(f"{code}_gap_other", ""),
                            key=f"gap_other_{code}",
                            placeholder="e.g. Not applicable to our business model"
                        )

                    # Show policy generator here too
                    if st.button(f"✨ Generate Policy for {code}",
                                 key=f"gen5_{code}"):
                        db[f"{code}_generated"] = PRINCIPLES[code]["policy_template"]
                        st.success("Policy generated! Go back to this principle to copy it.")
    else:
        st.success("✅ All 9 principles have policies in place!")

    # ── SMART RECOMMENDATIONS ─────────────────────────────────────────────
    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### 💡 Smart Recommendations")

        recs_shown = 0

        if db.get("P3_policy") != "Yes":
            st.warning("👷 **P3 (Employee Wellbeing)** is not yet covered. "
                       "This is the most commonly checked principle by banks and buyers. "
                       "A simple written safety policy takes 30 minutes to create.")
            recs_shown += 1

        if db.get("P6_policy") != "Yes":
            st.warning("🌿 **P6 (Environment)** is not yet covered. "
                       "If you are a manufacturer, this is mandatory to address. "
                       "Use the generator to create a simple environment policy.")
            recs_shown += 1

        if db.get("P1_policy") != "Yes":
            st.warning("⚖️ **P1 (Ethics)** is not covered. "
                       "This is the foundation of BRSR. Start here first.")
            recs_shown += 1

        any_no_procedure = any(
            db.get(f"{c}_translated") == "No"
            for c in PRINCIPLES
            if db.get(f"{c}_policy") == "Yes"
        )
        if any_no_procedure:
            st.info("📋 You have policies but no procedures for some principles. "
                    "Convert at least your P1, P3, and P6 policies into simple "
                    "step-by-step checklists for your staff.")
            recs_shown += 1

        if db.get("gov_review_freq") == "Not reviewed yet":
            st.info("🗓️ You have no review process yet. Schedule a 2-hour annual "
                    "review meeting to go through your BRSR policies. "
                    "This alone significantly improves your score.")
            recs_shown += 1

        any_no_vc = any(
            db.get(f"{c}_value_chain") == "No"
            for c in ["P1", "P3", "P5", "P6"]
        )
        if any_no_vc:
            st.info("🔗 Consider extending your key policies (P1, P3, P5, P6) "
                    "to your main suppliers. Large buyers increasingly audit "
                    "supplier ESG practices, especially for export businesses.")
            recs_shown += 1

        if recs_shown == 0:
            st.success("🎯 No major gaps detected. Your Section B looks comprehensive!")

    # ── QUICK POLICY PACK ─────────────────────────────────────────────────
    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### 📄 Quick Policy Pack Generator")
        st.write("Generate policy statements for all principles you haven't covered yet "
                 "in one click.")

        if st.button("✨ Generate All Missing Policies", type="primary"):
            generated_count = 0
            for code in PRINCIPLES:
                if db.get(f"{code}_policy") != "Yes":
                    db[f"{code}_generated"] = PRINCIPLES[code]["policy_template"]
                    generated_count += 1
            if generated_count > 0:
                st.success(f"✅ Generated {generated_count} policy statements! "
                           "Go back to each principle to copy and adopt them.")
                st.balloons()
            else:
                st.info("All principles already have policies in place.")

        # Show any generated policies
        generated = [(code, db[f"{code}_generated"])
                     for code in PRINCIPLES
                     if db.get(f"{code}_generated")]

        if generated:
            st.markdown("**Your generated policies:**")
            for code, text in generated:
                with st.expander(f"📋 {code} — {PRINCIPLES[code]['title']}"):
                    st.markdown(
                        f'<div class="policy-box">{text}</div>',
                        unsafe_allow_html=True
                    )
                    st.caption("Copy this text, print it, sign it, and file it as your official policy.")

    # ── SAVE & PROCEED ────────────────────────────────────────────────────
    st.markdown("---")
    cf1, cf2, cf3 = st.columns([1, 2, 1])
    with cf2:
        if st.button("💾 Save Section B & Proceed to Section C →",
                     type="primary", use_container_width=True):
            st.balloons()
            st.success("✅ Section B saved! "
                       "Next: Section C — Environmental Disclosures (Energy, Water, Waste).")

    c_back, _, _ = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back to Governance", use_container_width=True):
            go_b(4); st.rerun()