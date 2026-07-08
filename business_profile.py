"""
business_profile.py — Central Tier Logic for BRSR Tool

Handles business type (Sole Prop / Partnership / Pvt Ltd / Listed) and
tells each principle which questions to show or hide.

Every page imports this and calls its functions to decide what to display.
"""

import streamlit as st


BUSINESS_TYPES = [
    "Sole Proprietorship",
    "Partnership / LLP",
    "Private Limited",
    "Public Listed"
]

TYPE_DESCRIPTIONS = {
    "Sole Proprietorship":
        "Owned by one person. Most small traders, consultants, shops.",
    "Partnership / LLP":
        "Owned by 2+ partners. Registered partnership firm or LLP.",
    "Private Limited":
        "Registered Pvt Ltd company. Has shareholders and directors.",
    "Public Listed":
        "Shares traded on BSE/NSE. BRSR is mandatory for top 1000 listed.",
}


# ────────────────────────────────────────────────────────────────
# INIT — call at top of every page
# ────────────────────────────────────────────────────────────────
def init_business_profile():
    """Ensures business_type exists in session state."""
    if "business_type" not in st.session_state:
        st.session_state.business_type = "Private Limited"


def get_business_type():
    init_business_profile()
    return st.session_state.business_type


# ────────────────────────────────────────────────────────────────
# TIER CHECKS
# ────────────────────────────────────────────────────────────────
def is_sole_prop():
    return get_business_type() == "Sole Proprietorship"

def is_partnership():
    return get_business_type() == "Partnership / LLP"

def is_pvt_ltd():
    return get_business_type() == "Private Limited"

def is_listed():
    return get_business_type() == "Public Listed"

def has_board():
    """True if business has a Board of Directors."""
    return get_business_type() in ["Private Limited", "Public Listed"]

def has_shareholders():
    return get_business_type() in ["Private Limited", "Public Listed"]

# Companies Act 2013, Section 135 CSR thresholds (any ONE triggers CSR).
# These apply to ANY company (Private Limited included), not just listed ones.
CSR_NETWORTH_CR = 500     # net worth >= Rs 500 crore
CSR_TURNOVER_CR = 1000    # turnover >= Rs 1,000 crore
CSR_NETPROFIT_CR = 5      # net profit >= Rs 5 crore in any financial year


def requires_csr(turnover_cr=0, net_worth_cr=0, net_profit_cr=0):
    """CSR under Companies Act Sec 135 applies to ANY company meeting any one
    of the net-worth / turnover / net-profit thresholds — not listed-only.
    Indicative: the statutory test uses audited financials, so confirm with a
    CA. With no financials supplied, returns False (unknown -> don't assume)."""
    return (
        (turnover_cr or 0) >= CSR_TURNOVER_CR
        or (net_worth_cr or 0) >= CSR_NETWORTH_CR
        or (net_profit_cr or 0) >= CSR_NETPROFIT_CR
    )

def requires_formal_policies():
    """Formal written policies expected for Pvt Ltd + Listed."""
    return has_board()


# ────────────────────────────────────────────────────────────────
# APPLICABILITY HELPERS (used in principle files)
# ────────────────────────────────────────────────────────────────
def should_show_board_questions():
    return has_board()

def should_show_csr_questions():
    return requires_csr()

def should_show_formal_policy_questions():
    return requires_formal_policies()

def should_show_kmp_questions():
    return has_board()

def should_show_shareholder_questions():
    return has_shareholders()


# ────────────────────────────────────────────────────────────────
# UI COMPONENTS
# ────────────────────────────────────────────────────────────────
def show_business_type_selector():
    """Renders the business type selector. Call on Home page."""
    init_business_profile()

    st.markdown("### 🏢 What type of business do you run?")
    st.caption(
        "This helps us hide questions that don't apply to you. "
        "You can change this later."
    )

    current = st.session_state.business_type
    if current not in BUSINESS_TYPES:
        current = BUSINESS_TYPES[2]  # default to Pvt Ltd

    selected = st.radio(
        "Business Type",
        BUSINESS_TYPES,
        index=BUSINESS_TYPES.index(current),
        format_func=lambda x: f"{x}  —  {TYPE_DESCRIPTIONS[x]}",
        label_visibility="collapsed"
    )
    st.session_state.business_type = selected
    return selected
def show_sidebar_logo():
    """Render Ecosetu logo in sidebar. Call from every page."""
    from pathlib import Path
    base_dir = Path(__file__).parent
    try:
        st.logo(
            str(base_dir / "assets" / "ecosetu_logo.png"),
            icon_image=str(base_dir / "assets" / "ecosetu_icon_128.png"),
            size="large"
        )
    except (AttributeError, TypeError):
        with st.sidebar:
            st.image(str(base_dir / "assets" / "ecosetu_logo.png"),
                     use_container_width=True)
            st.markdown("---")

def show_tier_badge():
    """Small badge to show current tier on each page."""
    btype = get_business_type()
    colors = {
        "Sole Proprietorship": "#e8f5e9",
        "Partnership / LLP": "#fff8e1",
        "Private Limited": "#e3f2fd",
        "Public Listed": "#fce4ec"
    }
    colors_text = {
        "Sole Proprietorship": "#2e7d32",
        "Partnership / LLP": "#e65100",
        "Private Limited": "#1565c0",
        "Public Listed": "#c2185b"
    }
    st.markdown(
        f'<div style="display:inline-block;'
        f'background:{colors.get(btype, "#eee")};'
        f'color:{colors_text.get(btype, "#333")};'
        f'padding:4px 12px;border-radius:12px;'
        f'font-size:12px;font-weight:600;margin-bottom:8px;">'
        f'🏢 {btype}</div>',
        unsafe_allow_html=True
    )


def show_not_applicable_notice(what):
    """Call when a section is N/A for current business type."""
    btype = get_business_type()
    st.info(
        f"📌 **{what}** is not applicable for {btype}. "
        "We'll mark this section as 'Not Applicable' in your BRSR report."
    )
# ─────────────────────────────────────────────────────────────────────────────
# CROSS-SECTION NAVIGATION
# ─────────────────────────────────────────────────────────────────────────────
PAGE_FLOW = [
    ("Home",         "Home.py",                                  "🏠"),
    ("Section A",    "pages/1_Section_A.py",                     "📋"),
    ("Section B",    "pages/2_Section_B.py",                     "🧭"),
    ("Principle 1",  "pages/3_Principle_1.py",                   "⚖️"),
    ("Principle 2",  "pages/4_Principle_2.py",                   "🔄"),
    ("Principle 3",  "pages/5_Principle_3.py",                   "👥"),
    ("Principle 4+5","pages/6_Principle_4_5.py",                 "🤝"),
    ("Principle 6",  "pages/7_Principle_6.py",                   "🌿"),
    ("Principle 7+8+9","pages/8_Principle_7_8_9.py",             "🤝"),
    ("Generate Report","pages/9_Generate_Report.py",             "📄"),
]
# ─────────────────────────────────────────────────────────────────────────────
# MANDATORY FIELD VALIDATION
# ─────────────────────────────────────────────────────────────────────────────
def check_mandatory_fields(current_page_name):
    """
    Checks if prerequisite sections are filled. Shows a warning + redirect
    button if not. Stops the page from rendering if validation fails.
    """
    requirements = {
        "Section B":       ("data",   "company_name", "Section A"),
        "Principle 1":     ("data_b", None,           "Section B"),
        "Principle 2":     ("data_b", None,           "Section B"),
        "Principle 3":     ("data_b", None,           "Section B"),
        "Principle 4+5":   ("data_b", None,           "Section B"),
        "Principle 6":     ("data_b", None,           "Section B"),
        "Principle 7+8+9": ("data_b", None,           "Section B"),
        "Generate Report": ("data",   "company_name", "Section A"),
    }

    if current_page_name not in requirements:
        return True

    key, subkey, prereq_name = requirements[current_page_name]
    data = st.session_state.get(key, {})

    if subkey:
        ok = bool(data.get(subkey))
    else:
        ok = bool(data) and len(data) > 1

    if not ok:
        st.warning(
            f"⚠️ **{prereq_name} not yet completed.** "
            f"Please fill {prereq_name} first — it pre-fills important data "
            f"used in this section."
        )
        col1, col2 = st.columns(2)
        with col1:
            path_map = {
                "Section A": "pages/1_Section_A.py",
                "Section B": "pages/2_Section_B.py",
            }
            if st.button(
                f"← Go fill {prereq_name}",
                type="primary",
                use_container_width=True,
                key=f"redirect_{current_page_name}"
            ):
                target = path_map.get(prereq_name)
                if target:
                    st.switch_page(target)
        with col2:
            st.markdown(
                "<div style='text-align:center; color:#64748B; "
                "padding-top:8px; font-size:13px;'>"
                "💡 Use the sidebar to navigate to Home"
                "</div>",
                unsafe_allow_html=True
            )
        st.stop()

    return True

def render_section_navigation(current_page_name):
    """
    Renders Previous / Next buttons at the bottom of every page.
    Home is reachable via the sidebar.
    """
    idx = next(
        (i for i, (name, _, _) in enumerate(PAGE_FLOW) if name == current_page_name),
        None
    )
    if idx is None:
        return

    st.markdown("---")
    st.markdown("")

    col_back, col_spacer, col_next = st.columns([2, 1, 2])

    # ── Previous button ────────────────────────────────────────────────
    with col_back:
        if idx > 0 and current_page_name != "Section A":
            prev_name, prev_path, prev_icon = PAGE_FLOW[idx - 1]
            if prev_name == "Home":
                # Skip showing "Back to Home" — use sidebar
                pass
            else:
                if st.button(
                    f"← Back to {prev_name}",
                    key=f"nav_back_{current_page_name}",
                    use_container_width=True
                ):
                    st.switch_page(prev_path)

    # ── Spacer (empty middle column) ──────────────────────────────────
    with col_spacer:
        st.markdown(
            "<div style='text-align:center; color:#94A3B8; "
            "font-size:11px; padding-top:8px;'>"
            "Use sidebar for Home"
            "</div>",
            unsafe_allow_html=True
        )

    # ── Next button ────────────────────────────────────────────────────
    with col_next:
        if idx < len(PAGE_FLOW) - 1:
            next_name, next_path, next_icon = PAGE_FLOW[idx + 1]
            if st.button(
                f"{next_icon} Continue to {next_name} →",
                type="primary",
                key=f"nav_next_{current_page_name}",
                use_container_width=True
            ):
                st.switch_page(next_path)

    st.markdown("")
