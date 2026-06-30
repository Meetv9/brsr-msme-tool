import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BRSR Section C | Principle 2",
    page_icon="♻️",
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
        padding: 14px 18px; border-radius: 0 10px 10px 0;
        margin: 10px 0 16px 0;
    }
    .benefit-box b { color: #1b5e20; font-size: 15px; }
    .benefit-box p { color: #2e7d32; margin: 4px 0 0 0; font-size: 14px; }
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
    .advanced-badge {
        background: #f3f4f6; color: #6b7280;
        border: 1px solid #d1d5db; border-radius: 20px;
        padding: 2px 12px; font-size: 12px; font-weight: 600;
    }
    .tip-box {
        background: #fff8e1; border-left: 4px solid #ffc107;
        padding: 10px 14px; border-radius: 0 8px 8px 0;
        font-size: 13px; margin: 6px 0;
    }
    .how-to-box {
        background: #e3f2fd; border-left: 4px solid #1976d2;
        padding: 10px 14px; border-radius: 0 8px 8px 0;
        font-size: 13px; margin: 6px 0;
    }
    .reaction-good {
        background: #e8f5e9; border: 1px solid #a5d6a7;
        border-radius: 8px; padding: 10px 14px;
        font-size: 13px; color: #1b5e20; margin: 6px 0;
    }
    .reaction-warn {
        background: #fff3e0; border: 1px solid #ffcc80;
        border-radius: 8px; padding: 10px 14px;
        font-size: 13px; color: #e65100; margin: 6px 0;
    }
    .reaction-bad {
        background: #ffebee; border: 1px solid #ef9a9a;
        border-radius: 8px; padding: 10px 14px;
        font-size: 13px; color: #c62828; margin: 6px 0;
    }
    .auto-calc {
        background: #f0f4ff; border: 1px solid #c7d2fe;
        border-radius: 8px; padding: 10px 14px;
        font-size: 14px; font-weight: 600;
        color: #3730a3; margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
if "c_p2" not in st.session_state:
    st.session_state.c_p2 = {}
if "step_c_p2" not in st.session_state:
    st.session_state.step_c_p2 = 1
if "lca_entries" not in st.session_state:
    st.session_state.lca_entries = []
if "risk_entries" not in st.session_state:
    st.session_state.risk_entries = []
if "reclaimed_categories" not in st.session_state:
    st.session_state.reclaimed_categories = []

p2 = st.session_state.c_p2
# ─── TIER LOGIC (NEW) ──────────────────────────────────────────
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from business_profile import init_business_profile, show_tier_badge, show_sidebar_logo

init_business_profile()
show_tier_badge()
show_sidebar_logo()

# ─── END TIER LOGIC ────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def benefit(title, text):
    st.markdown(
        f'<div class="benefit-box"><b>💰 {title}</b>'
        f'<p>{text}</p></div>',
        unsafe_allow_html=True
    )

def tip(text):
    st.markdown(f'<div class="tip-box">💡 {text}</div>',
                unsafe_allow_html=True)

def how_to(text):
    st.markdown(
        f'<div class="how-to-box">📖 How to find this data: {text}</div>',
        unsafe_allow_html=True
    )

def auto_calc(text):
    st.markdown(f'<div class="auto-calc">🔢 {text}</div>',
                unsafe_allow_html=True)

def react_good(text):
    st.markdown(f'<div class="reaction-good">✅ {text}</div>',
                unsafe_allow_html=True)

def react_warn(text):
    st.markdown(f'<div class="reaction-warn">⚠️ {text}</div>',
                unsafe_allow_html=True)

def react_bad(text):
    st.markdown(f'<div class="reaction-bad">🚨 {text}</div>',
                unsafe_allow_html=True)

def badge_essential():
    st.markdown('<span class="essential-badge">🔴 Essential</span>',
                unsafe_allow_html=True)

def badge_leadership():
    st.markdown('<span class="leadership-badge">🟡 Leadership</span>',
                unsafe_allow_html=True)

def badge_advanced():
    st.markdown('<span class="advanced-badge">⚪ Advanced</span>',
                unsafe_allow_html=True)

def safe_pct(num, den):
    try:
        num = float(num or 0)
        den = float(den or 0)
        if den > 0:
            return round((num / den) * 100, 1)
        return 0.0
    except:
        return 0.0

def go(step):
    st.session_state.step_c_p2 = step

# ─────────────────────────────────────────────────────────────────────────────
# SCORE
# ─────────────────────────────────────────────────────────────────────────────
def calc_p2_score():
    score = 0
    # Essential (70%) — credit substantive disclosure, not a page visit.

    # R&D / Capex: real investment figures entered (current or previous FY).
    if any(p2.get(k, 0) for k in (
            "rd_total", "rd_sustain", "capex_total", "capex_sustain",
            "rd_total_prev", "rd_sustain_prev",
            "capex_total_prev", "capex_sustain_prev")):
        score += 17

    # Sustainable sourcing: an affirmative procedure, backed by a written
    # description or a non-zero sourced %. Informal-but-undocumented = half.
    sourcing = str(p2.get("has_sourcing_procedure", "No"))
    if sourcing == "Yes" and (p2.get("sourcing_desc") or
                              p2.get("sourcing_pct_cur", 0) > 0):
        score += 18
    elif sourcing.startswith("Informal"):
        score += 9

    # End-of-life waste: at least one stream disclosed with real quantities
    # or a handling description.
    waste_keys = ("plastics", "ewaste", "hazardous", "other")
    if any(
        p2.get(f"{k}_reused_cur", 0) or p2.get(f"{k}_recycled_cur", 0) or
        p2.get(f"{k}_disposed_cur", 0) or
        (p2.get(f"has_{k}") == "Yes" and p2.get(f"{k}_process"))
        for k in waste_keys
    ):
        score += 17

    # EPR: a definite applicability answer. If applicable, PCB alignment
    # must be stated (not left at "Not sure") for full credit.
    epr = str(p2.get("epr_applicable", ""))
    if epr == "No":
        score += 18
    elif epr == "Yes":
        aligned = p2.get("epr_pcb_aligned", "")
        score += 18 if aligned and aligned != "Not sure" else 9

    # Leadership (30%) — already real-data based.
    if st.session_state.lca_entries:         score += 8
    if st.session_state.risk_entries:        score += 7
    if p2.get("recycled_input_cur", 0) > 0:  score += 5
    if any(p2.get(f"l4_{k}_reused_cur", 0) or p2.get(f"l4_{k}_recycled_cur", 0) or
           p2.get(f"l4_{k}_disposed_cur", 0) for k in waste_keys):
        score += 5
    if st.session_state.reclaimed_categories: score += 5
    return min(score, 100)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ♻️ P2 Progress")
    score = calc_p2_score()
    st.progress(score / 100)
    st.metric("P2 Completion", f"{score}%")
    if score < 40:
        st.caption("🔴 Just getting started")
    elif score < 70:
        st.caption("🟡 Good progress")
    else:
        st.caption("🟢 Looking strong")

    st.divider()
    st.markdown("**Field Guide**")
    st.markdown(
        '<span class="essential-badge">🔴 Essential</span> — Must fill<br>'
        '<span class="leadership-badge">🟡 Leadership</span> — Recommended<br>'
        '<span class="advanced-badge">⚪ Advanced</span> — Large companies',
        unsafe_allow_html=True
    )
    st.divider()
    st.markdown("**📌 P2 In Plain English**")
    st.caption(
        "Principle 2 asks: Are your products safe and sustainable? "
        "Do you source materials responsibly? "
        "How do you handle waste? "
        "European and US buyers check this before placing orders."
    )

# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
render_pagehead(
    "Step 4 of 9 · Principle 2",
    "Sustainable & Safe Products",
    "Show that your goods and services are made sustainably and safely — "
    "R&D, sustainable sourcing, and responsible resource use."
)

# Step nav
steps = {
    1: "💡 R&D & Capex",
    2: "🌿 Sourcing",
    3: "🗑️ End-of-Life",
    4: "📜 EPR",
    5: "🏆 Leadership",
    6: "✅ Summary"
}
nav = st.columns(6)
for i, (num, label) in enumerate(steps.items()):
    with nav[i]:
        t = "primary" if st.session_state.step_c_p2 == num else "secondary"
        if st.button(label, key=f"nav_p2_{num}",
                     type=t, use_container_width=True):
            go(num)

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# STEP 1: R&D AND CAPEX
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.step_c_p2 == 1:

    st.header("💡 Essential Q1 — R&D and Capital Investment in Sustainability")
    badge_essential()

    benefit(
        "Green investments = lower borrowing costs",
        "Banks like SBI, HDFC, and SIDBI offer Green Loans at lower interest "
        "rates to MSMEs that invest in energy-efficient equipment, solar panels, "
        "or waste reduction systems. Even small investments documented here qualify."
    )

    with st.container(border=True):
        st.markdown("#### Did your business invest in any technology to reduce "
                    "environmental or social impact this year?")

        tip("This does NOT require a formal R&D department. Any investment counts "
            "— LED lights, solar panel, water-saving machine, or fuel-efficient vehicle.")

        dna_rd = st.toggle(
            "No such investment made / Data Not Available",
            value=p2.get("dna_rd", False), key="dna_rd_toggle"
        )
        p2["dna_rd"] = dna_rd

        if dna_rd:
            st.markdown(
                '<div class="how-to-box">📖 Even if no formal investment, think:<br>'
                '• Did you switch to LED lighting? (energy efficiency capex)<br>'
                '• Did you buy equipment that uses less water or power?<br>'
                '• Did you change packaging to reduce plastic?<br>'
                'If yes to any — go back and fill this section.</div>',
                unsafe_allow_html=True
            )
            p2.update({"rd_total": 0, "rd_sustain": 0,
                        "capex_total": 0, "capex_sustain": 0,
                        "rd_total_prev": 0, "rd_sustain_prev": 0,
                        "capex_total_prev": 0, "capex_sustain_prev": 0})
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Current Financial Year**")
                p2["rd_total"] = st.number_input(
                    "Total R&D spend (₹)",
                    min_value=0, value=p2.get("rd_total", 0),
                    help="Most MSMEs have 0 here — that's fine."
                )
                p2["rd_sustain"] = st.number_input(
                    "R&D for environmental/social improvements (₹)",
                    min_value=0, value=p2.get("rd_sustain", 0),
                    help="e.g. Testing eco-friendly packaging"
                )
                p2["capex_total"] = st.number_input(
                    "Total Capex (₹)",
                    min_value=0, value=p2.get("capex_total", 0),
                    help="Total money spent on equipment, machinery, vehicles"
                )
                p2["capex_sustain"] = st.number_input(
                    "Capex on sustainability (₹)",
                    min_value=0, value=p2.get("capex_sustain", 0),
                    help="e.g. Solar panels, LED lighting, water recycling"
                )

            with c2:
                st.markdown("**Previous Financial Year**")
                p2["rd_total_prev"] = st.number_input(
                    "Total R&D spend (₹)",
                    min_value=0, value=p2.get("rd_total_prev", 0),
                    key="rd_t_prev"
                )
                p2["rd_sustain_prev"] = st.number_input(
                    "R&D for sustainability (₹)",
                    min_value=0, value=p2.get("rd_sustain_prev", 0),
                    key="rd_s_prev"
                )
                p2["capex_total_prev"] = st.number_input(
                    "Total Capex (₹)",
                    min_value=0, value=p2.get("capex_total_prev", 0),
                    key="cap_t_prev"
                )
                p2["capex_sustain_prev"] = st.number_input(
                    "Capex on sustainability (₹)",
                    min_value=0, value=p2.get("capex_sustain_prev", 0),
                    key="cap_s_prev"
                )

            # Auto-calculations
            st.markdown("")
            st.markdown("**Auto-Calculated Sustainability Percentages:**")
            mc1, mc2, mc3, mc4 = st.columns(4)
            rd_pct_cur = safe_pct(p2["rd_sustain"], p2["rd_total"])
            cap_pct_cur = safe_pct(p2["capex_sustain"], p2["capex_total"])
            rd_pct_prev = safe_pct(p2["rd_sustain_prev"], p2["rd_total_prev"])
            cap_pct_prev = safe_pct(p2["capex_sustain_prev"], p2["capex_total_prev"])

            mc1.metric("R&D Sustain % (Current)", f"{rd_pct_cur}%")
            mc2.metric("Capex Sustain % (Current)", f"{cap_pct_cur}%")
            mc3.metric("R&D Sustain % (Previous)", f"{rd_pct_prev}%")
            mc4.metric("Capex Sustain % (Previous)", f"{cap_pct_prev}%")

            if cap_pct_cur >= 10:
                react_good(
                    f"{cap_pct_cur}% of Capex on sustainability. "
                    "You qualify for SBI's Green Equipment Loan scheme."
                )
            elif p2["capex_sustain"] > 0:
                react_warn(
                    f"{cap_pct_cur}% sustainability Capex. "
                    "Increasing above 10% qualifies for preferential green financing."
                )

            if p2["capex_total"] > 0 or p2["rd_total"] > 0:
                p2["sustain_improvements"] = st.text_area(
                    "Describe what improvements these investments achieved",
                    value=p2.get("sustain_improvements", ""),
                    height=80,
                    placeholder="e.g. Installed 2KW solar panel — reduces monthly "
                                "electricity by Rs.3,000 and cuts CO2 emissions."
                )

        p2["rd_capex_done"] = True

    # Bottom navigation
    _, _, c_next = st.columns([1, 2, 1])
    with c_next:
        if st.button("Next: Sustainable Sourcing →",
                     type="primary", use_container_width=True):
            go(2); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 2: SUSTAINABLE SOURCING
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_c_p2 == 2:

    st.header("🌿 Essential Q2 — Sustainable Sourcing")
    badge_essential()

    benefit(
        "Sustainable sourcing wins you bigger contracts",
        "Large Indian corporates like Tata, Reliance, and ITC now require "
        "suppliers to prove sustainable sourcing. European buyers have made "
        "this mandatory since 2024. Documenting this puts you ahead of 90% of MSMEs."
    )

    with st.container(border=True):
        st.markdown("#### Do you have any procedure for sourcing materials "
                    "sustainably or responsibly?")

        st.markdown(
            '<div class="how-to-box">📖 Examples any MSME can claim:<br>'
            '• Buying from local farmers or manufacturers (reduces transport)<br>'
            '• Preferring suppliers who use less plastic packaging<br>'
            '• Checking suppliers do not use child labour<br>'
            '• Using recycled or biodegradable packaging<br>'
            '• Sourcing from women-owned or MSME suppliers</div>',
            unsafe_allow_html=True
        )

        p2["has_sourcing_procedure"] = st.radio(
            "Does your business have a sustainable sourcing procedure?",
            ["Yes", "No", "Informal — we do it but haven't written it down"],
            index=["Yes", "No",
                   "Informal — we do it but haven't written it down"].index(
                p2.get("has_sourcing_procedure", "No")
            ),
            key="sourcing_proc"
        )

        if p2["has_sourcing_procedure"] == "Yes":
            react_good("You have a sourcing procedure — strong positive for "
                       "export buyers and large corporates.")
            p2["sourcing_desc"] = st.text_area(
                "Briefly describe your sustainable sourcing procedure",
                value=p2.get("sourcing_desc", ""),
                height=80,
                placeholder="e.g. We prefer local suppliers within 100km. "
                            "We verify top 5 suppliers do not employ workers under 18."
            )
            c1, c2 = st.columns(2)
            with c1:
                p2["sourcing_pct_cur"] = st.slider(
                    "% of inputs sourced sustainably — Current FY",
                    0, 100, p2.get("sourcing_pct_cur", 0)
                )
            with c2:
                p2["sourcing_pct_prev"] = st.slider(
                    "% of inputs sourced sustainably — Previous FY",
                    0, 100, p2.get("sourcing_pct_prev", 0),
                    key="src_prev"
                )
            auto_calc(
                f"Current: {p2['sourcing_pct_cur']}% sustainably sourced | "
                f"Previous: {p2['sourcing_pct_prev']}%"
            )
            if p2["sourcing_pct_cur"] >= 50:
                react_good(
                    f"{p2['sourcing_pct_cur']}% sustainable sourcing — "
                    "use this as a marketing claim with buyers."
                )

        elif p2["has_sourcing_procedure"] == \
                "Informal — we do it but haven't written it down":
            react_warn(
                "You're already doing it but haven't documented it. "
                "Use the generator below to create a simple policy."
            )
            if st.button("✨ Generate Simple Sourcing Policy"):
                company = st.session_state.get(
                    "data", {}
                ).get("company_name", "Our Company")
                p2["generated_sourcing_policy"] = (
                    f"{company} is committed to responsible sourcing. "
                    f"We prioritise local suppliers to reduce transport emissions. "
                    f"We verify that key suppliers comply with labour laws and do not "
                    f"employ workers below the legal working age. We continuously work "
                    f"to increase the proportion of sustainably sourced inputs."
                )
            if p2.get("generated_sourcing_policy"):
                st.markdown(
                    f'<div style="background:#f0fff4; border:1px dashed #2e7d32; '
                    f'border-radius:8px; padding:16px; font-size:13px;">'
                    f'{p2["generated_sourcing_policy"]}</div>',
                    unsafe_allow_html=True
                )
        else:
            react_bad(
                "No sustainable sourcing procedure yet. "
                "Start with one simple rule — e.g. 'We prefer local suppliers' "
                "— and document it."
            )

        p2["sourcing_done"] = True

    c_back, _, c_next = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go(1); st.rerun()
    with c_next:
        if st.button("Next: Waste & End-of-Life →",
                     type="primary", use_container_width=True):
            go(3); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 3: WASTE & END-OF-LIFE
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_c_p2 == 3:

    st.header("🗑️ Essential Q3 — Waste Management & Product End-of-Life")
    badge_essential()

    benefit(
        "Proper waste management saves money and reduces legal risk",
        "Improper waste disposal can result in pollution board fines of "
        "₹1 lakh to ₹10 lakh. Documenting your waste management process "
        "protects you legally and improves your BRSR score significantly."
    )

    tip("Select only the waste types relevant to your business. "
        "1 metric tonne = 1000 kg. "
        "If unsure, weigh one bag of waste and multiply by bags per year.")

    waste_config = [
        ("plastics", "🧴 Plastics & Packaging",
         "Plastic bags, wrappers, bottles, pouches, shrink wrap"),
        ("ewaste", "💻 E-Waste",
         "Old computers, phones, printers, batteries, cables"),
        ("hazardous", "⚠️ Hazardous Waste",
         "Chemicals, solvents, paints, industrial oils"),
        ("other", "🗂️ Other Waste",
         "Food waste, fabric scraps, paper, cardboard, wood")
    ]

    for key, label, examples in waste_config:
        with st.expander(label, expanded=(key == "plastics")):
            has_key = f"has_{key}"
            p2[has_key] = st.radio(
                f"Does your business generate {label.split(' ', 1)[1]}?",
                ["Yes", "No"],
                horizontal=True,
                index=0 if p2.get(has_key, "No") == "Yes" else 1,
                key=f"radio_{key}"
            )

            if p2[has_key] == "Yes":
                how_to(f"Examples: {examples}")

                p2[f"{key}_process"] = st.text_area(
                    "How do you handle this waste?",
                    value=p2.get(f"{key}_process", ""),
                    height=70,
                    placeholder="e.g. Sold to authorized scrap dealer. "
                                "We have reduced packaging by switching to "
                                "biodegradable alternatives.",
                    key=f"proc_{key}"
                )

                st.markdown("**Quantities (metric tonnes):**")

                # Current FY — self-labeling inputs (stack cleanly on mobile)
                st.markdown("**Current FY**")
                rc = st.columns(3)
                cur_reuse = rc[0].number_input(
                    "Re-Used (MT)", min_value=0.0, step=0.1,
                    value=float(p2.get(f"{key}_reused_cur", 0.0)),
                    key=f"{key}_reused_cur"
                )
                cur_recycle = rc[1].number_input(
                    "Recycled (MT)", min_value=0.0, step=0.1,
                    value=float(p2.get(f"{key}_recycled_cur", 0.0)),
                    key=f"{key}_recycled_cur"
                )
                cur_dispose = rc[2].number_input(
                    "Safely Disposed (MT)", min_value=0.0, step=0.1,
                    value=float(p2.get(f"{key}_disposed_cur", 0.0)),
                    key=f"{key}_disposed_cur"
                )
                cur_total = cur_reuse + cur_recycle + cur_dispose
                cur_pct = safe_pct(cur_reuse + cur_recycle, cur_total)
                st.caption(
                    f"Total: **{round(cur_total, 2)} MT** · "
                    f"Recycled/Re-used: **{cur_pct}%**"
                )

                # Previous FY — self-labeling inputs
                st.markdown("**Previous FY**")
                rp = st.columns(3)
                prev_reuse = rp[0].number_input(
                    "Re-Used (MT)", min_value=0.0, step=0.1,
                    value=float(p2.get(f"{key}_reused_prev", 0.0)),
                    key=f"{key}_reused_prev"
                )
                prev_recycle = rp[1].number_input(
                    "Recycled (MT)", min_value=0.0, step=0.1,
                    value=float(p2.get(f"{key}_recycled_prev", 0.0)),
                    key=f"{key}_recycled_prev"
                )
                prev_dispose = rp[2].number_input(
                    "Safely Disposed (MT)", min_value=0.0, step=0.1,
                    value=float(p2.get(f"{key}_disposed_prev", 0.0)),
                    key=f"{key}_disposed_prev"
                )
                prev_total = prev_reuse + prev_recycle + prev_dispose
                prev_pct = safe_pct(prev_reuse + prev_recycle, prev_total)
                st.caption(
                    f"Total: **{round(prev_total, 2)} MT** · "
                    f"Recycled/Re-used: **{prev_pct}%**"
                )

                # Save
                p2.update({
                    f"{key}_reused_cur": cur_reuse,
                    f"{key}_recycled_cur": cur_recycle,
                    f"{key}_disposed_cur": cur_dispose,
                    f"{key}_reused_prev": prev_reuse,
                    f"{key}_recycled_prev": prev_recycle,
                    f"{key}_disposed_prev": prev_dispose,
                })

                if cur_pct >= 50:
                    react_good(
                        f"{cur_pct}% of your {label.split(' ', 1)[1]} is "
                        "recycled or reused — strong circular economy performance."
                    )
                elif cur_total > 0:
                    react_warn(
                        f"Only {cur_pct}% recycled. "
                        "Find a local scrap dealer to increase this."
                    )

    p2["endoflife_done"] = True

    c_back, _, c_next = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go(2); st.rerun()
    with c_next:
        if st.button("Next: EPR →",
                     type="primary", use_container_width=True):
            go(4); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 4: EPR
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_c_p2 == 4:

    st.header("📜 Essential Q4 — Extended Producer Responsibility (EPR)")
    badge_essential()

    benefit(
        "EPR compliance protects you from heavy penalties",
        "Missing your EPR targets attracts Environmental Compensation, charged by "
        "formula on the shortfall (per tonne not collected/recycled) — it can run "
        "into lakhs, plus possible action under the Environment (Protection) Act. "
        "Documenting EPR status clearly protects you legally."
    )

    with st.container(border=True):
        st.markdown("#### Quick EPR Check — does EPR apply to you?")

        col1, col2 = st.columns(2)
        with col1:
            uses_plastic = st.checkbox(
                "My business uses plastic packaging or produces plastic products",
                value=p2.get("uses_plastic", False)
            )
            p2["uses_plastic"] = uses_plastic

            makes_electronics = st.checkbox(
                "My business manufactures or sells electronic products",
                value=p2.get("makes_electronics", False)
            )
            p2["makes_electronics"] = makes_electronics

        with col2:
            makes_batteries = st.checkbox(
                "My business makes or uses industrial batteries",
                value=p2.get("makes_batteries", False)
            )
            p2["makes_batteries"] = makes_batteries

            other_epr = st.checkbox(
                "My business falls under other EPR categories "
                "(tyres, oils, hazardous waste)",
                value=p2.get("other_epr", False)
            )
            p2["other_epr"] = other_epr

        epr_likely = (uses_plastic or makes_electronics or
                      makes_batteries or other_epr)

        st.markdown("")
        if epr_likely:
            react_warn(
                "EPR likely applies to your business. "
                "You should be registered with the Pollution Control Board."
            )
        else:
            react_good("EPR likely does NOT apply. Answer 'No' below.")

        p2["epr_applicable"] = st.radio(
            "⚠️ Is EPR applicable to your business?",
            ["Yes", "No", "Not Sure — need to check"],
            index=["Yes", "No", "Not Sure — need to check"].index(
                p2.get("epr_applicable", "Yes" if epr_likely else "No")
            ),
            key="epr_radio"
        )

        if p2["epr_applicable"] == "Yes":
            p2["epr_pcb_aligned"] = st.radio(
                "Is your waste collection plan aligned with the EPR plan "
                "submitted to the Pollution Control Board?",
                ["Yes — fully aligned", "Partially aligned",
                 "Not yet submitted to PCB", "Not sure"],
                index=["Yes — fully aligned", "Partially aligned",
                       "Not yet submitted to PCB", "Not sure"].index(
                    p2.get("epr_pcb_aligned", "Not sure")
                ),
                key="epr_pcb_radio"
            )
            if p2["epr_pcb_aligned"] == "Not yet submitted to PCB":
                react_bad(
                    "You must submit your EPR plan to the PCB. "
                    "Non-compliance attracts formula-based Environmental Compensation "
                    "on your shortfall (and can run into lakhs). "
                    "Contact your state PCB office or hire a local environmental "
                    "consultant — typically costs ₹10,000–25,000 for an MSME."
                )
            elif p2["epr_pcb_aligned"] in ["Partially aligned", "Not sure"]:
                p2["epr_steps"] = st.text_area(
                    "What steps are you taking to align?",
                    value=p2.get("epr_steps", ""),
                    height=80,
                    placeholder="e.g. We have engaged XYZ Environmental Consultants "
                                "to review our EPR plan and ensure full compliance "
                                "by Q3 this financial year."
                )
            else:
                react_good(
                    "EPR plan aligned — strong compliance. "
                    "Keep PCB registration renewed annually."
                )

        elif p2["epr_applicable"] == "Not Sure — need to check":
            st.info(
                "📞 To check EPR applicability, contact your state Pollution "
                "Control Board or visit cpcb.nic.in"
            )
        else:
            react_good(
                "EPR not applicable — document this clearly. "
                "It protects you from future regulatory queries."
            )

        p2["epr_done"] = True

    c_back, _, c_next = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go(3); st.rerun()
    with c_next:
        if st.button("Next: Leadership Indicators →",
                     type="primary", use_container_width=True):
            go(5); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 5: LEADERSHIP INDICATORS
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_c_p2 == 5:

    st.header("🏆 Leadership Indicators — L1 to L5")
    badge_leadership()

    st.info(
        "Leadership indicators are voluntary. Filling these signals advanced "
        "ESG maturity and helps unlock premium finance and export opportunities. "
        "Most MSMEs will fill some but not all — that is completely acceptable."
    )

    # Use tabs — one per leadership indicator
    lt1, lt2, lt3, lt4, lt5 = st.tabs([
        "🔬 L1: LCA",
        "⚠️ L2: Product Risks",
        "♻️ L3: Recycled Inputs",
        "📦 L4: Reclaimed MT",
        "📊 L5: Reclaimed %"
    ])

    # ── L1: LCA ───────────────────────────────────────────────────────────
    with lt1:
        badge_leadership()
        st.markdown("### L1 — Life Cycle Assessment (LCA)")
        st.markdown(
            "An LCA studies the full environmental impact of a product — "
            "from raw material extraction to disposal. "
            "Most MSMEs have not done this — that is completely normal."
        )
        tip("Even a simplified LCA done with a local consultant or college "
            "counts. Some IITs and NITs offer free LCA studies for MSMEs.")

        lca_done = st.radio(
            "Has your business conducted a Life Cycle Assessment for any product?",
            ["No", "Yes"],
            horizontal=True,
            index=0 if p2.get("lca_done", "No") == "No" else 1,
            key="lca_done_radio"
        )
        p2["lca_done"] = lca_done

        if lca_done == "Yes":
            st.markdown("**Add LCA entries — one per product:**")

            with st.form("lca_form", clear_on_submit=True):
                lf1, lf2, lf3 = st.columns(3)
                with lf1:
                    lca_nic = st.text_input(
                        "NIC Code",
                        placeholder="e.g. 10790"
                    )
                    lca_product = st.text_input(
                        "Product / Service Name",
                        placeholder="e.g. Freeze-dried Palak Paneer"
                    )
                with lf2:
                    lca_turnover = st.number_input(
                        "% of Turnover contributed",
                        min_value=0.0, max_value=100.0, value=0.0
                    )
                    lca_boundary = st.text_input(
                        "Boundary of assessment",
                        placeholder="e.g. Cradle to gate / Full lifecycle"
                    )
                with lf3:
                    lca_external = st.radio(
                        "Done by external agency?",
                        ["Yes", "No"], horizontal=True,
                        key="lca_ext_form"
                    )
                    lca_public = st.radio(
                        "Results published publicly?",
                        ["Yes", "No"], horizontal=True,
                        key="lca_pub_form"
                    )
                lca_link = st.text_input(
                    "Web link to results (if public)",
                    placeholder="e.g. www.yourbusiness.com/lca-report"
                )

                if st.form_submit_button("➕ Add LCA Entry"):
                    st.session_state.lca_entries.append({
                        "NIC Code": lca_nic,
                        "Product": lca_product,
                        "Turnover %": lca_turnover,
                        "Boundary": lca_boundary,
                        "External Agency": lca_external,
                        "Public Results": lca_public,
                        "Web Link": lca_link or "—"
                    })
                    st.success("LCA entry added.")

            if st.session_state.lca_entries:
                st.markdown("**Your LCA entries:**")
                st.dataframe(
                    pd.DataFrame(st.session_state.lca_entries),
                    use_container_width=True
                )
                if st.button("🗑️ Clear all LCA entries", key="clear_lca"):
                    st.session_state.lca_entries = []
                    st.rerun()
        else:
            st.caption(
                "If you ever conduct an LCA in future, come back and fill this section. "
                "It significantly improves your score with international buyers."
            )

    # ── L2: PRODUCT RISKS ────────────────────────────────────────────────
    with lt2:
        badge_leadership()
        st.markdown("### L2 — Social / Environmental Risks from Products")
        st.markdown(
            "Even without an LCA, if you are aware of any environmental "
            "or social concern arising from your product or its disposal, "
            "mention it here along with what you are doing about it."
        )
        tip("Example: A food packaging company knows its plastic pouches "
            "contribute to landfill waste. Action: switching to biodegradable "
            "alternatives by FY2026.")

        with st.form("risk_form", clear_on_submit=True):
            rf1, rf2 = st.columns(2)
            with rf1:
                risk_product = st.text_input(
                    "Product / Service Name",
                    placeholder="e.g. Freeze-dried Palak Paneer"
                )
                risk_desc = st.text_area(
                    "Description of risk or concern",
                    height=100,
                    placeholder="e.g. Our plastic packaging contributes to "
                                "landfill waste in urban areas."
                )
            with rf2:
                risk_action = st.text_area(
                    "Action taken or planned to mitigate",
                    height=100,
                    placeholder="e.g. We are testing biodegradable packaging "
                                "and plan to switch all products by FY2026. "
                                "Currently 20% of SKUs have switched."
                )

            if st.form_submit_button("➕ Add Risk Entry"):
                st.session_state.risk_entries.append({
                    "Product": risk_product,
                    "Risk / Concern": risk_desc,
                    "Action Taken": risk_action
                })
                st.success("Risk entry added.")

        if st.session_state.risk_entries:
            st.markdown("**Your risk entries:**")
            st.dataframe(
                pd.DataFrame(st.session_state.risk_entries),
                use_container_width=True
            )
            if st.button("🗑️ Clear all risk entries", key="clear_risks"):
                st.session_state.risk_entries = []
                st.rerun()

    # ── L3: RECYCLED INPUTS ───────────────────────────────────────────────
    with lt3:
        badge_leadership()
        st.markdown("### L3 — Recycled / Reused Input Material %")
        st.markdown(
            "What percentage of your raw materials (by value) were "
            "recycled or reused material?"
        )

        how_to(
            "Check your purchase invoices — some suppliers label materials "
            "as 'recycled' or 'reclaimed'. If you buy scrap material from a "
            "dealer, that counts as recycled input. "
            "Divide recycled material spend by total material spend × 100."
        )

        dna_recycled = st.toggle(
            "Data Not Available",
            value=p2.get("dna_recycled", False),
            key="dna_recycled_tog"
        )
        p2["dna_recycled"] = dna_recycled

        if not dna_recycled:
            l3c1, l3c2 = st.columns(2)
            with l3c1:
                p2["recycled_input_cur"] = st.number_input(
                    "Recycled / Reused input % — Current FY",
                    min_value=0.0, max_value=100.0,
                    value=float(p2.get("recycled_input_cur", 0.0)),
                    step=0.5, key="ri_cur"
                )
            with l3c2:
                p2["recycled_input_prev"] = st.number_input(
                    "Recycled / Reused input % — Previous FY",
                    min_value=0.0, max_value=100.0,
                    value=float(p2.get("recycled_input_prev", 0.0)),
                    step=0.5, key="ri_prev"
                )

            if p2["recycled_input_cur"] > 0:
                react_good(
                    f"{p2['recycled_input_cur']}% recycled inputs — "
                    "a positive circular economy indicator. "
                    "Mention this in your marketing materials."
                )
            else:
                tip(
                    "Even small amounts count. Check if any raw material "
                    "you buy comes from recycled sources."
                )

    # ── L4: RECLAIMED MT ─────────────────────────────────────────────────
    with lt4:
        badge_leadership()
        st.markdown("### L4 — Products Reclaimed at End of Life (Metric Tonnes)")
        st.markdown(
            "Of the products and packaging you sold, how much came back "
            "to you (or an authorized recycler) for reuse, recycling, "
            "or safe disposal?"
        )

        tip("1 metric tonne = 1000 kg. "
            "Ask your scrap dealer or recycler for weight receipts. "
            "This data can usually be found in your scrap sale invoices.")

        dna_mt = st.toggle(
            "Data Not Available",
            value=p2.get("dna_reclaimed_mt", False),
            key="dna_mt_tog"
        )
        p2["dna_reclaimed_mt"] = dna_mt

        if not dna_mt:
            waste_types_l4 = [
                ("plastics", "Plastics (including packaging)"),
                ("ewaste", "E-waste"),
                ("hazardous", "Hazardous waste"),
                ("other", "Other waste")
            ]

            for wkey, wlabel in waste_types_l4:
                with st.expander(wlabel, expanded=(wkey == "plastics")):
                    st.markdown("**Current FY (MT)**")
                    rcur = st.columns(3)
                    p2[f"l4_{wkey}_reused_cur"] = rcur[0].number_input(
                        "Re-Used", min_value=0.0, step=0.01,
                        value=float(p2.get(f"l4_{wkey}_reused_cur", 0.0)),
                        key=f"l4_{wkey}_rc"
                    )
                    p2[f"l4_{wkey}_recycled_cur"] = rcur[1].number_input(
                        "Recycled", min_value=0.0, step=0.01,
                        value=float(p2.get(f"l4_{wkey}_recycled_cur", 0.0)),
                        key=f"l4_{wkey}_rcc"
                    )
                    p2[f"l4_{wkey}_disposed_cur"] = rcur[2].number_input(
                        "Safely Disposed", min_value=0.0, step=0.01,
                        value=float(p2.get(f"l4_{wkey}_disposed_cur", 0.0)),
                        key=f"l4_{wkey}_dc"
                    )

                    st.markdown("**Previous FY (MT)**")
                    rprev = st.columns(3)
                    p2[f"l4_{wkey}_reused_prev"] = rprev[0].number_input(
                        "Re-Used", min_value=0.0, step=0.01,
                        value=float(p2.get(f"l4_{wkey}_reused_prev", 0.0)),
                        key=f"l4_{wkey}_rp"
                    )
                    p2[f"l4_{wkey}_recycled_prev"] = rprev[1].number_input(
                        "Recycled", min_value=0.0, step=0.01,
                        value=float(p2.get(f"l4_{wkey}_recycled_prev", 0.0)),
                        key=f"l4_{wkey}_rcp"
                    )
                    p2[f"l4_{wkey}_disposed_prev"] = rprev[2].number_input(
                        "Safely Disposed", min_value=0.0, step=0.01,
                        value=float(p2.get(f"l4_{wkey}_disposed_prev", 0.0)),
                        key=f"l4_{wkey}_dp"
                    )

            p2["reclaimed_mt_done"] = True

    # ── L5: RECLAIMED % ───────────────────────────────────────────────────
    with lt5:
        badge_leadership()
        st.markdown("### L5 — Reclaimed Products as % of Products Sold")
        st.markdown(
            "For each product category, what percentage of products sold "
            "were reclaimed (returned for recycling or safe disposal)?"
        )

        tip("Example: You sold 10,000 units of Product A. "
            "500 units were returned or collected for recycling. "
            "That's 5% reclaimed.")

        with st.form("reclaimed_cat_form", clear_on_submit=True):
            rc1, rc2 = st.columns(2)
            with rc1:
                cat_name = st.text_input(
                    "Product Category",
                    placeholder="e.g. Freeze-dried Curries"
                )
            with rc2:
                cat_pct = st.number_input(
                    "Reclaimed as % of products sold",
                    min_value=0.0, max_value=100.0, value=0.0, step=0.5
                )

            if st.form_submit_button("➕ Add Category"):
                st.session_state.reclaimed_categories.append({
                    "Product Category": cat_name,
                    "Reclaimed %": cat_pct
                })
                st.success("Category added.")

        if st.session_state.reclaimed_categories:
            st.markdown("**Your reclaimed categories:**")
            st.dataframe(
                pd.DataFrame(st.session_state.reclaimed_categories),
                use_container_width=True
            )
            if st.button("🗑️ Clear categories", key="clear_cats"):
                st.session_state.reclaimed_categories = []
                st.rerun()

    # Bottom nav
    c_back, _, c_next = st.columns([1, 2, 1])
    with c_back:
        if st.button("← Back", use_container_width=True):
            go(4); st.rerun()
    with c_next:
        if st.button("Next: Summary →",
                     type="primary", use_container_width=True):
            go(6); st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# STEP 6: SUMMARY
# ═════════════════════════════════════════════════════════════════════════════
elif st.session_state.step_c_p2 == 6:

    st.header("✅ Principle 2 — Complete Summary & Score")

    final_score = calc_p2_score()

    sc1, sc2 = st.columns([1, 2])
    with sc1:
        colour = ("green" if final_score >= 70
                  else "orange" if final_score >= 40 else "red")
        st.markdown(
            f"<h1 style='color:{colour}; text-align:center'>{final_score}%</h1>"
            "<p style='text-align:center; color:gray'>P2 Completion Score</p>",
            unsafe_allow_html=True
        )
        st.progress(final_score / 100)
    with sc2:
        if final_score >= 70:
            react_good("Strong P2 disclosure. Your sustainable products section "
                       "will impress export buyers and green loan assessors.")
        elif final_score >= 40:
            react_warn("Good progress. Complete missing sections to strengthen score.")
        else:
            react_bad("Several essential fields incomplete. Go back and fill them.")

    # ── ESSENTIAL SUMMARY ─────────────────────────────────────────────────
    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### 🔴 Essential Indicators Summary")
        ec1, ec2, ec3, ec4 = st.columns(4)
        ec1.metric("Sustainability Capex",
                   f"Rs.{p2.get('capex_sustain', 0):,}")
        ec2.metric("Sustainable Sourcing",
                   f"{p2.get('sourcing_pct_cur', 0)}%")
        ec3.metric("EPR Status",
                   p2.get("epr_applicable", "Not answered"))
        ec4.metric("Sourcing Procedure",
                   p2.get("has_sourcing_procedure", "Not answered"))

    # ── LEADERSHIP SUMMARY ────────────────────────────────────────────────
    with st.container(border=True):
        st.markdown("#### 🟡 Leadership Indicators Summary")
        lc1, lc2, lc3, lc4, lc5 = st.columns(5)
        lc1.metric("LCA Entries", len(st.session_state.lca_entries))
        lc2.metric("Risk Entries", len(st.session_state.risk_entries))
        lc3.metric("Recycled Input %",
                   f"{p2.get('recycled_input_cur', 0)}%")
        reclaimed_filled = any(
            p2.get(f"l4_{k}_reused_cur", 0) or p2.get(f"l4_{k}_recycled_cur", 0) or
            p2.get(f"l4_{k}_disposed_cur", 0)
            for k in ("plastics", "ewaste", "hazardous", "other"))
        lc4.metric("Reclaimed MT",
                   "Done" if reclaimed_filled else "Not filled")
        lc5.metric("Reclaimed Categories",
                   len(st.session_state.reclaimed_categories))

    # ── RECOMMENDATIONS ───────────────────────────────────────────────────
    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### 💡 Recommendations")
        recs = 0

        if p2.get("capex_sustain", 0) == 0 and not p2.get("dna_rd"):
            react_warn(
                "Zero sustainability investment. Even switching to LED lights "
                "counts. Document any energy or waste saving investment."
            )
            recs += 1

        if p2.get("has_sourcing_procedure") == "No":
            react_bad(
                "No sustainable sourcing procedure. Write one simple rule "
                "and document it."
            )
            recs += 1

        if (p2.get("epr_applicable") == "Yes" and
                p2.get("epr_pcb_aligned") == "Not yet submitted to PCB"):
            react_bad(
                "EPR plan not submitted to PCB — address this immediately."
            )
            recs += 1

        if not st.session_state.lca_entries and p2.get("lca_done") == "Yes":
            react_warn("You said LCA was done but no entries added. "
                       "Go to Step 5 L1 and add your LCA details.")
            recs += 1

        if not st.session_state.risk_entries:
            react_warn(
                "No product risks documented. Even one entry shows "
                "self-awareness and earns leadership indicator credit."
            )
            recs += 1

        if recs == 0:
            react_good("No major gaps in P2! Proceed to Principle 3.")

    # ── BANK READY SCORE ──────────────────────────────────────────────────
    st.markdown("---")
    with st.container(border=True):
        st.markdown("#### 🏦 Bank-Ready Score for P2")

        bank_score = 0
        bank_items = []

        if p2.get("capex_sustain", 0) > 0:
            bank_score += 20
            bank_items.append(("✅ Sustainability investment documented", "+20"))
        else:
            bank_items.append(("❌ No sustainability investment", "+0"))

        if p2.get("has_sourcing_procedure") == "Yes":
            bank_score += 20
            bank_items.append(("✅ Sustainable sourcing procedure in place", "+20"))
        elif p2.get("has_sourcing_procedure") == \
                "Informal — we do it but haven't written it down":
            bank_score += 10
            bank_items.append(("🔄 Informal sourcing — not yet documented", "+10"))
        else:
            bank_items.append(("❌ No sourcing procedure", "+0"))

        if p2.get("epr_applicable") == "No":
            bank_score += 20
            bank_items.append(("✅ EPR not applicable — clearly documented", "+20"))
        elif p2.get("epr_pcb_aligned") == "Yes — fully aligned":
            bank_score += 20
            bank_items.append(("✅ EPR compliant — plan submitted to PCB", "+20"))
        elif p2.get("epr_applicable") == "Yes":
            bank_score += 10
            bank_items.append(("🔄 EPR applicable but not fully aligned", "+10"))
        else:
            bank_items.append(("❌ EPR status unclear", "+0"))

        if st.session_state.lca_entries:
            bank_score += 20
            bank_items.append(
                (f"✅ LCA conducted for "
                 f"{len(st.session_state.lca_entries)} product(s)", "+20"))
        else:
            bank_items.append(("⚪ No LCA conducted", "+0"))

        if st.session_state.risk_entries:
            bank_score += 20
            bank_items.append(
                (f"✅ {len(st.session_state.risk_entries)} product risk(s) "
                 "documented with mitigation actions", "+20"))
        else:
            bank_items.append(("⚠️ No product risks documented", "+0"))

        for item, pts in bank_items:
            st.markdown(f"{item} &nbsp;&nbsp; `{pts} points`")

        st.markdown("")
        bank_colour = ("green" if bank_score >= 70
                       else "orange" if bank_score >= 40 else "red")
        st.markdown(
            f"**Bank-Ready Score: "
            f"<span style='color:{bank_colour}'>{bank_score}/100</span>**",
            unsafe_allow_html=True
        )

        if bank_score >= 70:
            st.success(
                "🏦 Strong sustainability profile. "
                "You are likely eligible for green loan schemes "
                "from SBI, Bank of Baroda, and SIDBI."
            )
        elif bank_score >= 40:
            st.warning(
                "🏦 Moderate profile. Document sourcing and waste management "
                "to improve significantly."
            )
        else:
            st.error(
                "🏦 Weak sustainability profile. "
                "Focus on sustainable sourcing and EPR compliance first."
            )

    # ── SAVE ──────────────────────────────────────────────────────────────
    st.markdown("---")
    cf1, cf2, cf3 = st.columns([1, 2, 1])
    with cf2:
        if st.button(
            "💾 Save P2 & Move to Principle 3 →",
            type="primary", use_container_width=True
        ):
            st.session_state.c_p2 = p2
            st.balloons()
            st.success(
                "✅ Principle 2 saved! "
                "Next: Principle 3 — Employee & Worker Wellbeing."
            )

    c_back2, _, _ = st.columns([1, 2, 1])
    with c_back2:
        if st.button("← Back to Leadership", use_container_width=True):
            go(5); st.rerun()
           
 # ─── BOTTOM NAVIGATION ──────────────────────────────────────────────────
from business_profile import render_section_navigation
render_section_navigation("Principle 2")