"""
9_📄_Generate_Report.py — Final BRSR PDF Generation

Pulls data from all sections + principles in session state and creates
a unified BRSR-audit-ready PDF.
"""

import streamlit as st
import sys
from pathlib import Path

# Make parent folder importable for business_profile & pdf_generator
sys.path.insert(0, str(Path(__file__).parent.parent))

from business_profile import (
    init_business_profile, get_business_type, show_tier_badge, is_listed, show_sidebar_logo
)

st.set_page_config(
    page_title="Generate BRSR Report",
    page_icon="📄",
    layout="centered"
)

init_business_profile()

st.title("📄 Generate Your BRSR Report")
show_tier_badge()
show_sidebar_logo()


st.markdown("""
This page compiles data from **all sections you filled** into one
BRSR-audit-ready PDF report.
""")

# ─────────────────────────────────────────────────────────────────────────────
# CHECK COMPLETENESS
# ─────────────────────────────────────────────────────────────────────────────
sections = {
    "Section A (General Disclosures)": st.session_state.get("data", {}),
    "Section B (Management & Process)": st.session_state.get("data_b", {}),
    "Principle 1 (Ethics)":
        st.session_state.get("p1", {}) or st.session_state.get("c_p1", {}),
    "Principle 2 (Sustainable Products)":
        st.session_state.get("p2", {}) or st.session_state.get("c_p2", {}),
    "Principle 3 (Employee Wellbeing)":
        st.session_state.get("p3", {}) or st.session_state.get("c_p3", {}),
    "Principles 4 & 5 (Stakeholders & Human Rights)":
        st.session_state.get("p4_5", {}) or st.session_state.get("c_p45", {}),
    "Principle 6 (Environment)": st.session_state.get("p6", {}),
    "Principles 7, 8, 9 (Policy, Community, Customers)":
        st.session_state.get("p789", {}),
}

st.markdown("### ✅ Completeness Check")

for name, data in sections.items():
    if data and len(data) > 1:
        st.markdown(f"✅ **{name}** — filled")
    else:
        st.markdown(f"⭕ {name} — not filled (will show as 'pending')")

# ─────────────────────────────────────────────────────────────────────────────
# COMPANY INFO PREVIEW
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
section_a = st.session_state.get("data", {})

if not section_a.get("company_name"):
    st.error(
        "⚠️ You haven't filled **Section A** yet. "
        "Please fill at least your company name before generating the report."
    )
    st.stop()

st.markdown("### 📋 Report Header Preview")

colp1, colp2 = st.columns(2)
with colp1:
    st.markdown(f"**Company:** {section_a.get('company_name', '—')}")
    st.markdown(f"**Business Type:** {get_business_type()}")
    st.markdown(f"**Financial Year:** {section_a.get('financial_year', '—')}")
with colp2:
    st.markdown(f"**CIN:** {section_a.get('cin') or 'N/A'}")
    st.markdown(f"**Turnover:** ₹{section_a.get('turnover_lakhs', 0)} Lakhs")
    st.markdown(f"**Email:** {section_a.get('email', '—')}")

# ─────────────────────────────────────────────────────────────────────────────
# GENERATE BUTTON
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🚀 Generate the PDF")

if st.button(
    "📄 Generate Full BRSR Report (PDF)",
    type="primary",
    use_container_width=True
):
    try:
        # Import PDF generator
        from pdf_generator import generate_brsr_pdf

        with st.spinner("Compiling all sections into PDF..."):
            # Calculate overall ESG score (same logic as Home.py)
            data = section_a
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
            overall_score = min(a_score, 100)

            # Build a merged data dict that PDF can consume
            merged = dict(data)
            merged["business_type_tier"] = get_business_type()
            merged["section_b"] = st.session_state.get("data_b", {})
            merged["p1"] = st.session_state.get("p1", {}) or st.session_state.get("c_p1", {})
            merged["p2"] = st.session_state.get("p2", {}) or st.session_state.get("c_p2", {})
            merged["p3"] = st.session_state.get("p3", {}) or st.session_state.get("c_p3", {})
            merged["p4_5"] = st.session_state.get("p4_5", {}) or st.session_state.get("c_p45", {})
            merged["p6"] = st.session_state.get("p6", {})
            merged["p789"] = st.session_state.get("p789", {})

            pdf_bytes = generate_brsr_pdf(merged, overall_score)

        st.success("✅ Report generated successfully!")
        st.download_button(
            label="📥 Download BRSR Report (PDF)",
            data=pdf_bytes,
            file_name=f"BRSR_Report_{data.get('company_name', 'Company').replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except ImportError:
        st.error(
            "❌ `pdf_generator.py` module not found. Ensure it exists "
            "in the same folder as Home.py."
        )
    except Exception as e:
        st.error(f"❌ Error generating PDF: {str(e)}")
        st.exception(e)
# ─────────────────────────────────────────────────────────────────────────────
# NOTE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "📌 **Note:** This PDF report is generated based on the data you have "
    "entered. For listed companies, please get this verified by a qualified "
    "ESG consultant or auditor before official BRSR submission to SEBI."
)


# ─── BOTTOM NAVIGATION ──────────────────────────────────────────────────
from business_profile import render_section_navigation
render_section_navigation("Generate Report")
