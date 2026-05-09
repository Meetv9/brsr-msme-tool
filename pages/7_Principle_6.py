import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BRSR P6 | Environment",
    page_icon="🌿",
    layout="centered"
)

# ─────────────────────────────────────────────────────────────────────────────
# CONVERSION CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
ELECTRICITY_RATE_PER_UNIT = 8.0
KWH_TO_MJ = 3.6
KWH_TO_GJ = 0.0036
DIESEL_KWH_PER_LITRE = 9.9
DIESEL_CO2_PER_LITRE = 2.68
GRID_CO2_PER_KWH = 0.82
TANKER_LITRES = 5000
LITRES_TO_KL = 0.001
LPG_CO2_PER_KG = 2.98
LITRES_PER_PERSON_PER_DAY = 40  # Standard MSME water benchmark

# ─────────────────────────────────────────────────────────────────────────────
# ESTIMATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def estimate_units_from_bill(monthly_bill_rs):
    return monthly_bill_rs / ELECTRICITY_RATE_PER_UNIT

def kwh_to_gj(kwh):
    return round(kwh * KWH_TO_GJ, 4)

def kwh_to_mj(kwh):
    return round(kwh * KWH_TO_MJ, 2)

def diesel_to_co2_tonnes(litres):
    return round((litres * DIESEL_CO2_PER_LITRE) / 1000, 4)

def electricity_to_co2_tonnes(kwh):
    return round((kwh * GRID_CO2_PER_KWH) / 1000, 4)

def tankers_to_kl(tankers_per_month, months=12):
    return round((tankers_per_month * TANKER_LITRES * months) * LITRES_TO_KL, 2)

def intensity(value, turnover):
    if turnover and turnover > 0:
        return round(value / turnover, 8)
    return None

def estimate_prev_year(current_value, pct_change=10):
    return round(current_value * (1 - pct_change/100), 2)

def money_saved_from_reduction(current_kwh, target_pct_reduction):
    saved_kwh = current_kwh * (target_pct_reduction / 100)
    return round(saved_kwh * ELECTRICITY_RATE_PER_UNIT, 2)

def estimate_water_from_workers(workers, working_days):
    """Standard MSME estimation: workers × 40 litres × days ÷ 1000 = kL/year"""
    return round((workers * LITRES_PER_PERSON_PER_DAY * working_days) / 1000, 2)

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
    .money-box {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border: 2px solid #66bb6a; border-radius: 14px;
        padding: 16px 20px; text-align: center; margin: 12px 0;
    }
    .estimation-box {
        background: #fff3e0; border: 2px dashed #ff9800;
        border-radius: 12px; padding: 14px 18px; margin: 10px 0;
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
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE — All keys initialized
# ─────────────────────────────────────────────────────────────────────────────
if "p6_mode" not in st.session_state:
    st.session_state.p6_mode = None
if "p6_quick_step" not in st.session_state:
    st.session_state.p6_quick_step = 1
if "p6_full_step" not in st.session_state:
    st.session_state.p6_full_step = 1
if "p6" not in st.session_state:
    st.session_state.p6 = {
        "electricity_kwh_yr": 0,
        "diesel_litres_yr": 0,
        "water_kl_yr": 0,
        "scope1_co2": 0,
        "scope2_co2": 0,
        "waste_tracked": False,
        "pcb_compliant": "",
        "env_compliant": "",
        "green_efforts": "",
        "green_preset": [],
        "zld": "No",
        "turnover_rs": 0,
        "water_estimated": False,
        "total_waste_kg_yr": 0,
        "monthly_bill": 0,
    }

p6 = st.session_state.p6

# Pre-fill turnover from Section A
sec_a = st.session_state.get("data", {})
if "turnover_lakhs" not in p6 and sec_a.get("turnover_lakhs"):
    p6["turnover_lakhs"] = sec_a["turnover_lakhs"]
    p6["turnover_rs"] = sec_a["turnover_lakhs"] * 100000

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

def money(title, amount):
    st.markdown(
        f'<div class="money-box">'
        f'<div style="font-size:13px;color:#2e7d32;">{title}</div>'
        f'<div style="font-size:28px;font-weight:700;color:#1b5e20;">₹{amount:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

def badge_e():
    st.markdown('<span class="essential-badge">🔴 Essential</span>',
                unsafe_allow_html=True)

def badge_l():
    st.markdown('<span class="leadership-badge">🟡 Leadership</span>',
                unsafe_allow_html=True)

def next_q():
    st.session_state.p6_quick_step += 1

def prev_q():
    st.session_state.p6_quick_step -= 1

def next_f():
    st.session_state.p6_full_step += 1

def prev_f():
    st.session_state.p6_full_step -= 1

# ─────────────────────────────────────────────────────────────────────────────
# BANK SCORE (PCB Cert + Env Law Compliance counted SEPARATELY)
# ─────────────────────────────────────────────────────────────────────────────
def calc_p6_score():
    score = 0
    if p6.get("electricity_kwh_yr", 0) > 0:      score += 10
    if p6.get("water_kl_yr", 0) > 0:              score += 10
    if p6.get("scope1_co2", 0) >= 0:              score += 5
    if p6.get("scope2_co2", 0) >= 0:              score += 5
    if p6.get("waste_tracked") or p6.get("waste_full"): score += 10
    if p6.get("pcb_compliant", "").startswith("Yes"): score += 15
    if p6.get("env_compliant", "").startswith("Yes"): score += 15
    if p6.get("green_efforts", "").strip() or p6.get("green_preset"): score += 15
    if p6.get("zld") == "Yes":                    score += 5
    if p6.get("turnover_rs", 0) > 0:              score += 10
    return min(score, 100)

# ─────────────────────────────────────────────────────────────────────────────
# MODE SELECTION
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.p6_mode is None:

    st.markdown("## 🌿 Principle 6 — Environment")
    st.markdown(
        "**Businesses should respect and make efforts "
        "to protect and restore the environment.**"
    )
    st.markdown("")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="mode-card">
            <div style="font-size:40px">⚡</div>
            <div style="font-size:20px;font-weight:700;color:#2e7d32;">Quick Mode</div>
            <div style="font-size:14px;color:#555;margin-top:8px;">
                8 simple questions<br>
                Uses your electricity bills<br>
                Calculates emissions automatically<br>
                Under 10 minutes
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Quick Mode ⚡",
                     use_container_width=True, type="primary"):
            st.session_state.p6_mode = "quick"
            st.rerun()

    with c2:
        st.markdown("""
        <div class="mode-card">
            <div style="font-size:40px">📋</div>
            <div style="font-size:20px;font-weight:700;color:#1565c0;">Full Mode</div>
            <div style="font-size:14px;color:#555;margin-top:8px;">
                All 12 Essential + 9 Leadership<br>
                Complete SEBI tables<br>
                Scope 1, 2 & 3 emissions<br>
                For consultants or serious users
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Full Mode 📋",
                     use_container_width=True):
            st.session_state.p6_mode = "full"
            st.rerun()

    st.info(
        "💡 **You don't need technical data.** "
        "Just your electricity bill and basic waste information. "
        "We calculate everything else for you."
    )
    st.stop()

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    mode_label = "⚡ Quick Mode" if st.session_state.p6_mode == "quick" else "📋 Full Mode"
    st.markdown(f"## 🌿 Principle 6 — Environment &nbsp; `{mode_label}`")
with col_h2:
    if st.button("Switch Mode"):
        st.session_state.p6_mode = None
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# QUICK MODE
# ═════════════════════════════════════════════════════════════════════════════
if st.session_state.p6_mode == "quick":

    TOTAL = 8
    step = st.session_state.p6_quick_step

    st.markdown(
        f'<div style="font-size:13px;color:#666;">'
        f'Question {min(step, TOTAL)} of {TOTAL}</div>',
        unsafe_allow_html=True
    )
    st.progress(min(step, TOTAL) / TOTAL)
    st.markdown("")

    # ── Q1: ELECTRICITY BILL ──────────────────────────────────────────────
    if step == 1:
        st.markdown("### ⚡ What is your average monthly electricity bill?")
        why(
            "Lower electricity = lower costs + better ESG score. "
            "Every ₹1,000 reduction in monthly bill = ₹12,000 saved per year. "
            "Banks and large buyers check your energy efficiency."
        )
        example(
            "A small factory paying ₹15,000/month electricity bill = "
            "approximately 1,875 units/month = 22,500 units/year."
        )

        st.markdown(
            '<div class="estimation-box">'
            '<b>🔧 We estimate your energy data from your bill.</b> '
            'You don\'t need to know "Joules" or "kWh". '
            'Just enter your monthly bill amount.'
            '</div>',
            unsafe_allow_html=True
        )

        monthly_bill = st.number_input(
            "Average monthly electricity bill (₹)",
            min_value=0,
            value=p6.get("monthly_bill", 0),
            help="Check your last 3 months' bills and take the average."
        )
        p6["monthly_bill"] = monthly_bill

        if monthly_bill > 0:
            monthly_units = estimate_units_from_bill(monthly_bill)
            yearly_units = monthly_units * 12
            yearly_gj = kwh_to_gj(yearly_units)
            scope2 = electricity_to_co2_tonnes(yearly_units)

            p6["electricity_kwh_yr"] = yearly_units
            p6["electricity_gj_yr"] = yearly_gj
            p6["scope2_co2"] = scope2

            calc(
                f"Monthly: ~{monthly_units:,.0f} units (kWh) | "
                f"Yearly: ~{yearly_units:,.0f} kWh | "
                f"{yearly_gj:,.2f} GJ"
            )

            st.info(
                f"🌍 **Your estimated Scope 2 emissions** "
                f"(from electricity): **{scope2:.2f} tonnes CO₂** per year"
            )

            potential_saving = money_saved_from_reduction(yearly_units, 10)
            st.markdown(
                f'<div class="money-box">'
                f'<div style="font-size:13px;color:#2e7d32;">'
                f'💡 If you reduce electricity by just 10%...</div>'
                f'<div style="font-size:24px;font-weight:700;color:#1b5e20;">'
                f'You save ₹{potential_saving:,.0f}/year</div>'
                f'<div style="font-size:12px;color:#555;">LED lights + scheduled '
                f'machine shutdowns can easily achieve this</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            if yearly_units > 100000:
                warn(
                    "High energy usage. Check if you qualify for the PAT Scheme "
                    "(Performance, Achieve and Trade) for energy efficiency incentives."
                )
            else:
                good("Energy usage is within typical MSME range.")

        _, c_next = st.columns([1, 1])
        with c_next:
            if st.button("Next →", type="primary",
                         use_container_width=True,
                         disabled=(monthly_bill == 0)):
                next_q(); st.rerun()

    # ── Q2: FUEL USAGE ────────────────────────────────────────────────────
    elif step == 2:
        st.markdown("### ⛽ Do you use diesel, petrol, or LPG at your business?")
        why(
            "Fuel costs money AND creates emissions (called Scope 1). "
            "Tracking this helps you find cost savings. "
            "Diesel generators are the biggest avoidable expense for most MSMEs."
        )
        example(
            "Generator runs for 4 hours/day × 25 days/month = "
            "100 hours/month. At 1 litre/hour = 100 litres/month. "
            "Annual = 1,200 litres diesel."
        )

        uses_fuel = st.radio(
            "Does your business use diesel, petrol, or LPG?",
            ["No — we only use grid electricity",
             "Yes — we use diesel/petrol (generator or vehicle)",
             "Yes — we use LPG/PNG for cooking or heating"],
            index=["No — we only use grid electricity",
                   "Yes — we use diesel/petrol (generator or vehicle)",
                   "Yes — we use LPG/PNG for cooking or heating"].index(
                p6.get("fuel_type", "No — we only use grid electricity")
            )
        )
        p6["fuel_type"] = uses_fuel

        if uses_fuel.startswith("Yes — we use diesel"):
            diesel_monthly = st.number_input(
                "Approximately how many litres of diesel/petrol per month?",
                min_value=0,
                value=p6.get("diesel_monthly", 0),
                help="Check fuel receipts or estimate from generator running hours."
            )
            p6["diesel_monthly"] = diesel_monthly
            diesel_yearly = diesel_monthly * 12
            p6["diesel_litres_yr"] = diesel_yearly
            scope1 = diesel_to_co2_tonnes(diesel_yearly)
            p6["scope1_co2"] = scope1
            fuel_cost = diesel_yearly * 90

            if diesel_yearly > 0:
                calc(
                    f"Yearly diesel: {diesel_yearly:,} litres | "
                    f"Scope 1 emissions: {scope1:.3f} tonnes CO₂"
                )
                money("Annual diesel cost estimate", fuel_cost)

                if scope1 > 5:
                    warn(
                        f"High diesel emissions ({scope1:.1f} tonnes CO₂). "
                        "Consider reducing generator hours or switching to solar."
                    )

        elif uses_fuel.startswith("Yes — we use LPG"):
            lpg_monthly = st.number_input(
                "How many kg of LPG per month?",
                min_value=0,
                value=p6.get("lpg_monthly", 0)
            )
            p6["lpg_monthly"] = lpg_monthly
            lpg_yearly = lpg_monthly * 12
            scope1_lpg = round((lpg_yearly * LPG_CO2_PER_KG) / 1000, 4)
            p6["scope1_co2"] = scope1_lpg
            p6["lpg_kg_yr"] = lpg_yearly
            if lpg_yearly > 0:
                calc(
                    f"Yearly LPG: {lpg_yearly} kg | "
                    f"Scope 1 emissions: {scope1_lpg:.3f} tonnes CO₂"
                )
        else:
            p6["scope1_co2"] = 0
            p6["diesel_litres_yr"] = 0
            good("No direct fuel use — zero Scope 1 emissions. Excellent.")

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q3: WATER USAGE (with NEW Estimation Option) ─────────────────────
    elif step == 3:
        st.markdown("### 💧 Where does your water come from and how much do you use?")
        why(
            "Water tracking helps you find leaks and reduce tanker costs. "
            "In Gujarat, water scarcity is a real risk. "
            "MSMEs that track water use qualify for water conservation subsidies."
        )
        example(
            "A small factory uses 2 borewells + 1 tanker every 2 weeks. "
            "Tanker = 5,000 litres × 2/month = 10,000 litres/month tanker + borewell estimate."
        )

        # NEW FEATURE: Estimation mode toggle
        estimate_mode = st.radio(
            "How do you want to enter water usage?",
            ["I know my water usage (bills / tanker / borewell data)",
             "I don't know — help me estimate"],
            index=0 if not p6.get("water_estimated") else 1,
            help="Choose 'I don't know' if you have no meter or bill data."
        )

        # ── OPTION A: USER KNOWS THEIR WATER USAGE ────────────────────────
        if estimate_mode == "I know my water usage (bills / tanker / borewell data)":
            p6["water_estimated"] = False

            water_source = st.multiselect(
                "What are your water sources? (select all that apply)",
                ["Borewell / Groundwater",
                 "Municipal / Government supply",
                 "Water tanker",
                 "Rainwater harvesting",
                 "River / Surface water",
                 "Other"],
                default=p6.get("water_sources", ["Borewell / Groundwater"])
            )
            p6["water_sources"] = water_source

            total_water_kl = 0

            if "Borewell / Groundwater" in water_source:
                borewell_monthly = st.number_input(
                    "Borewell — estimated monthly usage (kilolitres)",
                    min_value=0.0,
                    value=float(p6.get("borewell_kl_month", 0.0)),
                    help="1 kilolitre = 1000 litres. "
                         "If you don't know, estimate: "
                         "small factory = 5-20 KL/month."
                )
                p6["borewell_kl_month"] = borewell_monthly
                total_water_kl += borewell_monthly * 12

            if "Municipal / Government supply" in water_source:
                muni_monthly = st.number_input(
                    "Municipal supply — monthly (kilolitres)",
                    min_value=0.0,
                    value=float(p6.get("municipal_kl_month", 0.0))
                )
                p6["municipal_kl_month"] = muni_monthly
                total_water_kl += muni_monthly * 12

            if "Water tanker" in water_source:
                tankers_monthly = st.number_input(
                    "Water tankers — how many per month?",
                    min_value=0,
                    value=p6.get("tankers_per_month", 0),
                    help="Each tanker holds approximately 5,000 litres = 5 kilolitres."
                )
                p6["tankers_per_month"] = tankers_monthly
                tanker_kl = tankers_to_kl(tankers_monthly)
                total_water_kl += tanker_kl
                if tankers_monthly > 0:
                    tanker_cost = tankers_monthly * 12 * 800
                    money("Annual tanker cost estimate", tanker_cost)
                    warn(
                        "Reducing tanker dependency saves money. "
                        "Rainwater harvesting can pay back in 1-2 years."
                    )

            p6["water_kl_yr"] = round(total_water_kl, 2)

            if total_water_kl > 0:
                calc(
                    f"Total estimated water use: {total_water_kl:,.1f} kilolitres/year "
                    f"({total_water_kl * 1000:,.0f} litres)"
                )

                turnover = p6.get("turnover_rs", 0)
                if turnover > 0:
                    w_intensity = intensity(total_water_kl, turnover)
                    st.caption(
                        f"Water intensity: {w_intensity:.8f} kL per ₹ turnover"
                    )

        # ── OPTION B: USER DOESN'T KNOW — ESTIMATE FROM WORKERS ───────────
        else:
            p6["water_estimated"] = True

            st.warning(
                "📘 No problem! We will estimate your yearly water usage using "
                "the standard MSME benchmark — **40 litres per person per day**."
            )

            # Pre-fill workers from Section A if available
            default_workers = (
                p6.get("water_workers") or
                sec_a.get("total_perm_emp", 0) +
                sec_a.get("total_perm_wkr", 0) or 10
            )

            wc1, wc2 = st.columns(2)
            with wc1:
                workers = st.number_input(
                    "How many people work in your business daily?",
                    min_value=0,
                    value=int(default_workers),
                    help="Include all employees + workers who come daily."
                )
                p6["water_workers"] = workers

            with wc2:
                working_days = st.number_input(
                    "Working days per year",
                    min_value=0,
                    max_value=365,
                    value=p6.get("water_working_days", 300),
                    help="Typical: 300 days (excluding Sundays + holidays)."
                )
                p6["water_working_days"] = working_days

            estimated_kl = estimate_water_from_workers(workers, working_days)
            p6["water_kl_yr"] = estimated_kl

            calc(
                f"Estimation: {workers} people × 40 litres × {working_days} days "
                f"= {estimated_kl:,.2f} kilolitres/year"
            )

            st.info(
                "💡 This is a standard MSME estimation method used when "
                "no meter or bill data is available. You can refine this "
                "later by adding actual borewell or tanker data."
            )

            turnover = p6.get("turnover_rs", 0)
            if turnover > 0 and estimated_kl > 0:
                w_intensity = intensity(estimated_kl, turnover)
                st.caption(
                    f"Water intensity (estimated): "
                    f"{w_intensity:.8f} kL per ₹ turnover"
                )

        # ── ZLD QUESTION (applies in both modes) ──────────────────────────
        st.markdown("---")
        p6["zld"] = st.radio(
            "Do you have Zero Liquid Discharge (ZLD) — meaning you don't "
            "let any wastewater flow outside your premises?",
            ["No", "Yes", "Partially"],
            horizontal=True,
            index=["No", "Yes", "Partially"].index(
                p6.get("zld", "No")
            )
        )

        if p6["zld"] == "Yes":
            good(
                "ZLD implemented — excellent. This is a major positive for "
                "pollution board compliance and large buyer audits."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q4: WASTE ─────────────────────────────────────────────────────────
    elif step == 4:
        st.markdown("### 🗑️ What waste does your business generate?")
        why(
            "Tracking waste can generate income. Metal scrap, plastic waste, "
            "and packaging can be sold to kabadiwala for extra revenue. "
            "Proper documentation also protects you from pollution board penalties."
        )
        example(
            "A garment factory generates fabric off-cuts, plastic packaging, "
            "and old machine parts. Selling fabric scraps to rag dealers = "
            "₹2,000-5,000/month extra income."
        )

        waste_types = st.multiselect(
            "What types of waste does your business generate?",
            ["Plastic / Packaging waste",
             "Metal scrap / Machine parts",
             "Fabric / Textile waste",
             "Food waste",
             "Paper / Cardboard",
             "E-waste (old electronics, batteries)",
             "Chemicals / Solvents (Hazardous)",
             "Construction / Renovation waste",
             "Other"],
            default=p6.get("waste_types", [])
        )
        p6["waste_types"] = waste_types

        waste_data = {}
        total_waste_kg = 0

        for wtype in waste_types:
            col1, col2 = st.columns(2)
            with col1:
                kg = st.number_input(
                    f"{wtype} — approx kg per month",
                    min_value=0,
                    value=p6.get(f"waste_{wtype}_kg", 0),
                    key=f"waste_q_{wtype}"
                )
                p6[f"waste_{wtype}_kg"] = kg
                total_waste_kg += kg * 12
            with col2:
                method = st.selectbox(
                    f"How do you dispose of it?",
                    ["Sold to scrap/kabadiwala",
                     "Authorised recycler",
                     "Municipal garbage collection",
                     "Composting",
                     "PCB authorised disposal",
                     "Not yet managed"],
                    key=f"method_q_{wtype}"
                )
                waste_data[wtype] = {"kg_month": kg, "method": method}

        p6["waste_data"] = waste_data
        p6["total_waste_kg_yr"] = total_waste_kg
        p6["waste_tracked"] = len(waste_types) > 0

        if total_waste_kg > 0:
            total_tonnes = round(total_waste_kg / 1000, 3)
            calc(f"Total waste: {total_waste_kg:,} kg/year = {total_tonnes} metric tonnes")

        if "Chemicals / Solvents (Hazardous)" in waste_types:
            bad(
                "Hazardous waste must be disposed through PCB-authorised "
                "waste management company. Non-compliance = ₹1 lakh/day fine."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q5: PCB COMPLIANCE + ENVIRONMENTAL LAW (Q12) ─────────────────────
    elif step == 5:
        st.markdown("### ⚖️ Pollution Certificate & Environmental Law Compliance")
        why(
            "PCB (Pollution Control Board) compliance is the #1 thing "
            "bank auditors and large buyers check. "
            "Having your Consent to Operate (CTO) is essential."
        )
        example(
            "GPCB (Gujarat Pollution Control Board) issues Consent to Operate (CTO). "
            "This is different from your factory license. "
            "If you're not sure, check with your CA or call GPCB helpline."
        )

        # Q1 in this step — PCB Certificate
        st.markdown("#### 1️⃣ Pollution Control Board Certificate")

        with st.expander("📖 What is a PCB Certificate (CTO)? Click to learn"):
            st.markdown("""
**PCB = Pollution Control Board.** In Gujarat, it's called **GPCB**.

**CTO = Consent to Operate.** A legal permission from GPCB that says your
business is allowed to operate without polluting excessively.

**Who needs it?**
- Manufacturing units (factories, workshops, mills)
- Businesses using chemicals, boilers, or generators above certain size
- Food processing, chemical, textile, metal, paper industries

**Who usually doesn't need it?**
- Pure service businesses (consultancy, IT)
- Very small retail shops
- Home-based tailoring or small crafts

**How to check:** Look through your business documents for a certificate
from GPCB, or call the GPCB helpline: **079-23232152**.
            """)

        pcb_options = [
            "Yes — we have valid PCB certificate",
            "No — we don't have it",
            "Not Applicable — our business doesn't require it",
            "Applied and pending"
        ]
        current_pcb = p6.get("pcb_compliant", pcb_options[0])
        if current_pcb not in pcb_options:
            current_pcb = pcb_options[0]
        p6["pcb_compliant"] = st.radio(
            "Does your business have a valid Pollution Control Board "
            "certificate / Consent to Operate (CTO)?",
            pcb_options,
            index=pcb_options.index(current_pcb)
        )

        if p6["pcb_compliant"].startswith("Yes"):
            good(
                "PCB certificate in order — this is critical for bank loans "
                "and large buyer vendor approvals."
            )
            p6["pcb_expiry"] = st.text_input(
                "Certificate expiry date (optional)",
                value=p6.get("pcb_expiry", ""),
                placeholder="e.g. March 2026"
            )
        elif p6["pcb_compliant"].startswith("No"):
            bad(
                "No PCB certificate. This is a legal requirement for most "
                "manufacturing businesses. Contact GPCB immediately. "
                "Non-compliance can result in factory closure orders."
            )

        # Q2 in this step — Environmental Law Compliance (BRSR Q12)
        st.markdown("---")
        st.markdown("#### 2️⃣ Environmental Law Compliance (BRSR Q12)")
        why(
            "These three laws are the main environmental laws in India. "
            "Being compliant protects you from pollution board fines, "
            "factory closure notices, and loss of bank loans."
        )

        with st.expander("📖 What do these laws mean in simple words? Click to learn"):
            st.markdown("""
**💧 Water Act (Water Prevention & Control of Pollution Act, 1974)**
Prevents water pollution from your business. If you discharge any wastewater,
it should not pollute rivers, lakes, or groundwater.
*Example: Textile factory washing fabric should treat dirty water before releasing.*

**🌫️ Air Act (Air Prevention & Control of Pollution Act, 1981)**
Controls air pollution from your business. Chimneys, generators, boilers,
and dusty operations must follow emission limits.
*Example: Diesel generator exhaust + factory smoke should meet GPCB limits.*

**🌍 Environment Protection Act, 1986**
The umbrella law covering all environmental matters — waste handling,
hazardous chemical storage, noise pollution, and more.
*Example: Oil drums and chemical containers must be stored properly, not dumped.*

**✅ How to check if you're compliant:**
1. Do you have a valid GPCB Consent to Operate (CTO)?
2. Have you received any pollution board notice in the last year?
3. Are you following the conditions mentioned in your CTO?

If Yes to #1 and #3, and No to #2 — you are likely compliant.
            """)

        example(
            "A small garment factory with CTO from GPCB, no pending notices, "
            "and following the conditions in their certificate = Yes, compliant."
        )

        env_options = [
            "Yes — fully compliant",
            "No — there are some non-compliances",
            "Not Sure"
        ]
        current_env = p6.get("env_compliant", env_options[0])
        if current_env not in env_options:
            current_env = env_options[0]
        p6["env_compliant"] = st.radio(
            "Are you compliant with Water Act, Air Act, and Environment "
            "Protection Act?",
            env_options,
            horizontal=True,
            index=env_options.index(current_env)
        )

        if p6["env_compliant"].startswith("Yes"):
            good("Environmental law compliance confirmed.")
        elif p6["env_compliant"].startswith("No"):
            p6["env_noncompliance_desc"] = st.text_area(
                "Describe the non-compliance and corrective action",
                value=p6.get("env_noncompliance_desc", ""),
                height=80,
                placeholder="e.g. Air Act consent pending renewal. "
                            "Applied for renewal in January. Expected by April."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q6: GREEN EFFORTS ─────────────────────────────────────────────────
    elif step == 6:
        st.markdown("### 🌱 What are you doing to be more eco-friendly?")
        why(
            "Documenting even small green initiatives increases your ESG score "
            "significantly. Large buyers reward suppliers who are improving — "
            "not just those who are already perfect."
        )
        example(
            "Switched to LED lights (saves ₹2,000/month). "
            "Installed a rainwater harvesting tank. "
            "Sell all metal scrap to authorized recycler. "
            "Use both sides of paper. Any of these count."
        )

        preset_initiatives = [
            "LED lighting installed",
            "Solar panels installed",
            "Rainwater harvesting",
            "Sell scrap to authorized recycler",
            "Reduced plastic packaging",
            "Switched to energy-efficient machines",
            "Reuse process water",
            "Composting food/organic waste",
        ]

        selected_initiatives = st.multiselect(
            "Select initiatives you have already implemented:",
            preset_initiatives,
            default=p6.get("green_preset", [])
        )
        p6["green_preset"] = selected_initiatives

        p6["green_efforts"] = st.text_area(
            "Any other green efforts not listed above?",
            value=p6.get("green_efforts", ""),
            height=80,
            placeholder="e.g. We have reduced water usage by 20% by fixing "
                        "leaking pipes. We donate unused food to local "
                        "community kitchen."
        )

        all_efforts = selected_initiatives.copy()
        if p6.get("green_efforts", "").strip():
            all_efforts.append(p6["green_efforts"])
        p6["all_green_efforts"] = all_efforts

        if len(all_efforts) >= 3:
            good(
                f"{len(all_efforts)} green initiatives documented — "
                "excellent. This will stand out in your BRSR report."
            )
        elif len(all_efforts) > 0:
            warn(
                f"{len(all_efforts)} initiative(s). Even small things count. "
                "Add more if you think of any."
            )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q7: ECOLOGICALLY SENSITIVE ────────────────────────────────────────
    elif step == 7:
        st.markdown("### 🌳 Is your factory/office near any protected natural area?")
        why(
            "Businesses near forests, rivers, or wildlife sanctuaries have "
            "additional compliance requirements. "
            "If not applicable, just say No — this is a simple Yes/No check."
        )
        example(
            "If your factory is in an industrial area or city — answer No. "
            "If you're near a river, national park, or wetland — answer Yes."
        )

        p6["near_sensitive_area"] = st.radio(
            "Is your factory/office located near any of these: "
            "national park, wildlife sanctuary, river, wetland, forest, "
            "coastal zone?",
            ["No — we are in an industrial/urban area",
             "Yes — we are near a protected area"],
            index=0 if p6.get(
                "near_sensitive_area",
                "No — we are in an industrial/urban area"
            ).startswith("No") else 1
        )

        if p6["near_sensitive_area"].startswith("Yes"):
            p6["sensitive_area_desc"] = st.text_area(
                "Describe the location and what approvals you have",
                value=p6.get("sensitive_area_desc", ""),
                height=80,
                placeholder="e.g. Factory is located 500m from Sabarmati River. "
                            "We have NOC from Gujarat Pollution Control Board "
                            "for operations near water body."
            )
            warn(
                "Operations near sensitive areas require additional approvals. "
                "Ensure your CTO specifically covers this."
            )
        else:
            good("No sensitive area concerns — standard compliance applies.")

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Next →", type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── Q8: TURNOVER FOR INTENSITY ────────────────────────────────────────
    elif step == 8:
        st.markdown("### 📊 One last thing — your annual turnover")
        why(
            "BRSR requires 'energy intensity' and 'water intensity' — "
            "which is just how much energy/water you use per rupee of sales. "
            "We need your turnover to calculate this."
        )
        example(
            "Turnover ₹50 lakhs. Energy = 25,000 kWh. "
            "Energy intensity = 25,000 ÷ 50,00,000 = 0.005 kWh per rupee."
        )

        default_lakhs = p6.get(
            "turnover_lakhs",
            sec_a.get("turnover_lakhs", 0)
        )

        if default_lakhs > 0:
            st.success(
                f"✅ We found turnover of ₹{default_lakhs} lakhs from Section A."
            )

        turnover_lakhs = st.number_input(
            "Annual turnover (₹ Lakhs)",
            min_value=0.0,
            value=float(default_lakhs),
            help="1 Lakh = 1,00,000 rupees"
        )
        p6["turnover_lakhs"] = turnover_lakhs
        p6["turnover_rs"] = turnover_lakhs * 100000

        if turnover_lakhs > 0:
            elec = p6.get("electricity_kwh_yr", 0)
            water = p6.get("water_kl_yr", 0)
            elec_gj = kwh_to_gj(elec)
            turnover_rs = p6["turnover_rs"]

            e_intensity = intensity(elec_gj, turnover_rs)
            w_intensity = intensity(water, turnover_rs)

            p6["energy_intensity"] = e_intensity
            p6["water_intensity"] = w_intensity

            if e_intensity:
                calc(
                    f"Energy intensity: {e_intensity:.8f} GJ per ₹ turnover | "
                    f"Water intensity: {w_intensity:.8f} kL per ₹"
                )

        c_back, c_next = st.columns(2)
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_q(); st.rerun()
        with c_next:
            if st.button("Finish & See Results 🎉",
                         type="primary", use_container_width=True):
                next_q(); st.rerun()

    # ── QUICK SUMMARY (FIXED INDENTATION) ─────────────────────────────────
    elif step > 8:

        st.balloons()

        st.markdown(
            '<div class="section-win">'
            '<div style="font-size:48px">🎉</div>'
            '<div style="font-size:22px;font-weight:700;color:#1b5e20;">'
            'P6 Quick Mode Complete!</div>'
            '<div style="font-size:14px;color:#2e7d32;margin-top:8px;">'
            'Your factory\'s environmental profile is ready.'
            '</div></div>',
            unsafe_allow_html=True
        )

        score = calc_p6_score()
        colour = ("green" if score >= 70
                  else "orange" if score >= 40 else "red")
        st.markdown(
            f"<h2 style='color:{colour};text-align:center'>{score}/100</h2>"
            "<p style='text-align:center;color:gray'>Environmental Score</p>",
            unsafe_allow_html=True
        )
        st.progress(score / 100)

        st.markdown("---")
        st.markdown("### Your Environmental Summary")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Electricity/year",
                  f"{p6.get('electricity_kwh_yr', 0):,.0f} kWh")

        water_label = "Water/year"
        if p6.get("water_estimated"):
            water_label = "Water/year (est.)"
        m2.metric(water_label,
                  f"{p6.get('water_kl_yr', 0):,.1f} kL")

        scope1 = p6.get("scope1_co2", 0)
        scope2 = p6.get("scope2_co2", 0)
        m3.metric("Scope 1 + 2",
                  f"{round(scope1 + scope2, 3)} tCO₂")
        m4.metric("PCB Compliant",
                  "✅" if p6.get("pcb_compliant", "").startswith("Yes") else "❌")

        # Savings opportunity
        st.markdown("---")
        st.markdown("### 💰 Your Green Savings Opportunity")
        elec = p6.get("electricity_kwh_yr", 0)
        if elec > 0:
            saving_10 = money_saved_from_reduction(elec, 10)
            saving_20 = money_saved_from_reduction(elec, 20)
            sc1, sc2 = st.columns(2)
            with sc1:
                money("Saved by reducing electricity 10%", saving_10)
            with sc2:
                money("Saved by reducing electricity 20%", saving_20)
            st.caption(
                "💡 Switching to LED lights alone typically reduces electricity by 15-20%."
            )

        # ── SMART RECOMMENDATIONS (FIXED — properly indented inside elif) ──
        st.markdown("---")
        st.markdown("### 🎯 Smart Recommendations Based On Your Data")

        smart_recs = 0

        elec_check = p6.get("electricity_kwh_yr", 0)
        if elec_check > 50000:
            warn("High electricity use. Consider LED lights + Variable Frequency "
                 "Drives (VFD) for motors. Payback in 1-2 years.")
            smart_recs += 1

        diesel_check = p6.get("diesel_litres_yr", 0)
        if diesel_check > 1000:
            warn("High diesel use. Rooftop solar can reduce generator dependency "
                 "by 60-80%. Gujarat has one of the best solar subsidies in India.")
            smart_recs += 1

        water_check = p6.get("water_kl_yr", 0)
        if water_check > 500:
            warn("High water consumption. Rainwater harvesting typically pays "
                 "back in 18-24 months. Contact GEDA for subsidy info.")
            smart_recs += 1

        total_waste_check = p6.get("total_waste_kg_yr", 0)
        if total_waste_check > 1000:
            good("You generate good scrap volume. Partner with authorized "
                 "recyclers to generate extra income from waste.")
            smart_recs += 1

        if smart_recs == 0:
            good("Your usage levels are within healthy MSME ranges. "
                 "Keep tracking month-over-month to spot any creeping increases.")

        # ── WHAT TO DO NEXT (compliance gaps) ──
        st.markdown("---")
        st.markdown("### What To Do Next")

        recs = 0
        if not p6.get("pcb_compliant", "").startswith("Yes"):
            bad("Get your PCB Consent to Operate — highest priority.")
            recs += 1
        if not p6.get("env_compliant", "").startswith("Yes"):
            bad("Confirm compliance with Water/Air/Environment Acts.")
            recs += 1
        if not p6.get("waste_tracked"):
            warn("Document your waste. Even a simple scrap register helps.")
            recs += 1
        if not p6.get("green_preset") and not p6.get("green_efforts", "").strip():
            warn("Document at least 1-2 green initiatives you already do.")
            recs += 1
        if p6.get("zld") == "No" and "Chemicals / Solvents (Hazardous)" in p6.get("waste_types", []):
            bad("Hazardous waste + no ZLD = high compliance risk.")
            recs += 1
        if recs == 0:
            good("Strong environmental profile! No major gaps.")

        st.markdown("---")
        op1, op2 = st.columns(2)
        with op1:
            if st.button("📋 Switch to Full Mode",
                         use_container_width=True):
                st.session_state.p6_mode = "full"
                st.rerun()
        with op2:
            if st.button("💾 Save & Move to P7 →",
                         use_container_width=True, type="primary"):
                st.session_state.c_p6 = p6
                st.success("✅ P6 saved! Next: Principle 7 — Policy Advocacy.")

# ═════════════════════════════════════════════════════════════════════════════
# FULL MODE
# ═════════════════════════════════════════════════════════════════════════════
else:

    full_step = st.session_state.p6_full_step

    full_steps = {
        1: "⚡ Energy",
        2: "💧 Water",
        3: "🌫️ Emissions",
        4: "🗑️ Waste",
        5: "⚖️ Compliance",
        6: "🏆 Leadership",
        7: "✅ Summary"
    }

    nav = st.columns(7)
    for i, (num, label) in enumerate(full_steps.items()):
        with nav[i]:
            t = "primary" if full_step == num else "secondary"
            if st.button(label, key=f"fn6_{num}",
                         type=t, use_container_width=True):
                st.session_state.p6_full_step = num
                st.rerun()

    st.progress(full_step / len(full_steps))
    st.markdown("---")

    # ── FULL STEP 1: ENERGY ───────────────────────────────────────────────
    if full_step == 1:
        st.header("⚡ Energy Consumption (Essential Q1-Q2)")
        badge_e()

        st.markdown(
            '<div class="estimation-box">'
            '<b>🔧 Estimation Mode:</b> '
            'Enter your electricity bill and diesel usage. '
            'We convert to Joules/GJ automatically. '
            'Or enter kWh directly if you have meter readings.'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(border=True):
            st.markdown("#### Option A — Enter from Bills (Recommended for MSMEs)")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Current Financial Year**")
                monthly_bill_cur = st.number_input(
                    "Average monthly electricity bill (₹)",
                    min_value=0,
                    value=p6.get("monthly_bill", 0),
                    key="f_bill_cur",
                    help="Check last 12 months bills and average them."
                )
                if monthly_bill_cur > 0:
                    kwh_cur = estimate_units_from_bill(monthly_bill_cur) * 12
                    p6["electricity_kwh_yr"] = kwh_cur
                    st.caption(
                        f"Estimated: {kwh_cur:,.0f} kWh = {kwh_to_gj(kwh_cur):.3f} GJ"
                    )

                diesel_cur = st.number_input(
                    "Total diesel used this year (litres)",
                    min_value=0,
                    value=p6.get("diesel_litres_yr", 0),
                    key="f_diesel_cur"
                )
                p6["diesel_litres_yr"] = diesel_cur
                if diesel_cur > 0:
                    diesel_gj = round(diesel_cur * DIESEL_KWH_PER_LITRE * KWH_TO_GJ, 4)
                    st.caption(f"Diesel energy: {diesel_gj:.3f} GJ")

            with c2:
                st.markdown("**Previous Financial Year**")
                monthly_bill_prev = st.number_input(
                    "Average monthly electricity bill (₹) — Previous FY",
                    min_value=0,
                    value=p6.get("monthly_bill_prev", 0),
                    key="f_bill_prev"
                )
                if monthly_bill_prev == 0 and monthly_bill_cur > 0:
                    if st.button("📊 Estimate from Current Year"):
                        p6["monthly_bill_prev"] = int(
                            monthly_bill_cur * 0.9
                        )
                        st.rerun()
                    st.caption("Click above to estimate previous year as -10% of current")

                if monthly_bill_prev > 0:
                    kwh_prev = estimate_units_from_bill(monthly_bill_prev) * 12
                    p6["electricity_kwh_prev"] = kwh_prev
                    st.caption(
                        f"Estimated: {kwh_prev:,.0f} kWh = {kwh_to_gj(kwh_prev):.3f} GJ"
                    )

                diesel_prev = st.number_input(
                    "Total diesel used — Previous FY (litres)",
                    min_value=0,
                    value=p6.get("diesel_litres_prev", 0),
                    key="f_diesel_prev"
                )
                p6["diesel_litres_prev"] = diesel_prev

        with st.container(border=True):
            st.markdown("#### Option B — Enter kWh Directly (if you have meter readings)")
            c3, c4 = st.columns(2)
            with c3:
                kwh_direct = st.number_input(
                    "Electricity consumption — Current FY (kWh)",
                    min_value=0.0,
                    value=float(p6.get("electricity_kwh_yr", 0.0)),
                    key="f_kwh_direct"
                )
                if kwh_direct > 0:
                    p6["electricity_kwh_yr"] = kwh_direct
            with c4:
                other_energy = st.number_input(
                    "Energy from other sources — Current FY (kWh)",
                    min_value=0.0,
                    value=float(p6.get("other_energy_kwh", 0.0)),
                    key="f_other_energy",
                    help="Solar panels, biogas, etc."
                )
                p6["other_energy_kwh"] = other_energy

        elec = p6.get("electricity_kwh_yr", 0)
        diesel = p6.get("diesel_litres_yr", 0)
        other = p6.get("other_energy_kwh", 0)
        diesel_kwh_eq = diesel * DIESEL_KWH_PER_LITRE
        total_kwh = elec + diesel_kwh_eq + other
        total_gj = kwh_to_gj(total_kwh)

        p6["total_energy_kwh"] = total_kwh
        p6["total_energy_gj"] = total_gj

        if total_kwh > 0:
            st.markdown("")
            st.markdown("**Auto-Calculated Energy Totals:**")
            em1, em2, em3 = st.columns(3)
            em1.metric("Total Electricity", f"{elec:,.0f} kWh")
            em2.metric("Total Energy", f"{total_gj:.3f} GJ")
            turnover = p6.get("turnover_rs", 0)
            if turnover > 0:
                e_int = intensity(total_gj, turnover)
                em3.metric("Energy Intensity", f"{e_int:.8f} GJ/₹")

        with st.container(border=True):
            badge_e()
            st.markdown("#### PAT Scheme (Essential Q2)")
            st.caption(
                "The PAT Scheme (Performance Achieve Trade) applies to large "
                "energy-intensive industries. Most MSMEs are NOT designated consumers."
            )
            p6["pat_applicable"] = st.radio(
                "Is your business a Designated Consumer under PAT Scheme?",
                ["No — not applicable (most MSMEs)",
                 "Yes — we are under PAT Scheme"],
                horizontal=True,
                index=0 if p6.get(
                    "pat_applicable", "No — not applicable (most MSMEs)"
                ).startswith("No") else 1,
                key="f_pat"
            )

        _, c_next = st.columns([1, 1])
        with c_next:
            if st.button("Next: Water →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 2: WATER ────────────────────────────────────────────────
    elif full_step == 2:
        st.header("💧 Water (Essential Q3-Q4)")
        badge_e()

        with st.container(border=True):
            st.markdown("#### Water Withdrawal by Source (kilolitres)")
            example(
                "1 kilolitre = 1,000 litres. "
                "Monthly borewell pump running 2 hrs/day × 30 days × 5 L/min "
                "= 18,000 litres/month = 18 kL/month = 216 kL/year."
            )

            water_sources_full = [
                ("surface", "Surface Water (river, canal, lake)"),
                ("ground",  "Groundwater (borewell, tubewell)"),
                ("third",   "Third Party (tanker, municipal supply)"),
                ("sea",     "Seawater / Desalinated"),
                ("other",   "Other sources"),
            ]

            wdata = p6.get("water_full", {})
            total_withdrawal_cur = 0
            total_withdrawal_prev = 0

            wh = st.columns(3)
            wh[0].markdown("**Source**")
            wh[1].markdown("**Current FY (kL)**")
            wh[2].markdown("**Previous FY (kL)**")

            for wkey, wlabel in water_sources_full:
                wr = st.columns(3)
                wr[0].markdown(f"*{wlabel}*")
                cur_val = wr[1].number_input(
                    wlabel, min_value=0.0,
                    value=float(wdata.get(f"{wkey}_cur", 0.0)),
                    key=f"f_w_{wkey}_c", label_visibility="collapsed"
                )
                prev_val = wr[2].number_input(
                    wlabel, min_value=0.0,
                    value=float(wdata.get(f"{wkey}_prev", 0.0)),
                    key=f"f_w_{wkey}_p", label_visibility="collapsed"
                )
                wdata[f"{wkey}_cur"] = cur_val
                wdata[f"{wkey}_prev"] = prev_val
                total_withdrawal_cur += cur_val
                total_withdrawal_prev += prev_val

            p6["water_full"] = wdata

            wc = st.columns(2)
            p6["water_consumed_cur"] = wc[0].number_input(
                "Total water CONSUMED (current FY, kL)",
                min_value=0.0,
                value=float(p6.get("water_consumed_cur", total_withdrawal_cur)),
                key="f_wc_cur",
                help="Usually less than or equal to withdrawal. "
                     "Difference = water discharged."
            )
            p6["water_consumed_prev"] = wc[1].number_input(
                "Total water consumed (previous FY, kL)",
                min_value=0.0,
                value=float(p6.get("water_consumed_prev", 0.0)),
                key="f_wc_prev"
            )

            p6["water_kl_yr"] = total_withdrawal_cur

            if total_withdrawal_cur > 0:
                sm1, sm2, sm3 = st.columns(3)
                sm1.metric("Total Withdrawal (Cur)", f"{total_withdrawal_cur:.1f} kL")
                sm2.metric("Total Withdrawal (Prev)", f"{total_withdrawal_prev:.1f} kL")
                turnover = p6.get("turnover_rs", 0)
                if turnover > 0:
                    w_int = intensity(p6["water_consumed_cur"], turnover)
                    sm3.metric("Water Intensity", f"{w_int:.8f} kL/₹")

        with st.container(border=True):
            st.markdown("#### Zero Liquid Discharge (Essential Q4)")
            p6["zld"] = st.radio(
                "Have you implemented Zero Liquid Discharge?",
                ["No", "Yes", "Partially"],
                horizontal=True,
                index=["No", "Yes", "Partially"].index(
                    p6.get("zld", "No")
                ),
                key="f_zld"
            )
            if p6["zld"] != "No":
                p6["zld_desc"] = st.text_area(
                    "Describe ZLD coverage",
                    value=p6.get("zld_desc", ""),
                    height=60,
                    key="f_zld_desc"
                )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Emissions →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 3: EMISSIONS ────────────────────────────────────────────
    elif full_step == 3:
        st.header("🌫️ Emissions — Scope 1, 2 & Air Pollutants (Essential Q5-Q7)")
        badge_e()

        with st.container(border=True):
            st.markdown("#### GHG Emissions (Scope 1 & 2) — Essential Q6")
            st.info(
                "**Scope 1** = Direct emissions from fuel you burn at your site. "
                "**Scope 2** = Indirect emissions from electricity you buy. "
                "We calculate both automatically from your energy data."
            )

            diesel = p6.get("diesel_litres_yr", 0)
            elec = p6.get("electricity_kwh_yr", 0)

            scope1 = diesel_to_co2_tonnes(diesel)
            scope2 = electricity_to_co2_tonnes(elec)
            total_s12 = round(scope1 + scope2, 4)

            p6["scope1_co2"] = scope1
            p6["scope2_co2"] = scope2
            p6["scope12_co2"] = total_s12

            sc = st.columns(3)
            sc[0].metric("Scope 1 (tCO₂e)", f"{scope1:.4f}")
            sc[1].metric("Scope 2 (tCO₂e)", f"{scope2:.4f}")
            sc[2].metric("Total Scope 1+2", f"{total_s12:.4f}")

            turnover = p6.get("turnover_rs", 0)
            if turnover > 0:
                em_int = intensity(total_s12, turnover)
                st.caption(
                    f"Emission intensity: {em_int:.10f} tCO₂ per ₹ turnover"
                )

            st.caption(
                f"Formula: Scope 1 = {diesel} L diesel × {DIESEL_CO2_PER_LITRE} kg/L ÷ 1000 | "
                f"Scope 2 = {elec:,.0f} kWh × {GRID_CO2_PER_KWH} kg/kWh ÷ 1000"
            )

            p6["ghg_reduction_projects"] = st.text_area(
                "Any projects to reduce GHG emissions? (Essential Q7)",
                value=p6.get("ghg_reduction_projects", ""),
                height=60,
                placeholder="e.g. Installing 5KW solar panels (reduces Scope 2 by 30%). "
                            "Replacing diesel generator with grid connection.",
                key="f_ghg_proj"
            )

        with st.container(border=True):
            st.markdown("#### Air Pollutants (Essential Q5)")
            st.caption(
                "NOx, SOx, PM etc. Most MSMEs don't measure these formally. "
                "If you don't have measurements, select 'Data Not Available'."
            )

            dna_air = st.toggle(
                "Data Not Available — we don't measure air pollutants",
                value=p6.get("dna_air", True),
                key="f_dna_air"
            )
            p6["dna_air"] = dna_air

            if not dna_air:
                air_pollutants = ["NOx", "SOx", "Particulate Matter (PM)",
                                  "VOC", "HAP"]
                air_data = p6.get("air_data", {})
                for ap in air_pollutants:
                    ac = st.columns(3)
                    ac[0].markdown(f"*{ap}*")
                    air_data[f"{ap}_cur"] = ac[1].number_input(
                        f"{ap} cur", min_value=0.0,
                        value=float(air_data.get(f"{ap}_cur", 0.0)),
                        key=f"f_air_{ap}_c", label_visibility="collapsed"
                    )
                    ac[2].selectbox(
                        "Unit", ["mg/m³", "kg/year", "tonnes/year"],
                        key=f"f_air_{ap}_u"
                    )
                p6["air_data"] = air_data
            else:
                st.caption(
                    "💡 If you have a diesel generator or industrial "
                    "boiler, a third-party environmental consultant can "
                    "measure these for ₹5,000-15,000."
                )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Waste →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 4: WASTE ────────────────────────────────────────────────
    elif full_step == 4:
        st.header("🗑️ Waste Management (Essential Q8-Q9)")
        badge_e()

        with st.container(border=True):
            st.markdown("#### Waste Generated — Current & Previous Year (metric tonnes)")
            example(
                "1 metric tonne = 1,000 kg. "
                "If you generate 50 kg plastic/month = 600 kg/year = 0.6 metric tonnes."
            )

            waste_categories = [
                ("plastic",    "Plastic Waste (A)"),
                ("ewaste",     "E-waste (B)"),
                ("biomedical", "Bio-medical Waste (C)"),
                ("cd_waste",   "Construction & Demolition (D)"),
                ("battery",    "Battery Waste (E)"),
                ("hazardous",  "Other Hazardous Waste (G)"),
                ("non_haz",    "Other Non-hazardous Waste (H)"),
            ]

            waste_full = p6.get("waste_full", {})
            total_waste_cur = 0

            wh = st.columns(3)
            wh[0].markdown("**Waste Type**")
            wh[1].markdown("**Current FY (MT)**")
            wh[2].markdown("**Previous FY (MT)**")

            for wkey, wlabel in waste_categories:
                wr = st.columns(3)
                wr[0].markdown(f"*{wlabel}*")
                cur_w = wr[1].number_input(
                    wlabel, min_value=0.0, step=0.001,
                    value=float(waste_full.get(f"{wkey}_cur", 0.0)),
                    key=f"f_wst_{wkey}_c", label_visibility="collapsed"
                )
                prev_w = wr[2].number_input(
                    wlabel, min_value=0.0, step=0.001,
                    value=float(waste_full.get(f"{wkey}_prev", 0.0)),
                    key=f"f_wst_{wkey}_p", label_visibility="collapsed"
                )
                waste_full[f"{wkey}_cur"] = cur_w
                waste_full[f"{wkey}_prev"] = prev_w
                total_waste_cur += cur_w

            p6["waste_full"] = waste_full
            p6["total_waste_mt"] = round(total_waste_cur, 4)

            if total_waste_cur > 0:
                st.markdown(f"**Total waste generated: {total_waste_cur:.4f} MT**")

        with st.container(border=True):
            st.markdown("#### Waste Recovery (Recycled/Reused)")
            r1, r2, r3 = st.columns(3)
            p6["waste_recycled"] = r1.number_input(
                "Recycled (MT)", min_value=0.0, step=0.001,
                value=float(p6.get("waste_recycled", 0.0)), key="f_wrc"
            )
            p6["waste_reused"] = r2.number_input(
                "Re-used (MT)", min_value=0.0, step=0.001,
                value=float(p6.get("waste_reused", 0.0)), key="f_wru"
            )
            p6["waste_other_recovery"] = r3.number_input(
                "Other recovery (MT)", min_value=0.0, step=0.001,
                value=float(p6.get("waste_other_recovery", 0.0)), key="f_wor"
            )

            total_recovered = (p6["waste_recycled"] + p6["waste_reused"] +
                               p6["waste_other_recovery"])
            if total_waste_cur > 0:
                recovery_pct = round((total_recovered / total_waste_cur) * 100, 1)
                if recovery_pct >= 50:
                    good(f"{recovery_pct}% waste recovered — excellent circular economy.")
                elif recovery_pct > 0:
                    warn(f"{recovery_pct}% waste recovered. Increase recycling/selling scrap.")

        with st.container(border=True):
            st.markdown("#### Waste Disposal Methods")
            d1, d2, d3 = st.columns(3)
            p6["waste_incinerated"] = d1.number_input(
                "Incineration (MT)", min_value=0.0, step=0.001,
                value=float(p6.get("waste_incinerated", 0.0)), key="f_winc"
            )
            p6["waste_landfilled"] = d2.number_input(
                "Landfilling (MT)", min_value=0.0, step=0.001,
                value=float(p6.get("waste_landfilled", 0.0)), key="f_wlf"
            )
            p6["waste_other_disp"] = d3.number_input(
                "Other disposal (MT)", min_value=0.0, step=0.001,
                value=float(p6.get("waste_other_disp", 0.0)), key="f_wod"
            )

        with st.container(border=True):
            st.markdown("#### Waste Management Practices (Essential Q9)")
            p6["waste_practices"] = st.text_area(
                "Describe your waste management practices",
                value=p6.get("waste_practices", ""),
                height=100,
                placeholder="e.g. We segregate waste at source into 3 bins: "
                            "recyclable, non-recyclable, hazardous. "
                            "Plastic and metal scrap is sold to authorized recyclers monthly. "
                            "Hazardous chemicals are collected by PCB-authorised "
                            "waste management vendor quarterly.",
                key="f_wp"
            )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Compliance →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 5: COMPLIANCE ───────────────────────────────────────────
    elif full_step == 5:
        st.header("⚖️ Environmental Compliance (Essential Q10-Q12)")
        badge_e()

        with st.container(border=True):
            st.markdown("#### Pollution Control Board Certificate")
            pcb_options_full = [
                "Yes — we have valid PCB certificate",
                "No — we don't have it",
                "Not Applicable — our business doesn't require it",
                "Applied and pending"
            ]
            current_pcb_full = p6.get("pcb_compliant", pcb_options_full[0])
            if current_pcb_full not in pcb_options_full:
                current_pcb_full = pcb_options_full[0]
            p6["pcb_compliant"] = st.radio(
                "Does your business have a valid PCB Certificate / Consent to Operate?",
                pcb_options_full,
                index=pcb_options_full.index(current_pcb_full),
                key="f_pcb_full"
            )

        with st.container(border=True):
            st.markdown("#### Environmental Law Compliance (Essential Q12)")
            st.caption(
                "Separate from PCB certificate. This covers compliance with "
                "Water Act, Air Act, Environment Protection Act."
            )

            env_options_full = [
                "Yes — fully compliant",
                "No — some non-compliances exist",
                "Not Applicable"
            ]
            current_env_full = p6.get("env_compliant", env_options_full[0])
            if current_env_full not in env_options_full:
                current_env_full = env_options_full[0]
            p6["env_compliant"] = st.radio(
                "Is your business compliant with applicable environmental "
                "laws (Water Act, Air Act, Environment Protection Act)?",
                env_options_full,
                index=env_options_full.index(current_env_full),
                key="f_env_comp"
            )

            if p6["env_compliant"].startswith("No"):
                st.markdown("**Detail each non-compliance:**")
                p6["noncompliance_details"] = st.text_area(
                    "Law / regulation, details, fines paid, corrective action",
                    value=p6.get("noncompliance_details", ""),
                    height=100,
                    placeholder="e.g. Air Act Consent expired March 2025. "
                                "Renewal applied May 2025. GPCB notice received. "
                                "Fine of ₹10,000 paid. CTO renewal expected by August 2025.",
                    key="f_ncd"
                )

        with st.container(border=True):
            st.markdown("#### Ecologically Sensitive Areas (Essential Q10)")
            p6["near_sensitive"] = st.radio(
                "Do you have operations near ecologically sensitive areas?",
                ["No", "Yes"],
                horizontal=True,
                index=0 if p6.get("near_sensitive", "No") == "No" else 1,
                key="f_eco_sens"
            )
            if p6["near_sensitive"] == "Yes":
                p6["sensitive_details"] = st.text_area(
                    "Location, type of operations, compliance status",
                    value=p6.get("sensitive_details", ""),
                    height=80, key="f_eco_det"
                )

        with st.container(border=True):
            st.markdown("#### EIA (Environmental Impact Assessment) — Essential Q11")
            st.caption(
                "Required for major projects. Most MSMEs have not done EIA. "
                "Answer No if not applicable."
            )
            p6["eia_done"] = st.radio(
                "Have you conducted any EIA this financial year?",
                ["No", "Yes"],
                horizontal=True,
                index=0 if p6.get("eia_done", "No") == "No" else 1,
                key="f_eia"
            )
            if p6["eia_done"] == "Yes":
                ec = st.columns(3)
                p6["eia_project"] = ec[0].text_input(
                    "Project name", value=p6.get("eia_project", ""),
                    key="f_eia_proj"
                )
                p6["eia_notification"] = ec[1].text_input(
                    "EIA Notification No.",
                    value=p6.get("eia_notification", ""), key="f_eia_notif"
                )
                p6["eia_external"] = ec[2].radio(
                    "External agency?", ["Yes", "No"],
                    horizontal=True,
                    index=0 if p6.get("eia_external", "No") == "Yes" else 1,
                    key="f_eia_ext"
                )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Leadership →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 6: LEADERSHIP ───────────────────────────────────────────
    elif full_step == 6:
        st.header("🏆 Leadership Indicators — P6")
        badge_l()

        st.info(
            "These go beyond basic compliance. "
            "Filling even 3-4 of these puts you in the top 10% of MSMEs."
        )

        lt = st.tabs([
            "☀️ L1: Renewable Energy",
            "💧 L2: Water Discharge",
            "🏭 L3: Water Stress",
            "🌍 L4: Scope 3",
            "🌱 L6: Initiatives",
            "🚨 L7: Disaster Plan",
            "🔗 L9: VC Assessment"
        ])

        with lt[0]:
            badge_l()
            st.markdown("### Renewable vs Non-Renewable Energy Breakdown")
            example(
                "If you have solar panels generating 2,000 kWh/year = renewable. "
                "Grid electricity = non-renewable. "
                "Most MSMEs: 100% non-renewable unless they have solar."
            )
            rc = st.columns(2)
            p6["renewable_kwh"] = rc[0].number_input(
                "Electricity from renewable sources (kWh/year)",
                min_value=0.0,
                value=float(p6.get("renewable_kwh", 0.0)),
                key="f_ren_kwh",
                help="Solar panels, wind, biogas etc."
            )
            p6["nonrenewable_kwh"] = rc[1].number_input(
                "Electricity from non-renewable (kWh/year)",
                min_value=0.0,
                value=float(p6.get(
                    "nonrenewable_kwh",
                    p6.get("electricity_kwh_yr", 0.0)
                )),
                key="f_nonren_kwh"
            )
            total_energy = p6["renewable_kwh"] + p6["nonrenewable_kwh"]
            if total_energy > 0:
                ren_pct = round((p6["renewable_kwh"] / total_energy) * 100, 1)
                if ren_pct > 0:
                    good(
                        f"{ren_pct}% renewable energy. "
                        "This is a strong ESG positive and qualifies for "
                        "green loan incentives."
                    )
                else:
                    warn(
                        "0% renewable. Even a small rooftop solar installation "
                        "improves this significantly."
                    )

        with lt[1]:
            badge_l()
            st.markdown("### Water Discharge Details")
            p6["water_discharge_kl"] = st.number_input(
                "Total water discharged (kilolitres/year)",
                min_value=0.0,
                value=float(p6.get("water_discharge_kl", 0.0)),
                key="f_wd_kl"
            )
            p6["water_discharge_treated"] = st.radio(
                "Is the discharged water treated?",
                ["No treatment",
                 "Primary treatment",
                 "Secondary treatment",
                 "Tertiary treatment"],
                index=["No treatment", "Primary treatment",
                       "Secondary treatment",
                       "Tertiary treatment"].index(
                    p6.get("water_discharge_treated", "No treatment")
                ),
                key="f_wd_treat"
            )

        with lt[2]:
            badge_l()
            st.markdown("### Operations in Water Stress Areas")
            st.caption(
                "Gujarat has significant water stress areas. "
                "Check the Water Risk Atlas at wri.org to see if your area is water-stressed."
            )
            p6["water_stress_area"] = st.radio(
                "Are any of your facilities in water-stressed areas?",
                ["No", "Yes"],
                horizontal=True,
                index=0 if p6.get("water_stress_area", "No") == "No" else 1,
                key="f_ws_area"
            )
            if p6["water_stress_area"] == "Yes":
                p6["water_stress_desc"] = st.text_area(
                    "Area name and water usage details",
                    value=p6.get("water_stress_desc", ""),
                    height=60, key="f_ws_desc"
                )

        with lt[3]:
            badge_l()
            st.markdown("### Scope 3 Emissions")
            st.caption(
                "Scope 3 = indirect emissions from your supply chain — "
                "transport, raw materials, customer use of your product. "
                "Very difficult to calculate precisely. Most MSMEs don't have this data."
            )
            dna_scope3 = st.toggle(
                "Data Not Available — we don't track Scope 3",
                value=p6.get("dna_scope3", True),
                key="f_dna_s3"
            )
            p6["dna_scope3"] = dna_scope3
            if not dna_scope3:
                p6["scope3_co2"] = st.number_input(
                    "Scope 3 emissions (tonnes CO₂e)",
                    min_value=0.0,
                    value=float(p6.get("scope3_co2", 0.0)),
                    key="f_s3"
                )

        with lt[4]:
            badge_l()
            st.markdown("### Resource Efficiency Initiatives")
            p6["initiatives"] = st.text_area(
                "Describe any specific initiatives to improve resource "
                "efficiency or reduce environmental impact",
                value=p6.get("initiatives", ""),
                height=100,
                placeholder="e.g. 1. Installed LED lights across factory — "
                            "reduced electricity by 800 units/month. "
                            "2. Rainwater harvesting tank installed — "
                            "reduced tanker dependency by 30%. "
                            "3. Sell all metal scrap to authorized recycler "
                            "— earns ₹3,000/month.",
                key="f_init"
            )

        with lt[5]:
            badge_l()
            st.markdown("### Business Continuity & Disaster Management Plan")
            p6["disaster_plan"] = st.radio(
                "Do you have a business continuity and disaster management plan?",
                ["Yes", "No", "Informal plan only"],
                horizontal=True,
                index=["Yes", "No", "Informal plan only"].index(
                    p6.get("disaster_plan", "No")
                ),
                key="f_disaster"
            )
            if p6["disaster_plan"] != "No":
                p6["disaster_desc"] = st.text_area(
                    "Describe briefly (or provide web link)",
                    value=p6.get("disaster_desc", ""),
                    height=60,
                    placeholder="e.g. Fire safety plan in place. "
                                "Emergency evacuation procedure posted at all exits. "
                                "Annual fire drill conducted. "
                                "First aid team trained.",
                    key="f_disaster_desc"
                )

        with lt[6]:
            badge_l()
            st.markdown("### Value Chain Partner Environmental Assessment")
            p6["vc_env_pct"] = st.slider(
                "% of value chain partners assessed for "
                "environmental impacts (by value of business)",
                0, 100,
                p6.get("vc_env_pct", 0),
                key="f_vc_env"
            )
            if p6["vc_env_pct"] > 0:
                p6["vc_env_actions"] = st.text_area(
                    "Corrective actions from assessments",
                    value=p6.get("vc_env_actions", ""),
                    height=60, key="f_vc_env_act"
                )

        c_back, _, c_next = st.columns([1, 2, 1])
        with c_back:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
        with c_next:
            if st.button("Next: Summary →",
                         type="primary", use_container_width=True):
                next_f(); st.rerun()

    # ── FULL STEP 7: SUMMARY ──────────────────────────────────────────────
    elif full_step == 7:
        st.header("✅ Principle 6 — Full Mode Summary")

        score = calc_p6_score()
        colour = ("green" if score >= 70
                  else "orange" if score >= 40 else "red")
        st.markdown(
            f"<h2 style='color:{colour};text-align:center'>{score}/100</h2>"
            "<p style='text-align:center;color:gray'>Environmental Score</p>",
            unsafe_allow_html=True
        )
        st.progress(score / 100)

        st.markdown("---")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Energy",
                  f"{p6.get('total_energy_gj', 0):.3f} GJ")
        m2.metric("Total Water",
                  f"{p6.get('water_kl_yr', 0):.1f} kL")
        m3.metric("Scope 1+2 CO₂",
                  f"{p6.get('scope12_co2', round(p6.get('scope1_co2', 0) + p6.get('scope2_co2', 0), 4)):.4f} t")
        m4.metric("Total Waste",
                  f"{p6.get('total_waste_mt', 0):.3f} MT")

        st.markdown("---")
        with st.container(border=True):
            st.markdown("#### BRSR-Ready Summary Table")
            summary_data = [
                ["Total electricity consumption (kWh)",
                 f"{p6.get('electricity_kwh_yr', 0):,.0f}", "—"],
                ["Total fuel consumption (litres diesel)",
                 f"{p6.get('diesel_litres_yr', 0):,}", "—"],
                ["Total energy (GJ)",
                 f"{p6.get('total_energy_gj', 0):.4f}", "—"],
                ["Scope 1 emissions (tCO₂e)",
                 f"{p6.get('scope1_co2', 0):.4f}", "—"],
                ["Scope 2 emissions (tCO₂e)",
                 f"{p6.get('scope2_co2', 0):.4f}", "—"],
                ["Total water withdrawal (kL)",
                 f"{p6.get('water_kl_yr', 0):.2f}", "—"],
                ["Total waste generated (MT)",
                 f"{p6.get('total_waste_mt', 0):.4f}", "—"],
                ["PCB Certificate Status",
                 p6.get('pcb_compliant', '—'), "—"],
                ["Environmental Law Compliance",
                 p6.get('env_compliant', '—'), "—"],
            ]
            df = pd.DataFrame(
                summary_data,
                columns=["Parameter", "Current FY", "Previous FY"]
            )
            st.dataframe(df, use_container_width=True)

        elec = p6.get("electricity_kwh_yr", 0)
        if elec > 0:
            st.markdown("---")
            st.markdown("#### 💰 Your Green Savings Opportunity")
            gc1, gc2 = st.columns(2)
            with gc1:
                s10 = money_saved_from_reduction(elec, 10)
                money("Save 10% electricity", s10)
            with gc2:
                s20 = money_saved_from_reduction(elec, 20)
                money("Save 20% electricity", s20)

        st.markdown("---")
        recs = 0
        if not p6.get("pcb_compliant", "").startswith("Yes"):
            bad("PCB Certificate needed — highest priority.")
            recs += 1
        if not p6.get("env_compliant", "").startswith("Yes"):
            bad("Confirm environmental law compliance.")
            recs += 1
        if not p6.get("waste_tracked") and not p6.get("waste_full"):
            warn("Document your waste generation.")
            recs += 1
        if not p6.get("green_efforts", "").strip() and not p6.get("green_preset"):
            warn("Document at least 2 green initiatives.")
            recs += 1
        if recs == 0:
            good("No major P6 gaps! Strong environmental profile.")

        st.markdown("---")
        cf1, cf2, cf3 = st.columns([1, 2, 1])
        with cf2:
            if st.button("💾 Save P6 & Move to P7 →",
                         type="primary", use_container_width=True):
                st.session_state.c_p6 = p6
                st.balloons()
                st.success(
                    "✅ P6 saved! Next: Principle 7 — Policy Advocacy."
                )

        c_back2, _, _ = st.columns([1, 2, 1])
        with c_back2:
            if st.button("← Back", use_container_width=True):
                prev_f(); st.rerun()
                
# ─── BOTTOM NAVIGATION ──────────────────────────────────────────────────
from business_profile import render_section_navigation
render_section_navigation("Principle 6")
from business_profile import (
    init_business_profile, show_tier_badge, show_sidebar_logo,
    get_business_type, is_sole_prop, is_partnership,
    has_board, is_listed
)
init_business_profile()
show_sidebar_logo()
show_tier_badge()