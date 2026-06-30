import streamlit as st
import re
from pdf_generator import generate_brsr_pdf


def _trigger_pdf_download(data: dict, esg_score: int):
    """Redirect users to the dedicated Generate Report page."""
    st.info(
        "👉 **Section A is saved!** To generate the full BRSR PDF with all sections "
        "(A, B, and 9 Principles), please use the **'9 Generate Report'** page in "
        "the sidebar. That page pulls data from all sections into one unified "
        "BRSR-audit-ready report."
    )
    st.success(
        "✅ Your Section A data is saved. Continue filling Section B → "
        "9 Principles → then generate the full report."
    )


# ─────────────────────────────────────────────────────────────────────────────

# PAGE CONFIG

# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(

    page_title="BRSR Tool for MSMEs",

    page_icon="🌱",

    layout="centered"

)

from sidebar_footer import render_whatsapp_fab, render_pagehead
render_whatsapp_fab()



# ─────────────────────────────────────────────────────────────────────────────

# CUSTOM CSS

# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""

<style>

    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    .step-btn button { border-radius: 50px !important; font-size: 13px !important; }

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

    .section-card {

        background: #ffffff;

        border: 1px solid #e8eaf0;

        border-radius: 12px;

        padding: 20px 24px;

        margin-bottom: 16px;

    }

</style>

""", unsafe_allow_html=True)



# ─────────────────────────────────────────────────────────────────────────────

# SESSION STATE - stores all user data across steps

# ─────────────────────────────────────────────────────────────────────────────

if "step" not in st.session_state:

    st.session_state.step = 1



if "data" not in st.session_state:

    st.session_state.data = {}



d = st.session_state.data  # shorthand
# ─── TIER LOGIC (NEW) ──────────────────────────────────────────
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from business_profile import (
    init_business_profile, show_tier_badge, show_sidebar_logo,
    get_business_type, is_sole_prop, is_partnership,
    has_board, is_listed
)
init_business_profile()
show_sidebar_logo()
show_tier_badge()

# Auto-sync business_type from Home with ownership field in Section A
TIER_TO_OWNERSHIP = {
    "Sole Proprietorship": "Sole Proprietorship",
    "Partnership / LLP": "Partnership Firm",
    "Private Limited": "Private Limited Company",
    "Public Listed": "Public Limited Company"
}
if not d.get("ownership"):
    d["ownership"] = TIER_TO_OWNERSHIP.get(get_business_type(), "Sole Proprietorship")

show_tier_badge()
# ─── END TIER LOGIC ────────────────────────────────────────────



# ─────────────────────────────────────────────────────────────────────────────

# HELPER FUNCTIONS

# ─────────────────────────────────────────────────────────────────────────────

def tip(text):

    st.markdown(f'<div class="tip-box">💡 {text}</div>', unsafe_allow_html=True)



def warn(text):

    st.markdown(f'<div class="warn-box">⚠️ {text}</div>', unsafe_allow_html=True)



def card_start():

    st.markdown('<div class="section-card">', unsafe_allow_html=True)



def card_end():

    st.markdown('</div>', unsafe_allow_html=True)



def go(step):

    st.session_state.step = step



# ─────────────────────────────────────────────────────────────────────────────

# ESG SCORE CALCULATOR

# ─────────────────────────────────────────────────────────────────────────────

def calc_esg_score():

    score = 0

    if d.get("company_name"): score += 10

    if d.get("email"): score += 5

    if d.get("address"): score += 5

    if d.get("activities"): score += 10

    if d.get("products"): score += 10

    if d.get("export_pct", 0) > 0: score += 5

    if d.get("total_perm_emp", 0) > 0: score += 10

    female_pct = (d.get("perm_emp_female", 0) / d.get("total_perm_emp", 1)) * 100 if d.get("total_perm_emp", 0) > 0 else 0

    if female_pct >= 10: score += 10

    if female_pct >= 30: score += 5

    if d.get("board_female", 0) > 0: score += 10

    if d.get("has_grievance"): score += 10

    if d.get("issues"): score += 10

    return min(score, 100)



# ─────────────────────────────────────────────────────────────────────────────

# MSME CLASSIFICATION

# ─────────────────────────────────────────────────────────────────────────────

def get_msme_class(turnover_lakhs):

    # Turnover-based MSME limits (Govt of India, 2020): Micro ≤ ₹5 Cr,
    # Small ≤ ₹50 Cr, Medium ≤ ₹250 Cr. Above ₹250 Cr is not an MSME.
    # (Full MSME status also depends on plant & machinery investment.)

    if turnover_lakhs == 0:

        return "-"

    if turnover_lakhs <= 500:

        return "🔵 Micro Enterprise"

    elif turnover_lakhs <= 5000:

        return "🟡 Small Enterprise"

    elif turnover_lakhs <= 25000:

        return "🟠 Medium Enterprise"

    else:

        return "🔴 Large Enterprise (above MSME turnover limit)"



# ─────────────────────────────────────────────────────────────────────────────

# SIDEBAR

# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:

    st.markdown("### 🌱 BRSR Report Progress")

    st.progress(st.session_state.step / 5)

    st.caption(f"Step {st.session_state.step} of 5")



    st.divider()



    esg = calc_esg_score()

    st.metric("ESG Readiness Score", f"{esg}%",

              delta="Keep filling to improve" if esg < 100 else "Excellent!")



    if esg < 40:

        st.caption("🔴 Low - fill more sections")

    elif esg < 70:

        st.caption("🟡 Medium - good progress")

    else:

        st.caption("🟢 High - looking great!")



    st.divider()



    st.markdown("**📋 Your Business Summary**")

    st.caption(f"Name: {d.get('company_name', '-')}")

    st.caption(f"Type: {d.get('ownership', '-')}")

    st.caption(f"MSME Class: {get_msme_class(d.get('turnover_lakhs', 0))}")

    st.caption(f"Employees: {d.get('total_perm_emp', 0)}")

    st.caption(f"Export %: {d.get('export_pct', 0)}%")



    st.divider()



    st.markdown("**📖 What is BRSR?**")

    st.caption(

        "BRSR = Business Responsibility & Sustainability Reporting. "

        "It's a report that shows how responsibly your business operates - "

        "for the environment, your workers, and society. "

        "Banks, buyers, and partners increasingly ask for this."

    )



# ─────────────────────────────────────────────────────────────────────────────

# MAIN HEADER

# ─────────────────────────────────────────────────────────────────────────────

render_pagehead(
    "Step 1 of 9 · Section A",
    "Company Profile",
    "Tell us about your business — identity, finances, locations, and your "
    "people. This is the foundation of your BRSR report."
)



# ─────────────────────────────────────────────────────────────────────────────

# STEP NAVIGATION BAR

# ─────────────────────────────────────────────────────────────────────────────

steps = {

    1: "🏢 Your Business",

    2: "🏭 What You Sell",

    3: "🗺️ Where You Operate",

    4: "👥 Your People",

    5: "⚖️ Governance & Risks"

}



cols = st.columns(5)

for i, (num, label) in enumerate(steps.items()):

    with cols[i]:

        is_active = st.session_state.step == num

        btn_style = "primary" if is_active else "secondary"

        if st.button(label, key=f"nav_{num}", type=btn_style, use_container_width=True):

            go(num)



st.markdown("---")



# ═════════════════════════════════════════════════════════════════════════════

# STEP 1: YOUR BUSINESS

# ═════════════════════════════════════════════════════════════════════════════

if st.session_state.step == 1:



    st.header("🏢 Step 1: Tell Us About Your Business")

    st.write("This is basic information about your company. Just like filling a bank form.")



    # ── BLOCK 1: Company Identity ──────────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### 1️⃣ Company Identity")



        c1, c2 = st.columns(2)

        with c1:

            d["company_name"] = st.text_input(

                "⚠️ What is your company's full name?",

                value=d.get("company_name", ""),

                placeholder="e.g. Vaghani Foods Private Limited"

            )

            d["ownership"] = st.selectbox(

                "⚠️ What type of business do you run?",

                ["Sole Proprietorship", "Partnership Firm", "LLP (Limited Liability Partnership)",

                 "Private Limited Company", "Public Limited Company", "Other"],

                index=["Sole Proprietorship", "Partnership Firm", "LLP (Limited Liability Partnership)",

                       "Private Limited Company", "Public Limited Company", "Other"].index(d.get("ownership", "Sole Proprietorship"))

            )

            if d["ownership"] == "Other":

                d["ownership_other"] = st.text_input("Please describe your business type:",

                                                      placeholder="e.g. Hindu Undivided Family (HUF)")



        with c2:

            d["cin"] = st.text_input(

                "CIN Number (only if you are a Private/Public Limited Company)",

                value=d.get("cin", ""),

                placeholder="e.g. U74999GJ2020PTC114567",

                help="CIN is given by MCA when you register a company. Proprietorships and partnerships do NOT have a CIN."

            )



            # Real-time CIN validation

            if d["cin"]:

                if re.match(r'^[LU][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$', d["cin"]):

                    st.success("✅ Valid CIN format")

                else:

                    st.error("❌ Invalid CIN. Format should be like: U74999GJ2020PTC114567")



            d["year_started"] = st.number_input(

                "⚠️ Which year did you start your business?",

                min_value=1900, max_value=2026,

                value=d.get("year_started", 2015)

            )

            d["pan"] = st.text_input(

                "PAN of the entity",

                value=d.get("pan", ""),

                placeholder="e.g. AABCU9603R",

                help="The 10-character PAN issued to your business by the Income Tax Department. Required in SEBI BRSR Section A."

            ).strip().upper()

            if d["pan"]:

                if re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', d["pan"]):

                    st.success("✅ Valid PAN format")

                else:

                    st.error("❌ Invalid PAN. Format should be like: AABCU9603R")

            d["gstin"] = st.text_input(

                "GSTIN (if registered under GST)",

                value=d.get("gstin", ""),

                placeholder="e.g. 24AABCU9603R1ZM",

                help="The 15-character GST Identification Number. Leave blank if your business is not GST-registered."

            ).strip().upper()

            if d["gstin"]:

                if re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][0-9A-Z]Z[0-9A-Z]$', d["gstin"]):

                    st.success("✅ Valid GSTIN format")

                else:

                    st.error("❌ Invalid GSTIN. It should be 15 characters, like: 24AABCU9603R1ZM")



        tip("Not sure about CIN? If you registered your company with the MCA (Ministry of Corporate Affairs), you have a CIN. Sole proprietors and partnership firms do NOT have one - leave it blank.")



    # ── BLOCK 2: Financial Year & Turnover ────────────────────────────────

    with st.container(border=True):

        st.markdown("#### 2️⃣ Financial Details")



        c3, c4 = st.columns(2)

        with c3:

            d["financial_year"] = st.selectbox(

                "⚠️ Which financial year is this report for?",

                ["2025-26", "2024-25", "2023-24", "2022-23"],

                index=["2025-26", "2024-25", "2023-24", "2022-23"].index(d.get("financial_year", "2025-26"))

            )



            d["turnover_lakhs"] = st.number_input(

                "⚠️ What is your annual turnover? (in ₹ Lakhs)",

                min_value=0, max_value=100000,

                value=d.get("turnover_lakhs", 0),

                help="Annual turnover = total money your business received from sales in this financial year. 1 Crore = 100 Lakhs."

            )



        with c4:

            # MSME Auto Classification

            msme_class = get_msme_class(d["turnover_lakhs"])

            st.markdown("**Your MSME Classification:**")

            st.info(f"{msme_class}")



            d["listed"] = st.radio(

                "Is your company listed on a stock exchange (BSE/NSE)?",

                ["No - we are not listed (most MSMEs)", "Yes - we are listed"],

                index=0 if d.get("listed", "No - we are not listed (most MSMEs)") == "No - we are not listed (most MSMEs)" else 1

            )



        if d["listed"] == "Yes - we are listed":

            c5, c6 = st.columns(2)

            with c5:

                d["stock_exchange"] = st.multiselect("Which stock exchange(s)?",

                                                      ["BSE", "NSE", "Both"])

            with c6:

                d["paid_up_capital"] = st.text_input("Paid-up Capital (₹)",

                                                      placeholder="e.g. 50,00,000")



        tip("MSME Classification (as per Govt of India): Micro = turnover up to ₹5 Crore | Small = up to ₹50 Crore | Medium = up to ₹250 Crore. Above ₹250 Crore is not an MSME. Note: official status also depends on your investment in plant & machinery — this estimate uses turnover only.")



    # ── BLOCK 3: Address ──────────────────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### 3️⃣ Business Address")



        d["address"] = st.text_area(

            "⚠️ Registered Office Address",

            value=d.get("address", ""),

            placeholder="e.g. Plot No. 12, GIDC Industrial Area, Bhavnagar, Gujarat - 364001",

            height=80

        )



        same_addr = st.checkbox(

            "My operating address is the same as registered address",

            value=d.get("same_addr", True)

        )

        d["same_addr"] = same_addr



        if not same_addr:

            d["corporate_address"] = st.text_area(

                "Operating / Corporate Address",

                value=d.get("corporate_address", ""),

                placeholder="e.g. Office 5, Navjivan Complex, Ahmedabad - 380001",

                height=80

            )

        else:

            d["corporate_address"] = d["address"]



        c7, c8, c9 = st.columns(3)

        with c7:

            d["email"] = st.text_input(

                "⚠️ Business Email",

                value=d.get("email", ""),

                placeholder="e.g. info@yourbusiness.com"

            )

            if d["email"] and not re.match(

                    r'^[^@\s]+@[^@\s]+\.[^@\s]+$', d["email"].strip()):

                st.error("Please enter a valid email address, e.g. info@yourbusiness.com")



        with c8:

            d["phone"] = st.text_input(

                "⚠️ Phone Number",

                value=d.get("phone", ""),

                placeholder="e.g. +91 9409417490"

            )



        with c9:

            d["website"] = st.text_input(

                "Website (optional)",

                value=d.get("website", ""),

                placeholder="e.g. www.yourbusiness.com"

            )



    # ── BLOCK 4: Contact Person ───────────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### 4️⃣ Who Should Be Contacted For BRSR Questions?")

        tip("This is the person a bank officer, auditor, or government official should call if they have questions about this report. Usually the owner or a senior manager.")



        c10, c11 = st.columns(2)

        with c10:

            d["contact_name"] = st.text_input(

                "⚠️ Contact Person's Name",

                value=d.get("contact_name", ""),

                placeholder="e.g. Steve Thomas"

            )

            d["contact_designation"] = st.text_input(

                "⚠️ Their Job Title",

                value=d.get("contact_designation", ""),

                placeholder="e.g. Owner / Managing Director / CFO"

            )



        with c11:

            d["contact_email"] = st.text_input(

                "Contact Person's Email",

                value=d.get("contact_email", ""),

                placeholder="e.g. meet@yourbusiness.com"

            )

            if d["contact_email"] and not re.match(

                    r'^[^@\s]+@[^@\s]+\.[^@\s]+$', d["contact_email"].strip()):

                st.error("Please enter a valid email address.")

            d["contact_phone"] = st.text_input(

                "Contact Person's Phone",

                value=d.get("contact_phone", ""),

                placeholder="e.g. +xx +xxxxxxxxxx"

            )



    # ── BLOCK 5: Reporting Boundary ───────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### 5️⃣ Does This Report Cover Just Your Business, or Other Companies Too?")

        tip("'Standalone' means this report is only for your main company. 'Consolidated' means it covers your company AND any other companies you own. Almost all MSMEs should choose Standalone.")



        d["reporting_boundary"] = st.radio(

            "⚠️ This BRSR report covers:",

            [

                "Standalone - Only my main business (recommended for most MSMEs)",

                "Consolidated - My business AND other companies I own"

            ],

            index=0 if "Consolidated" not in d.get("reporting_boundary", "") else 1

        )



    # ── NAVIGATION ────────────────────────────────────────────────────────

    st.markdown("")

    c_nav1, c_nav2 = st.columns([3, 1])

    with c_nav2:

        if st.button("Next: What You Sell →", type="primary", use_container_width=True):

            if not d.get("company_name"):

                st.error("Please enter your company name before continuing.")

            elif not d.get("address"):

                st.error("Please enter your registered address before continuing.")

            else:

                go(2)

                st.rerun()



# ═════════════════════════════════════════════════════════════════════════════

# STEP 2: WHAT YOU SELL

# ═════════════════════════════════════════════════════════════════════════════

elif st.session_state.step == 2:



    st.header("🏭 Step 2: What Does Your Business Sell?")

    st.write("Describe your main products or services. Focus on what earns you 90% of your revenue.")



    # ── BLOCK 1: Business Activities ──────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### 6️⃣ Your Main Business Activities")

        tip("A 'business activity' is what your business DOES - like Manufacturing, Trading, Service, or Farming. Most MSMEs have just 1-2 activities.")



        st.caption("**Example:** A garment manufacturer might list: Activity 1 = Manufacturing → Garment Manufacturing (95% of revenue)")



        num_act = st.number_input(

            "How many main activities does your business have?",

            min_value=1, max_value=5, value=d.get("num_activities", 1)

        )

        d["num_activities"] = int(num_act)



        activities = d.get("activities", [{}] * int(num_act))

        if len(activities) < int(num_act):

            activities += [{}] * (int(num_act) - len(activities))



        activity_options = [

            "Manufacturing", "Trading / Wholesale", "Retail", "Export / Import",

            "Food Processing", "Textile & Apparel", "Construction",

            "IT / Technology Services", "Financial Services", "Healthcare",

            "Agriculture / Farming", "Logistics / Transport", "Education",

            "Hospitality / Tourism", "Others"

        ]



        total_act_pct = 0

        for i in range(int(num_act)):

            st.markdown(f"**Activity {i+1}**")

            ca1, ca2, ca3 = st.columns([2, 2, 1])

            with ca1:

                main_act = st.selectbox(

                    "Type of Activity",

                    activity_options,

                    key=f"main_act_{i}",

                    index=activity_options.index(activities[i].get("main", "Manufacturing")) if activities[i].get("main") in activity_options else 0

                )

                if main_act == "Others":

                    main_act = st.text_input("Describe your activity:", key=f"main_act_other_{i}",

                                             placeholder="e.g. Handicraft Making")

            with ca2:

                sub_act = st.text_input(

                    "More Specific Description",

                    value=activities[i].get("sub", ""),

                    key=f"sub_act_{i}",

                    placeholder="e.g. Freeze-dried Indian Curry Manufacturing"

                )

            with ca3:

                act_pct = st.number_input(

                    "% Revenue",

                    min_value=0, max_value=100,

                    value=activities[i].get("pct", 100),

                    key=f"act_pct_{i}"

                )

            activities[i] = {"main": main_act, "sub": sub_act, "pct": act_pct}

            total_act_pct += act_pct



        d["activities"] = activities



        if int(num_act) > 1:

            if total_act_pct != 100:

                warn(f"Your activity percentages add up to {total_act_pct}%. They should add up to 100%.")

            else:

                st.success("✅ Percentages add up to 100%")



    # ── BLOCK 2: Products & Services ──────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### 7️⃣ Your Main Products or Services")

        tip("List the specific products or services you sell. A food company might list: 1) Freeze-dried Curry, 2) Ready-to-eat Dal Makhani, 3) Packaged Biryani")



        num_prod = st.number_input(

            "How many main products/services do you sell?",

            min_value=1, max_value=20, value=d.get("num_products", 1)

        )

        d["num_products"] = int(num_prod)



        products = d.get("products", [{}] * int(num_prod))

        if len(products) < int(num_prod):

            products += [{}] * (int(num_prod) - len(products))



        total_prod_pct = 0

        for i in range(int(num_prod)):

            st.markdown(f"**Product / Service {i+1}**")

            cp1, cp2, cp3 = st.columns([3, 1, 1])

            with cp1:

                prod_name = st.text_input(

                    "Product or Service Name",

                    value=products[i].get("name", ""),

                    key=f"prod_{i}",

                    placeholder="e.g. Freeze-dried Palak Paneer"

                )

            with cp2:

                nic = st.text_input(

                    "NIC Code (optional)",

                    value=products[i].get("nic", ""),

                    key=f"nic_{i}",

                    placeholder="e.g. 10790",

                    help="NIC code is a government industry classification number. Ask your CA or search 'NIC code [your product]' on Google."

                )

            with cp3:

                prod_pct = st.number_input(

                    "% Revenue",

                    min_value=0, max_value=100,

                    value=products[i].get("pct", 100),

                    key=f"prod_pct_{i}"

                )

            products[i] = {"name": prod_name, "nic": nic, "pct": prod_pct}

            total_prod_pct += prod_pct



        d["products"] = products



        if int(num_prod) > 1:

            if total_prod_pct != 100:

                warn(f"Your product percentages add up to {total_prod_pct}%. They should add up to 100%.")

            else:

                st.success("✅ Percentages add up to 100%")



        st.caption("💡 NIC Code examples: Food products = 1079 | Textiles = 1311 | Chemicals = 2011 | Machinery = 2811 | Construction = 4100 | Trading = 4690")



    # ── NAVIGATION ────────────────────────────────────────────────────────

    st.markdown("")

    cn1, cn2, cn3 = st.columns([1, 2, 1])

    with cn1:

        if st.button("← Back", use_container_width=True):

            go(1); st.rerun()

    with cn3:

        if st.button("Next: Where You Operate →", type="primary", use_container_width=True):

            go(3); st.rerun()



# ═════════════════════════════════════════════════════════════════════════════

# STEP 3: WHERE YOU OPERATE

# ═════════════════════════════════════════════════════════════════════════════

elif st.session_state.step == 3:



    st.header("🗺️ Step 3: Where Does Your Business Operate?")

    st.write("Tell us about your factories, offices, and the markets you sell in.")



    # ── BLOCK 1: Locations ────────────────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### 8️⃣ Your Business Locations in India")

        tip("Count every physical location. A factory where you make products = 'plant'. An office where your team works = 'office'.")



        c1, c2 = st.columns(2)

        with c1:

            d["num_plants"] = st.number_input(

                "⚠️ Number of factories / manufacturing units in India",

                min_value=0, max_value=500, value=d.get("num_plants", 1),

                help="Any place where you physically make or produce your product."

            )

            d["num_offices"] = st.number_input(

                "⚠️ Number of offices in India",

                min_value=0, max_value=500, value=d.get("num_offices", 1),

                help="Registered office, branch office, sales office, warehouse etc."

            )



        with c2:

            d["num_intl_plants"] = st.number_input(

                "Factories outside India (if any)",

                min_value=0, max_value=100, value=d.get("num_intl_plants", 0)

            )

            d["num_intl_offices"] = st.number_input(

                "Offices outside India (if any)",

                min_value=0, max_value=100, value=d.get("num_intl_offices", 0)

            )



    # ── BLOCK 2: Markets ──────────────────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### 9️⃣ Which Markets Do You Sell In?")



        c3, c4 = st.columns(2)

        with c3:

            d["num_states"] = st.number_input(

                "⚠️ How many Indian states do you sell in?",

                min_value=1, max_value=28, value=d.get("num_states", 1),

                help="Count every state where you have buyers, distributors, or dealers."

            )

        with c4:

            d["num_countries"] = st.number_input(

                "How many countries do you export to? (put 0 if no exports)",

                min_value=0, max_value=200, value=d.get("num_countries", 0)

            )



        d["export_pct"] = st.slider(

            "⚠️ What % of your total revenue comes from exports (sales outside India)?",

            min_value=0, max_value=100, value=d.get("export_pct", 0), step=1

        )



        if d["export_pct"] > 0:

            st.success(f"✅ You export {d['export_pct']}% of your revenue - this is a positive ESG indicator for global buyers.")



        st.markdown("**⚠️ Who are your main customers? (select all that apply)**")

        customer_options = [

            "Individual consumers / end users (B2C - e.g. people buying from your shop)",

            "Other businesses / companies (B2B - e.g. selling to factories or stores)",

            "Government / PSU",

            "Exporters or Trading Houses",

            "Retailers / Distributors / Wholesalers",

            "Online platforms (Amazon, Flipkart, etc.)",

            "Others"

        ]



        d["customer_types"] = st.multiselect(

            "Select all types of customers you sell to:",

            customer_options,

            default=d.get("customer_types", [])

        )



        if "Others" in str(d.get("customer_types", [])):

            d["customer_other"] = st.text_input(

                "You selected 'Others' - please describe:",

                value=d.get("customer_other", ""),

                placeholder="e.g. NGOs, Hospitals, Cooperatives"

            )



    # ── NAVIGATION ────────────────────────────────────────────────────────

    st.markdown("")

    cn1, cn2, cn3 = st.columns([1, 2, 1])

    with cn1:

        if st.button("← Back", use_container_width=True):

            go(2); st.rerun()

    with cn3:

        if st.button("Next: Your People →", type="primary", use_container_width=True):

            go(4); st.rerun()



# ═════════════════════════════════════════════════════════════════════════════

# STEP 4: YOUR PEOPLE

# ═════════════════════════════════════════════════════════════════════════════

elif st.session_state.step == 4:



    st.header("👥 Step 4: Your Employees & Workers")

    st.write("This section is about the people who work for you.")



    st.info("""

    📌 **Quick Explanation of Terms:**

    - **Employees** = People doing office, management, or administrative work (on your payroll)

    - **Workers** = People doing physical / factory / production / field work (on your payroll)

    - **Permanent** = Regular, full-time staff

    - **Contract / Temporary** = People hired through an agency or on short-term basis

    """)



    # ── BLOCK 1: Permanent Employees ─────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### 🔟 Permanent Employees (Office / Management Staff)")



        c1, c2, c3, c4 = st.columns(4)

        with c1:

            d["total_perm_emp"] = st.number_input("Total", min_value=0, value=d.get("total_perm_emp", 5), key="tpe")

        with c2:

            d["perm_emp_male"] = st.number_input("Male", min_value=0, value=d.get("perm_emp_male", 4), key="pem")

        with c3:

            d["perm_emp_female"] = st.number_input("Female", min_value=0, value=d.get("perm_emp_female", 1), key="pef")

        with c4:

            if d["total_perm_emp"] > 0:

                div = round((d["perm_emp_female"] / d["total_perm_emp"]) * 100, 1)

                st.metric("Gender Diversity", f"{div}%")



        if d["perm_emp_male"] + d["perm_emp_female"] != d["total_perm_emp"] and d["total_perm_emp"] > 0:

            st.error(f"❌ Male ({d['perm_emp_male']}) + Female ({d['perm_emp_female']}) = {d['perm_emp_male'] + d['perm_emp_female']}, but Total = {d['total_perm_emp']}. Please fix this.")



    # ── BLOCK 2: Contract Employees ───────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### Contract / Temporary Employees")

        tip("These are office/admin staff hired through a placement agency or on a short-term contract. Not on your permanent payroll.")



        c5, c6, c7 = st.columns(3)

        with c5:

            d["total_temp_emp"] = st.number_input("Total", min_value=0, value=d.get("total_temp_emp", 0), key="tte")

        with c6:

            d["temp_emp_male"] = st.number_input("Male", min_value=0, value=d.get("temp_emp_male", 0), key="tem")

        with c7:

            d["temp_emp_female"] = st.number_input("Female", min_value=0, value=d.get("temp_emp_female", 0), key="tef")



        if d["temp_emp_male"] + d["temp_emp_female"] != d["total_temp_emp"] and d["total_temp_emp"] > 0:

            st.error(f"❌ Male + Female ≠ Total. Please check.")



    # ── BLOCK 3: Permanent Workers ────────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### Permanent Workers (Factory / Shop Floor / Field Staff)")

        tip("Workers are people who do physical work - in your factory, warehouse, farm, or at customer sites. They are different from office employees.")



        c8, c9, c10 = st.columns(3)

        with c8:

            d["total_perm_wkr"] = st.number_input("Total", min_value=0, value=d.get("total_perm_wkr", 0), key="tpw")

        with c9:

            d["perm_wkr_male"] = st.number_input("Male", min_value=0, value=d.get("perm_wkr_male", 0), key="pwm")

        with c10:

            d["perm_wkr_female"] = st.number_input("Female", min_value=0, value=d.get("perm_wkr_female", 0), key="pwf")



        if d["perm_wkr_male"] + d["perm_wkr_female"] != d["total_perm_wkr"] and d["total_perm_wkr"] > 0:

            st.error(f"❌ Male + Female ≠ Total. Please check.")



    # ── BLOCK 4: Contract Workers ─────────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### Contract / Temporary Workers")



        c11, c12, c13 = st.columns(3)

        with c11:

            d["total_temp_wkr"] = st.number_input("Total", min_value=0, value=d.get("total_temp_wkr", 0), key="ttw")

        with c12:

            d["temp_wkr_male"] = st.number_input("Male", min_value=0, value=d.get("temp_wkr_male", 0), key="twm")

        with c13:

            d["temp_wkr_female"] = st.number_input("Female", min_value=0, value=d.get("temp_wkr_female", 0), key="twf")



    # ── BLOCK 5: Differently Abled ────────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### Differently Abled Staff")

        tip("Include anyone with a physical or mental disability. Put 0 if you have none. This is not a negative - it's just information.")



        c14, c15 = st.columns(2)

        with c14:

            d["diff_emp"] = st.number_input("Differently Abled Employees", min_value=0, value=d.get("diff_emp", 0))

        with c15:

            d["diff_wkr"] = st.number_input("Differently Abled Workers", min_value=0, value=d.get("diff_wkr", 0))



    # ── BLOCK 6: Leadership & Women ───────────────────────────────────────

    # ── BLOCK 6: Leadership & Women (tier-gated) ─────────────────────────
    if has_board():
    
        # Reset board/kmp defaults if they were zeroed out for non-board tier
        if d.get("board_total", 0) < 1:
            d["board_total"] = 2
        if d.get("kmp_total", 0) < 1:
            d["kmp_total"] = 1
        with st.container(border=True):
            st.markdown("#### Women in Leadership")
            tip("'Board of Directors' = owners/directors of the company registered with MCA. 'KMP' = Key Management Personnel - senior managers like CEO, CFO, COO, General Manager etc.")

            c16, c17 = st.columns(2)
            with c16:
                st.markdown("**Board of Directors**")
                d["board_total"] = st.number_input("Total Directors", min_value=1, value=d.get("board_total", 2), key="bt")
                d["board_female"] = st.number_input("Women Directors", min_value=0, value=d.get("board_female", 0), key="bf")
                if d["board_female"] == 0:
                    warn("No women on the board. Many banks and investors now look for at least one woman director.")

            with c17:
                st.markdown("**Key Management Personnel (KMP)**")
                d["kmp_total"] = st.number_input("Total KMPs", min_value=0, value=d.get("kmp_total", 1), key="kt")
                d["kmp_female"] = st.number_input("Women KMPs", min_value=0, value=d.get("kmp_female", 0), key="kf")
    else:
        # Set zero values for sole prop / partnership so score calc doesn't break
        d["board_total"] = 0
        d["board_female"] = 0
        d["kmp_total"] = 0
        d["kmp_female"] = 0
        with st.container(border=True):
            st.info(
                f"📌 **Board & KMP questions skipped** — not applicable for "
                f"**{get_business_type()}**. This is correct for most small businesses."
            )


    # ── BLOCK 7: Employee Turnover ────────────────────────────────────────

    with st.container(border=True):

        st.markdown("#### Staff Turnover Rate (Last 3 Years)")

        tip("Turnover rate = what % of your staff left and were replaced each year. High turnover (above 30%) is a red flag for banks and investors. Low turnover shows a stable, well-run business.")



        c18, c19, c20 = st.columns(3)

        with c18:

            d["turnover_fy1"] = st.number_input("Turnover % this year (FY 24-25)", min_value=0, max_value=100, value=d.get("turnover_fy1", 0))

        with c19:

            d["turnover_fy2"] = st.number_input("Turnover % last year (FY 23-24)", min_value=0, max_value=100, value=d.get("turnover_fy2", 0))

        with c20:

            d["turnover_fy3"] = st.number_input("Turnover % 2 years ago (FY 22-23)", min_value=0, max_value=100, value=d.get("turnover_fy3", 0))



        avg_turnover = round((d["turnover_fy1"] + d["turnover_fy2"] + d["turnover_fy3"]) / 3, 1)

        if avg_turnover > 30:

            warn(f"Your average staff turnover is {avg_turnover}%. This is high. Investors and banks may ask questions about this.")

        elif avg_turnover > 0:

            st.success(f"✅ Average staff turnover: {avg_turnover}% - this looks healthy.")



    # ── NAVIGATION ────────────────────────────────────────────────────────

    st.markdown("")

    cn1, cn2, cn3 = st.columns([1, 2, 1])

    with cn1:

        if st.button("← Back", use_container_width=True):

            go(3); st.rerun()

    # Block navigation while any gender split does not reconcile with its total.
    workforce_groups = [
        ("Permanent employees", "perm_emp_male", "perm_emp_female", "total_perm_emp"),
        ("Other/temporary employees", "temp_emp_male", "temp_emp_female", "total_temp_emp"),
        ("Permanent workers", "perm_wkr_male", "perm_wkr_female", "total_perm_wkr"),
        ("Other/temporary workers", "temp_wkr_male", "temp_wkr_female", "total_temp_wkr"),
    ]
    workforce_errors = [
        f"{glabel}: Male ({d.get(m, 0)}) + Female ({d.get(f, 0)}) = "
        f"{d.get(m, 0) + d.get(f, 0)}, but Total = {d.get(t, 0)}."
        for glabel, m, f, t in workforce_groups
        if d.get(t, 0) > 0 and d.get(m, 0) + d.get(f, 0) != d.get(t, 0)
    ]

    with cn3:

        if st.button("Next: Governance & Risks →", type="primary", use_container_width=True):

            if workforce_errors:

                for _e in workforce_errors:

                    st.error(f"❌ {_e}")

                st.warning("Please fix the workforce counts above before continuing.")

            else:

                go(5); st.rerun()
# ═════════════════════════════════════════════════════════════════════════════
# STEP 5: GOVERNANCE, CSR & BUSINESS RISKS  (Upgraded)
# ═════════════════════════════════════════════════════════════════════════════

elif st.session_state.step == 5:

    st.header("⚖️ Step 5: Governance, CSR & Business Risks")
    st.write("The final section. Almost done!")

    d = st.session_state.data  # Ensure we're always working with a direct reference

    # ── HELPER: Safe empty-list initialiser (avoids shared-reference bug) ─
    def _init_list(existing, n):
        """Return a list of n independent dicts, preserving existing entries."""
        base = list(existing) if existing else []
        while len(base) < n:
            base.append({})
        return base[:n]

    # ══════════════════════════════════════════════════════════════════════
    # BLOCK 1: Related Companies
    # ══════════════════════════════════════════════════════════════════════
    with st.container(border=True):
        st.markdown("#### 1️⃣ Do You Own Other Companies?")
        tip(
            "Most small business owners run just one company. "
            "Only answer 'Yes' if you have formally registered other companies "
            "that you own or partially own."
        )

        owns_others = st.radio(
            "Do you own or control any other companies?",
            ["No - I run just one business", "Yes - I have related companies"],
            index=0 if d.get("has_subsidiaries", "No") != "Yes - I have related companies" else 1,
            key="has_subsidiaries_radio"
        )
        d["has_subsidiaries"] = owns_others

        if owns_others == "Yes - I have related companies":
            num_subs = int(st.number_input(
                "How many related companies?",
                min_value=1, max_value=20,
                value=max(1, len(d.get("subsidiaries", [{}])))
            ))

            subs = _init_list(d.get("subsidiaries"), num_subs)

            RELATIONSHIP_OPTIONS = [
                "Subsidiary (I own majority)",
                "Joint Venture (shared ownership)",
                "Associate Company",
                "Holding Company (owns me)",
                "Others",
            ]

            for i in range(num_subs):
                with st.expander(f"🏢 Company {i + 1}", expanded=True):
                    cs1, cs2, cs3 = st.columns(3)
                    with cs1:
                        name = st.text_input(
                            "Company Name",
                            key=f"sub_name_{i}",
                            value=subs[i].get("name", ""),
                            placeholder="e.g. Vaghani Agro Pvt Ltd"
                        )
                    with cs2:
                        saved_rel = subs[i].get("rel", RELATIONSHIP_OPTIONS[0])
                        rel_idx = (
                            RELATIONSHIP_OPTIONS.index(saved_rel)
                            if saved_rel in RELATIONSHIP_OPTIONS else 0
                        )
                        rel = st.selectbox(
                            "Your Relationship",
                            RELATIONSHIP_OPTIONS,
                            index=rel_idx,
                            key=f"sub_rel_{i}"
                        )
                        if rel == "Others":
                            rel = st.text_input(
                                "Describe relationship:",
                                key=f"sub_rel_other_{i}",
                                value=subs[i].get("rel_other", "")
                            )
                    with cs3:
                        shares = st.number_input(
                            "% Shares You Hold",
                            min_value=0, max_value=100,
                            value=int(subs[i].get("shares", 51)),
                            key=f"sub_shares_{i}"
                        )
                    subs[i] = {"name": name, "rel": rel, "shares": shares}

            d["subsidiaries"] = subs
        else:
            d.pop("subsidiaries", None)
            st.success("✅ Not applicable - single business entity.")

    # ══════════════════════════════════════════════════════════════════════
    # BLOCK 2: CSR
    # ══════════════════════════════════════════════════════════════════════
    with st.container(border=True):
        st.markdown("#### 2️⃣ Corporate Social Responsibility (CSR)")
        st.info(
            "**Is CSR mandatory for you?**\n\n"
            "CSR under **Section 135** of the Companies Act applies **only** if your company meets "
            "**any one** of:\n"
            "- Net worth ≥ ₹500 Crore, **or**\n"
            "- Annual turnover ≥ ₹1,000 Crore, **or**\n"
            "- Net profit ≥ ₹5 Crore in **any** financial year\n\n"
            "**Most MSMEs do NOT qualify. If you're below these numbers, select 'Not Applicable'.**"
        )

        CSR_OPTIONS = [
            "Not Applicable - we are below the threshold (most MSMEs)",
            "Yes - we meet the CSR threshold",
        ]
        saved_csr = d.get("csr_applicable", CSR_OPTIONS[0])
        csr_idx = 1 if saved_csr == CSR_OPTIONS[1] else 0

        d["csr_applicable"] = st.radio(
            "Is CSR (Section 135) applicable to your company?",
            CSR_OPTIONS,
            index=csr_idx,
            key="csr_applicable_radio"
        )

        if d["csr_applicable"] == CSR_OPTIONS[1]:
            cc1, cc2, cc3 = st.columns(3)
            with cc1:
                d["csr_turnover"] = st.text_input(
                    "Annual Turnover (₹)",
                    value=d.get("csr_turnover", ""),
                    placeholder="e.g. 12,00,00,00,000"
                )
            with cc2:
                d["csr_networth"] = st.text_input(
                    "Net Worth (₹)",
                    value=d.get("csr_networth", ""),
                    placeholder="e.g. 5,00,00,00,000"
                )
            with cc3:
                d["csr_budget"] = st.text_input(
                    "CSR Budget This Year (₹)",
                    value=d.get("csr_budget", ""),
                    placeholder="e.g. 25,00,000"
                )

            d["csr_activities"] = st.text_area(
                "Briefly describe your CSR activities",
                value=d.get("csr_activities", ""),
                placeholder="e.g. Funded 2 village schools in Bhavnagar; organised health camps for 500 workers.",
                height=80
            )
        else:
            for key in ("csr_turnover", "csr_networth", "csr_budget", "csr_activities"):
                d.pop(key, None)

    # ══════════════════════════════════════════════════════════════════════
    # BLOCK 3: Grievances
    # ══════════════════════════════════════════════════════════════════════
    with st.container(border=True):
        st.markdown("#### 3️⃣ Complaints & Grievance System")
        tip(
            "A grievance mechanism is a simple way for people to raise concerns with your business. "
            "Even a WhatsApp number, a suggestion box, or a complaints register qualifies."
        )

        d["has_grievance"] = st.toggle(
            "Do you have a formal way for people to raise complaints?",
            value=d.get("has_grievance", False)
        )

        if d["has_grievance"]:
            st.success("✅ Excellent - a grievance mechanism significantly improves your ESG score.")
            gc1, gc2 = st.columns(2)
            with gc1:
                d["grievance_url"] = st.text_input(
                    "Link to your grievance policy (optional)",
                    value=d.get("grievance_url", ""),
                    placeholder="e.g. www.yourbusiness.com/grievance"
                )
            with gc2:
                d["grievance_officer"] = st.text_input(
                    "Grievance Officer Name & Contact (optional)",
                    value=d.get("grievance_officer", ""),
                    placeholder="e.g. Mr. Ravi Shah - ravi@company.com"
                )
        else:
            warn(
                "**Recommendation:** Set up a simple complaint register or a dedicated email ID. "
                "This takes ~10 minutes and directly improves your BRSR score."
            )
            d.pop("grievance_url", None)
            d.pop("grievance_officer", None)

        st.markdown("**Complaints received this year - by stakeholder group**")

        GRIEVANCE_GROUPS = [
            "Customers",
            "Employees and Workers",
            "Suppliers / Vendors",
            "Community (people near your factory/office)",
            "Investors / Shareholders",
        ]

        grievance_data = d.get("grievance_data", {})

        for group in GRIEVANCE_GROUPS:
            with st.expander(f"📌 {group}"):
                cg1, cg2, cg3, cg4 = st.columns(4)
                prev = grievance_data.get(group, {})
                with cg1:
                    filed = st.number_input(
                        "Received this year",
                        min_value=0,
                        value=int(prev.get("filed", 0)),
                        key=f"filed_{group}"
                    )
                with cg2:
                    resolved = st.number_input(
                        "Resolved this year",
                        min_value=0,
                        value=int(prev.get("resolved", 0)),
                        key=f"resolved_{group}"
                    )
                with cg3:
                    pending = st.number_input(
                        "Still unresolved",
                        min_value=0,
                        value=int(prev.get("pending", 0)),
                        key=f"pending_{group}"
                    )
                with cg4:
                    prev_filed = st.number_input(
                        "Received last year",
                        min_value=0,
                        value=int(prev.get("prev_filed", 0)),
                        key=f"prev_{group}"
                    )

                # Live consistency check
                if resolved > filed:
                    st.warning("⚠️ Resolved complaints cannot exceed received complaints.")
                if pending > filed:
                    st.warning("⚠️ Unresolved complaints cannot exceed received complaints.")

                grievance_data[group] = {
                    "filed": filed,
                    "resolved": resolved,
                    "pending": pending,
                    "prev_filed": prev_filed,
                }

        d["grievance_data"] = grievance_data

    # ══════════════════════════════════════════════════════════════════════
    # BLOCK 4: Material Issues (Risks & Opportunities)
    # ══════════════════════════════════════════════════════════════════════
    with st.container(border=True):
        st.markdown("#### 4️⃣ Key Business Risks & Opportunities (ESG Related)")
        st.write("List the main environmental or social issues that could affect your business.")

        with st.expander("💡 Examples - click to expand"):
            ex1, ex2 = st.columns(2)
            with ex1:
                st.markdown(
                    "**🔴 Risks**\n"
                    "- Water shortage affecting your factory\n"
                    "- New pollution regulations adding costs\n"
                    "- Raw material price rise due to climate events\n"
                    "- Supply chain disruption from floods or cyclones"
                )
            with ex2:
                st.markdown(
                    "**🟢 Opportunities**\n"
                    "- Growing demand for eco-friendly products\n"
                    "- Government subsidy for solar panels\n"
                    "- Export orders from ESG-conscious foreign buyers\n"
                    "- Cost savings from energy efficiency upgrades"
                )

        num_issues = int(st.number_input(
            "How many key issues do you want to report? (minimum 2 recommended)",
            min_value=0, max_value=8,
            value=max(2, int(d.get("num_issues", 2)))
        ))
        d["num_issues"] = num_issues

        ISSUE_TOPICS = [
            "Water Usage / Scarcity",
            "Energy Consumption / Rising Energy Costs",
            "Waste / Pollution",
            "Worker Health & Safety",
            "Raw Material Availability",
            "Climate Change / Extreme Weather",
            "Regulatory / Legal Changes",
            "Gender Diversity & Inclusion",
            "Supply Chain Disruptions",
            "Technology / Cyber Risks",
            "Others",
        ]

        IMPACT_OPTIONS = ["High", "Medium", "Low"]
        TIMEFRAME_OPTIONS = ["Short-term (< 1 year)", "Medium-term (1–3 years)", "Long-term (3+ years)"]

        issues = _init_list(d.get("issues"), num_issues)

        for i in range(num_issues):
            with st.expander(f"{'🔴' if issues[i].get('type', 'Risk') == 'Risk' else '🟢'} Issue {i + 1}: {issues[i].get('topic', 'Not set yet')}", expanded=True):
                ci1, ci2 = st.columns(2)
                with ci1:
                    saved_topic = issues[i].get("topic", ISSUE_TOPICS[0])
                    topic_idx = (
                        ISSUE_TOPICS.index(saved_topic)
                        if saved_topic in ISSUE_TOPICS else 0
                    )
                    topic = st.selectbox(
                        "What is the issue?",
                        ISSUE_TOPICS,
                        index=topic_idx,
                        key=f"issue_topic_{i}"
                    )
                    if topic == "Others":
                        topic = st.text_input(
                            "Describe the issue:",
                            key=f"issue_other_{i}",
                            value=issues[i].get("topic_other", ""),
                            placeholder="e.g. Political instability in export markets"
                        )

                    itype = st.radio(
                        "Risk or Opportunity?",
                        ["Risk", "Opportunity"],
                        index=0 if issues[i].get("type", "Risk") == "Risk" else 1,
                        key=f"itype_{i}",
                        horizontal=True
                    )

                    impact = st.select_slider(
                        "Potential Impact",
                        options=IMPACT_OPTIONS,
                        value=issues[i].get("impact", "Medium"),
                        key=f"impact_{i}"
                    )

                    timeframe = st.selectbox(
                        "When could this affect you?",
                        TIMEFRAME_OPTIONS,
                        index=TIMEFRAME_OPTIONS.index(issues[i].get("timeframe", TIMEFRAME_OPTIONS[1]))
                        if issues[i].get("timeframe") in TIMEFRAME_OPTIONS else 1,
                        key=f"timeframe_{i}"
                    )

                with ci2:
                    rationale = st.text_area(
                        "Why does this affect your business?",
                        value=issues[i].get("rationale", ""),
                        key=f"irat_{i}",
                        height=100,
                        placeholder="e.g. Our factory uses groundwater daily. If the water table drops, we cannot operate."
                    )
                    mitigation = st.text_area(
                        "How are you handling it?",
                        value=issues[i].get("mitigation", ""),
                        key=f"imit_{i}",
                        height=100,
                        placeholder="e.g. We have installed rainwater harvesting and are targeting a 20% reduction this year."
                    )

                issues[i] = {
                    "topic": topic,
                    "type": itype,
                    "impact": impact,
                    "timeframe": timeframe,
                    "rationale": rationale,
                    "mitigation": mitigation,
                }

        d["issues"] = issues

    # ══════════════════════════════════════════════════════════════════════
    # COMPLETION SUMMARY
    # ══════════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.header("✅ Section A - Completion Summary")

    REQUIRED_CHECKS = {
        "Company name entered":          lambda: bool(d.get("company_name")),
        "Registered address entered":    lambda: bool(d.get("address")),
        "Business email entered":        lambda: bool(d.get("email")),
        "Contact person entered":        lambda: bool(d.get("contact_name")),
        "Business activities listed":    lambda: bool(d.get("activities") and d["activities"][0].get("main")),
        "Products / services listed":    lambda: bool(d.get("products") and d["products"][0].get("name")),
        "Plants / offices entered":      lambda: (d.get("num_plants") is not None and d.get("num_offices") is not None),
        "Employee data entered":         lambda: d.get("total_perm_emp", 0) > 0,
        "Grievance mechanism answered":  lambda: "has_grievance" in d,
        "At least 1 risk/opportunity":   lambda: bool(d.get("issues") and d["issues"][0].get("topic")),
    }

    check_results = {label: fn() for label, fn in REQUIRED_CHECKS.items()}
    filled = sum(check_results.values())
    total  = len(check_results)

    st.progress(filled / total, text=f"{filled} of {total} sections completed")

    col_a, col_b = st.columns(2)
    items = list(check_results.items())
    mid   = (len(items) + 1) // 2
    for col, chunk in zip([col_a, col_b], [items[:mid], items[mid:]]):
        with col:
            for label, status in chunk:
                st.markdown(f"{'✅' if status else '❌'} {label}")

    # ── Smart Insights ────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📊 Smart Insights Based On Your Data")

    insights_shown = 0

    if d.get("export_pct", 0) > 20:
        st.warning(
            "🌍 **High export exposure detected.** Foreign buyers increasingly require BRSR/ESG "
            "compliance - a complete report gives you a measurable competitive advantage."
        )
        insights_shown += 1

    if d.get("board_female", 0) == 0:
        st.warning(
            "👩 **No women on your board.** Adding even one woman director improves your ESG score "
            "and is increasingly expected by banks and larger corporate buyers."
        )
        insights_shown += 1

    if not d.get("has_grievance"):
        st.warning(
            "📣 **No grievance mechanism.** A simple complaints email or register takes ~10 minutes "
            "to set up and directly improves your BRSR score."
        )
        insights_shown += 1

    total_emp = d.get("total_perm_emp", 0)
    if total_emp > 0:
        female_pct = round((d.get("perm_emp_female", 0) / total_emp) * 100, 1)
        if female_pct < 10:
            st.warning(
                f"👥 **Only {female_pct}% of your employees are women.** "
                "Diversity above 30% significantly improves ESG ratings."
            )
            insights_shown += 1

    if d.get("activities") and any(
        a.get("main") == "Manufacturing" for a in d.get("activities", [])
    ):
        st.info(
            "🏭 **Manufacturing business detected.** Environmental disclosures "
            "(Section B - energy, water, waste) will be especially important in your full BRSR report."
        )
        insights_shown += 1

    if insights_shown == 0:
        st.success("🎯 No major gaps detected. Your data looks comprehensive!")

    # ── ESG Score & PDF Generation ────────────────────────────────────────
    st.markdown("---")
    st.subheader("📄 Generate Your BRSR PDF Report")

    esg_score = calc_esg_score()

    REQUIRED_FIELDS = {
        "company_name":   "Company Name",
        "address":        "Registered Address",
        "email":          "Business Email",
        "phone":          "Phone Number",
        "activities":     "Business Activities",
        "products":       "Products / Services",
        "num_plants":     "Number of Plants",
        "num_offices":    "Number of Offices",
        "total_perm_emp": "Total Permanent Employees",
    }

    def _field_filled(key):
        val = d.get(key)
        if val is None:
            return False
        if isinstance(val, str):
            return val.strip() != ""
        if isinstance(val, list):
            return len(val) > 0
        if isinstance(val, (int, float)):
            return True          # 0 is a valid answer
        return bool(val)

    missing_fields = [label for key, label in REQUIRED_FIELDS.items() if not _field_filled(key)]
    all_filled = len(missing_fields) == 0

    # Completion checklist
    st.markdown("#### ✅ Completion Checklist")
    cl1, cl2 = st.columns(2)
    field_items = list(REQUIRED_FIELDS.items())
    mid_f = (len(field_items) + 1) // 2
    for col, chunk in zip([cl1, cl2], [field_items[:mid_f], field_items[mid_f:]]):
        with col:
            for key, label in chunk:
                if _field_filled(key):
                    st.success(f"✔️ {label}")
                else:
                    st.warning(f"❌ {label} is missing")

    # ESG score display
    st.markdown("---")
    score_col, info_col = st.columns([1, 2])
    with score_col:
        colour = "green" if esg_score >= 70 else "orange" if esg_score >= 40 else "red"
        st.markdown(
            f"<h1 style='color:{colour}; text-align:center'>{esg_score}%</h1>"
            "<p style='text-align:center; color:gray'>ESG Readiness Score</p>",
            unsafe_allow_html=True
        )
        st.progress(esg_score / 100)
    with info_col:
        if esg_score >= 70:
            st.success("🎉 Strong report! You're ready to generate your BRSR PDF.")
        elif esg_score >= 40:
            st.warning("📈 Good progress. Fill in the remaining fields to improve your score before generating.")
        else:
            st.error("📋 Several fields are incomplete. Please review the checklist above.")

    # Gate: block generation only if required fields are missing
    st.markdown("---")
    SCORE_THRESHOLD = 60   # Configurable - set to whatever makes sense for your product

    if not all_filled:
        st.error(
            f"⚠️ **{len(missing_fields)} required field(s) missing:** "
            + ", ".join(missing_fields)
            + ". Please complete them before generating."
        )
    elif esg_score < SCORE_THRESHOLD:
        st.warning(
            f"⚠️ Your ESG score ({esg_score}%) is below the recommended threshold of {SCORE_THRESHOLD}%. "
            "You can still generate the report - but consider filling in the highlighted fields first."
        )
        col_gen, col_skip = st.columns(2)
        with col_gen:
            if st.button("Generate Anyway", use_container_width=True):
                _trigger_pdf_download(d, esg_score)
        with col_skip:
            st.caption("We recommend reaching at least 60% before sharing this report externally.")
    else:
        if st.button("🖨️ Generate BRSR PDF Report", type="primary", use_container_width=True):
            _trigger_pdf_download(d, esg_score)




    # ── Navigation ────────────────────────────────────────────────────────
    st.markdown("---")
    nav1, _, nav3 = st.columns([1, 2, 1])
    with nav1:
        if st.button("← Back to Step 4", use_container_width=True):
            go(4)
            st.rerun()
    with nav3:
        st.caption("Step 5 of 5 - Final Step")
        

# ─── BOTTOM NAVIGATION ──────────────────────────────────────────────────
from business_profile import render_section_navigation
render_section_navigation("Section A")
