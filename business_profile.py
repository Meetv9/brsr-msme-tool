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

def requires_csr():
    """CSR mandatory under Companies Act Sec 135 — large companies only."""
    return is_listed()

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
