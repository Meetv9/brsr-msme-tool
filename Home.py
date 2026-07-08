"""
Home.py — Main Landing Page for BRSR MSME Tool

Run this file with: streamlit run Home.py

Streamlit auto-detects the /pages folder and builds the sidebar menu.
"""

import streamlit as st
from PIL import Image
from pathlib import Path
from scoring import strict_overall, BRSR_SECTION_LABELS
_BASE_DIR = Path(__file__).parent
_ecosetu_icon = Image.open(_BASE_DIR / "assets" / "ecosetu_favicon.png")
from business_profile import (
    show_business_type_selector,
    show_tier_badge,
    get_business_type,
    is_sole_prop,
    is_listed,
)
from sidebar_footer import render_sidebar_footer
# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ecosetu — BRSR for Indian MSMEs",
    page_icon="assets/ecosetu_favicon.png",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "mailto:meet.vaghani9909@gmail.com",
        "Report a bug": "mailto:meet.vaghani9909@gmail.com?subject=Ecosetu%20Bug%20Report",
        "About": "Ecosetu — BRSR compliance for Indian MSMEs. Built by Meet Vaghani. Visit ecosetu.co.in"
    }
)
# ─────────────────────────────────────────────────────────────────────
# IN-APP BROWSER NOTICE — for LinkedIn / Instagram / WhatsApp visitors
# ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='background:#fff8e1; border:1px solid #ffcc80;
                border-radius:8px; padding:10px 14px;
                font-size:13px; color:#5d4037; margin: 32px 0 20px 0;
                line-height:1.5;'>
        💡 <b>Opened this from LinkedIn, Instagram, or WhatsApp?</b>
        For sign-up + PDF downloads to work properly, tap the 
        <b> ••• menu</b> in the top corner and choose 
        <b>"Open in browser"</b> (or Safari/Chrome).
    </div>
    """,
    unsafe_allow_html=True,
)
# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR LOGO (shows on every page automatically)
# ─────────────────────────────────────────────────────────────────────────────
try:
    st.logo(
        str(_BASE_DIR / "assets" / "ecosetu_logo.png"),
        icon_image=str(_BASE_DIR / "assets" / "ecosetu_icon_128.png"),
        size="large"
    )
except (AttributeError, TypeError):
    # Fallback for older Streamlit versions
    with st.sidebar:
        st.image(str(_BASE_DIR / "assets" / "ecosetu_logo.png"),
                 use_container_width=True)
        st.markdown("---")


# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

    :root {
        --eco-deep: #0F4C2C;
        --eco-green: #16A34A;
        --eco-mint: #DCFCE7;
        --eco-ink: #0B1F16;
        --eco-slate: #4B5D55;
        --eco-indigo: #6366F1;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3, h4 { font-family: 'Sora', sans-serif !important; letter-spacing: -0.02em; }

    .block-container { padding-top: 2.5rem; max-width: 1020px; margin-left: auto; margin-right: auto; }

    /* ── Animated mesh hero ─────────────────────────────── */
    .eco-hero {
        position: relative; overflow: hidden;
        border-radius: 24px; padding: 46px 38px 40px;
        margin: 6px 0 14px;
        background:
            radial-gradient(120% 120% at 0% 0%, rgba(22,163,74,0.30) 0%, rgba(22,163,74,0) 45%),
            radial-gradient(120% 120% at 100% 0%, rgba(99,102,241,0.28) 0%, rgba(99,102,241,0) 42%),
            radial-gradient(130% 130% at 80% 100%, rgba(16,124,67,0.30) 0%, rgba(16,124,67,0) 50%),
            linear-gradient(135deg, #07291A 0%, #0F4C2C 55%, #0B3A22 100%);
        box-shadow: 0 24px 60px -28px rgba(15,76,44,0.65);
    }
    .eco-hero::after {
        content: ""; position: absolute; inset: -40%;
        background: conic-gradient(from 0deg at 50% 50%, transparent 0deg, rgba(220,252,231,0.07) 120deg, transparent 240deg);
        animation: ecospin 22s linear infinite; pointer-events: none;
    }
    @keyframes ecospin { to { transform: rotate(360deg); } }
    .eco-hero > * { position: relative; z-index: 1; }

    .eco-eyebrow {
        display: inline-flex; align-items: center; gap: 8px;
        font-size: 11.5px; font-weight: 600; letter-spacing: 2px;
        text-transform: uppercase; color: #BBF7D0;
        background: rgba(220,252,231,0.10); border: 1px solid rgba(220,252,231,0.22);
        padding: 6px 14px; border-radius: 999px; margin-bottom: 18px;
    }
    .eco-dot { width: 7px; height: 7px; border-radius: 50%; background: #4ADE80;
               box-shadow: 0 0 0 0 rgba(74,222,128,0.7); animation: ecopulse 2s infinite; }
    @keyframes ecopulse {
        0% { box-shadow: 0 0 0 0 rgba(74,222,128,0.6); }
        70% { box-shadow: 0 0 0 8px rgba(74,222,128,0); }
        100% { box-shadow: 0 0 0 0 rgba(74,222,128,0); }
    }
    .eco-h1 {
        font-family: 'Sora', sans-serif; font-weight: 800;
        font-size: clamp(30px, 5.2vw, 50px); line-height: 1.05;
        color: #FFFFFF; margin: 0 0 16px;
    }
    .eco-h1 .grad {
        background: linear-gradient(90deg, #4ADE80, #A7F3D0 60%, #C7D2FE);
        -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    }
    .eco-sub {
        font-size: clamp(14px, 2.2vw, 17px); line-height: 1.6;
        color: #CDEAD9; max-width: 620px; margin: 0 0 24px;
    }
    .eco-cta-row { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
    .eco-btn-primary {
        display: inline-flex; align-items: center; gap: 9px;
        padding: 14px 26px; border-radius: 12px; text-decoration: none;
        font-weight: 700; font-size: 15.5px; color: #07291A;
        background: linear-gradient(180deg, #6EE7A0, #22C55E);
        box-shadow: 0 12px 26px -10px rgba(34,197,94,0.8);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .eco-btn-primary:hover { transform: translateY(-2px); box-shadow: 0 18px 34px -10px rgba(34,197,94,0.9); }
    .eco-btn-ghost {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 13px 22px; border-radius: 12px; text-decoration: none;
        font-weight: 600; font-size: 15px; color: #EAFBF1;
        border: 1px solid rgba(220,252,231,0.32); background: rgba(220,252,231,0.06);
        transition: background .18s ease, border-color .18s ease;
    }
    .eco-btn-ghost:hover { background: rgba(220,252,231,0.14); border-color: rgba(220,252,231,0.55); }
    .eco-hero-note { font-size: 12.5px; color: #9FD3B4; margin-top: 14px; }

    /* ── Stat band ──────────────────────────────────────── */
    .eco-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 18px 0 8px; }
    .eco-stat {
        background: #FFFFFF; border: 1px solid #E6F0EA; border-radius: 16px;
        padding: 16px 14px; text-align: center;
        box-shadow: 0 8px 22px -18px rgba(15,76,44,0.5);
    }
    .eco-stat .num { font-family: 'Sora', sans-serif; font-weight: 800; font-size: 22px; color: var(--eco-deep); }
    .eco-stat .lbl { font-size: 11.5px; color: var(--eco-slate); margin-top: 3px; }
    @media (max-width: 640px) {
        .eco-stats { grid-template-columns: repeat(2, 1fr); }
        .eco-hero { padding: 34px 22px 30px; }
    }

    /* ── Feature cards ──────────────────────────────────── */
    .eco-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 8px 0; }
    @media (max-width: 760px) { .eco-grid { grid-template-columns: 1fr; } }
    .eco-card {
        background: #FFFFFF; border: 1px solid #E6F0EA; border-radius: 18px;
        padding: 20px 18px; transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }
    .eco-card:hover { transform: translateY(-3px); border-color: #BBF7D0;
                      box-shadow: 0 18px 40px -22px rgba(15,76,44,0.55); }
    .eco-card .ic {
        width: 42px; height: 42px; border-radius: 12px; display: flex;
        align-items: center; justify-content: center; font-size: 20px; margin-bottom: 12px;
        background: var(--eco-mint);
    }
    .eco-card h4 { font-size: 16px; color: var(--eco-ink); margin: 0 0 6px; }
    .eco-card p { font-size: 13px; color: var(--eco-slate); line-height: 1.55; margin: 0; }

    .eco-section-title { font-family:'Sora',sans-serif; font-weight:700; font-size: 22px;
                         color: var(--eco-ink); margin: 6px 0 4px; }
    .eco-section-kicker { font-size:11.5px; font-weight:600; letter-spacing:2px; text-transform:uppercase;
                          color: var(--eco-green); margin-bottom: 2px; }

    /* ── Functional classes (kept for progress + score) ── */
    .hero-box {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border: 2px solid #66bb6a; border-radius: 16px;
        padding: 24px; margin: 16px 0; text-align: center;
    }
    .progress-card { border: 1px solid #E6F0EA; border-radius: 16px; padding: 18px; margin: 8px 0;
                     box-shadow: 0 8px 22px -20px rgba(15,76,44,0.5); }
    .score-big { font-family:'Sora',sans-serif; font-size: 56px; font-weight: 800; color: #0F4C2C; margin: 8px 0; }
    .section-link {
        background: #F6FBF8; border-left: 4px solid var(--eco-green);
        padding: 12px 16px; margin: 8px 0; border-radius: 0 10px 10px 0;
        font-size: 14px; color: var(--eco-ink);
    }
    .done-tick { color: #16A34A; font-weight: 700; font-size: 16px; }
    .pending-tick { color: #C7D2CC; font-size: 16px; }

    /* ── Save & Resume highlight banner ─────────────────── */
    .eco-save {
        position: relative; overflow: hidden;
        display: flex; align-items: center; gap: 20px;
        border-radius: 20px; padding: 22px 26px; margin: 20px 0 6px;
        text-decoration: none;
        background:
            radial-gradient(120% 150% at 0% 0%, rgba(99,102,241,0.22) 0%, rgba(99,102,241,0) 55%),
            radial-gradient(130% 150% at 100% 100%, rgba(74,222,128,0.18) 0%, rgba(74,222,128,0) 55%),
            linear-gradient(135deg, #0E3D26 0%, #145236 60%, #10402A 100%);
        border: 1px solid rgba(167,243,208,0.25);
        box-shadow: 0 18px 44px -26px rgba(15,76,44,0.7);
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }
    .eco-save:hover { transform: translateY(-3px); border-color: rgba(167,243,208,0.55);
                      box-shadow: 0 24px 54px -24px rgba(15,76,44,0.85); }
    .eco-save::after {
        content:""; position:absolute; inset:-50%;
        background: conic-gradient(from 0deg at 50% 50%, transparent 0deg, rgba(199,210,254,0.09) 130deg, transparent 250deg);
        animation: ecospin 26s linear infinite; pointer-events:none;
    }
    .eco-save > * { position: relative; z-index: 1; }
    .eco-save-ic {
        flex: 0 0 auto; width: 58px; height: 58px; border-radius: 16px;
        display:flex; align-items:center; justify-content:center; font-size: 28px;
        background: linear-gradient(180deg, rgba(199,210,254,0.22), rgba(110,231,160,0.18));
        border: 1px solid rgba(220,252,231,0.3);
    }
    .eco-save-body { flex: 1 1 auto; min-width: 0; }
    .eco-save-pill {
        display:inline-block; font-size:10.5px; font-weight:700; letter-spacing:1.5px;
        text-transform:uppercase; color:#07291A;
        background: linear-gradient(90deg,#A7F3D0,#C7D2FE);
        padding:3px 10px; border-radius:999px; margin-bottom:9px;
    }
    .eco-save-body h4 { font-family:'Sora',sans-serif; font-weight:700; font-size:18px;
                        color:#FFFFFF; margin:0 0 5px; line-height:1.25; }
    .eco-save-body p { font-size:13.5px; color:#CDEAD9; line-height:1.55; margin:0; }
    .eco-save-cta {
        flex: 0 0 auto; display:inline-flex; align-items:center; gap:7px;
        font-weight:700; font-size:14px; color:#07291A;
        background: linear-gradient(180deg, #6EE7A0, #22C55E);
        padding:11px 18px; border-radius:11px; white-space:nowrap;
        box-shadow: 0 10px 22px -10px rgba(34,197,94,0.8);
    }
    @media (max-width: 640px) {
        .eco-save { flex-direction: column; align-items: flex-start; gap: 14px; padding: 20px; }
        .eco-save-cta { align-self: stretch; justify-content:center; }
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO — Ecosetu Branding
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="eco-hero">
        <div class="eco-eyebrow">
            <svg width="14" height="14" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
                <g transform="translate(15,12)">
                    <rect x="0" y="0" width="6" height="56" rx="3" fill="#A7F3D0"/>
                    <rect x="0" y="0" width="38" height="6" rx="3" fill="#A7F3D0"/>
                    <rect x="0" y="25" width="28" height="6" rx="3" fill="#4ADE80"/>
                    <rect x="0" y="50" width="38" height="6" rx="3" fill="#A7F3D0"/>
                </g>
            </svg>
            Ecosetu · BRSR for Indian MSMEs
        </div>
        <div class="eco-h1">
            Turn your factory's numbers into a<br>
            <span class="grad">bank-ready sustainability report.</span>
        </div>
        <div class="eco-sub">
            BRSR is the language banks, big buyers, and EU importers now speak.
            Ecosetu translates your everyday business data into an audit-ready
            BRSR report — in about 60 minutes, with zero jargon and zero cost.
        </div>
        <div class="eco-cta-row">
            <a class="eco-btn-primary" href="https://forms.gle/ZAvGwN25sCPT3gU3A"
               target="_blank" rel="noopener">🌱 Become a Founding Member — Free for Life</a>
            <a class="eco-btn-ghost" href="#what-is-brsr">How it works ↓</a>
        </div>
        <div class="eco-hero-note">First 100 companies only · No payment · No trial expiry · No catch.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Stat band
st.markdown(
    """
    <div class="eco-stats">
        <div class="eco-stat"><div class="num">9</div><div class="lbl">NGRBC principles</div></div>
        <div class="eco-stat"><div class="num">~60 min</div><div class="lbl">to a full report</div></div>
        <div class="eco-stat"><div class="num">100%</div><div class="lbl">in your browser</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Feature cards — why Ecosetu
st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
st.markdown('<div class="eco-section-kicker">Why Ecosetu</div>', unsafe_allow_html=True)
st.markdown('<div class="eco-section-title">Built for an MSME, not a Big-4 corporate</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="eco-grid">
        <div class="eco-card">
            <div class="ic">⚡</div>
            <h4>Quick Mode</h4>
            <p>Answer 10–15 plain-language questions per principle. We do the
               scoring, GHG maths, and water intensity for you.</p>
        </div>
        <div class="eco-card">
            <div class="ic">🇮🇳</div>
            <h4>Indian context</h4>
            <p>Indian regulatory terms, CEA grid factors, IPCC
               fuel factors — every number sourced and defensible.</p>
        </div>
        <div class="eco-card">
            <div class="ic">📄</div>
            <h4>Bank-ready PDF</h4>
            <p>An audit-ready, BRSR-format report you can hand to a bank,
               buyer, or auditor — with a methodology appendix.</p>
        </div>
        <div class="eco-card">
            <div class="ic">💼</div>
            <h4>Tier-aware</h4>
            <p>Sole proprietor? We hide board, KMP and shareholder questions
               that don't apply to you.</p>
        </div>
        <div class="eco-card">
            <div class="ic">🔒</div>
            <h4>Privacy-first</h4>
            <p>Your data stays in your browser session. No account, no
               server storage, no data collection.</p>
        </div>
        <div class="eco-card">
            <div class="ic">🌉</div>
            <h4>Green compliance, bridged</h4>
            <p>From confused to compliant — Ecosetu bridges the gap between
               your shop floor and what regulators expect.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Save & Resume highlight banner (clickable → Save & Resume page) ──────────
st.markdown(
    """
    <a class="eco-save" href="Save_and_Resume" target="_self">
        <div class="eco-save-ic">💾</div>
        <div class="eco-save-body">
            <span class="eco-save-pill">New · Never lose your work</span>
            <h4>Save &amp; Resume — pick up exactly where you left off</h4>
            <p>No account, no sign-up. Download a small progress file any time and
               re-upload it later — on any device — to restore every answer and land
               back on the exact step you were on. 100% in your browser.</p>
        </div>
        <span class="eco-save-cta">See how →</span>
    </a>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
# ─────────────────────────────────────────────────────────────────────────────
# WHY BRSR? — Educational content for new visitors
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div id="what-is-brsr"></div>', unsafe_allow_html=True)
st.markdown('<div class="eco-section-kicker">The basics</div>', unsafe_allow_html=True)
st.markdown('<div class="eco-section-title">📖 What is BRSR & why it matters</div>', unsafe_allow_html=True)
st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

with st.expander("**What is BRSR?**  (1 min read)", expanded=False):
    st.markdown("""
**BRSR** stands for **Business Responsibility & Sustainability Reporting**.

It's a SEBI-mandated disclosure framework that asks Indian companies:

> *"How do you treat your employees, customers, environment,
> and community — beyond just making profits?"*

The framework has **9 NGRBC principles** covering ethics, sustainability,
employee welfare, stakeholder engagement, human rights, environment,
policy advocacy, inclusive growth, and customer responsibility.

**Currently mandatory for:** Top 1,000 listed companies (by market cap)
**Voluntary for:** All other companies — but increasingly demanded by
buyers, banks, and government schemes.
""")

with st.expander("**Why should an MSME care about BRSR?**", expanded=False):
    st.markdown("""
You're not legally required to file BRSR (unless you're a top-1000 listed
company). But here's why MSMEs are doing it voluntarily:

| Reason | What it unlocks |
|--------|-----------------|
| 🏦 **Bank loans** | Lower interest rates from SBI, HDFC, ICICI on ESG-disclosed loans |
| 🌍 **Export contracts** | EU buyers ask Indian vendors for ESG data under the revised CSRD (post-Omnibus); the largest EU groups report from 2028 on FY 2027 data |
| 🏭 **Big buyer contracts** | Tata, Reliance, ITC, Marico now ask suppliers for ESG data |
| 🪙 **Government schemes** | PLI, RAMP, Aatmanirbhar Bharat schemes prioritize compliant MSMEs |
| 💰 **Green funding** | SIDBI, NABARD offer concessional rates to ESG-disclosed MSMEs |
| 📈 **Investor readiness** | If you ever raise funds, this is the first thing they'll ask |

**One clean BRSR report = leverage in 6 different conversations.**
""")

with st.expander("**How does this tool help me?**", expanded=False):
    st.markdown("""
This tool is built **specifically for Indian MSMEs**, not big corporates.
Here's what makes it different:

- ⚡ **Quick Mode** — Answer just 10–15 questions per principle in plain language
- 🌐 **Indian context** — Examples in Indian regulatory terms
- 💼 **Tier-aware** — If you're a sole proprietor, we hide board/KMP questions
- 🧮 **Auto-calculations** — We compute scores, GHG emissions, water intensity for you
- 📄 **BRSR-format PDF** — Audit-ready report you can send to banks/buyers
- 🆓 **Free to use** — No signup, no payment, no data collection
- 🔒 **Privacy-first** — Your data stays in your browser session, never sent to a server

Built for MSMEs by an MSME-focused developer.
""")

with st.expander("**How long does this take?**", expanded=False):
    st.markdown("""
**Quick Mode:** ~45–60 minutes for the entire BRSR report (all 9 principles).

**Full Mode:** ~3–4 hours if you want to fill every SEBI essential indicator.

You can save and resume anytime — your progress is auto-saved in your
browser session.

**Tip:** Have these ready before you start:
- Last year's turnover figure
- Number of employees and workers
- Electricity bills (annual kWh consumption)
- PCB Consent to Operate certificate
- A rough idea of your sourcing patterns
""")

with st.expander("**What's changing in 2025–2028?**", expanded=False):
    st.markdown("""
The disclosure landscape is tightening on two fronts — worth knowing where
you fit.

**India — BRSR Core (SEBI):**
- **Top 250** listed companies: BRSR Core assurance + value-chain disclosures already apply (FY 2025-26).
- **Top 1,000** listed companies: BRSR Core expands to all of them by FY 2026-27, with full **reasonable assurance** targeted by FY 2027-28.
- Result: large buyers increasingly push these expectations down to their MSME suppliers.

**Europe — the rules were made lighter in Dec 2025:**
- Earlier, many EU companies had to publish detailed ESG reports. In December 2025 the EU **relaxed** these rules.
- Now **only very large companies** (more than 1,000 staff and over €450M turnover) must report.
- The deadline was also pushed back — the next big batch reports in **2028**, using their 2027 data.
- Smaller companies are **no longer forced** to report, and they only need to ask their **direct suppliers** for data.
- **What this means for you:** EU buyers still ask their Indian suppliers for ESG data — just under the lighter, simpler rules now. A clean BRSR keeps you ready either way.
""")

st.markdown("")
# ─────────────────────────────────────────────────────────────────────
# METHODOLOGY DOWNLOAD — for CAs, ESG consultants, advocates
# ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📘 For Reviewers, CAs & ESG Consultants")
st.markdown(
    "Want to understand how Ecosetu calculates every number — from electricity bills to "
    "Scope 1 emissions to water withdrawal? Read our **Principle 6 Calculation Methodology**. "
    "Every formula, every constant, every source — fully transparent."
)

try:
    with open("assets/Ecosetu_P6_Methodology.pdf", "rb") as pdf_file:
        pdf_bytes = pdf_file.read()

    dl_col1, dl_col2, dl_col3 = st.columns([1, 2, 1])
    with dl_col2:
        st.download_button(
            label="📥  Download Methodology Document (PDF)",
            data=pdf_bytes,
            file_name="Ecosetu_P6_Methodology.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
        st.markdown(
            """
            <p style='text-align:center; color:#666; font-size:13px; margin-top:6px;'>
                9 pages · References IPCC, CEA, CPHEEO, SEBI BRSR guidelines
            </p>
            <p style='text-align:center; font-size:13px; color:#666; margin-top:4px;'>
                Download not working on mobile? 
                <a href='https://github.com/Meetv9/brsr-msme-tool/raw/main/assets/Ecosetu_P6_Methodology.pdf'
                   target='_blank' rel='noopener' style='color:#0F4C2C; font-weight:600;'>
                   Open the PDF directly →
                </a>
            </p>
            """,
            unsafe_allow_html=True,
        )
except FileNotFoundError:
    st.warning("Methodology document is being updated — please check back soon.")


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: BUSINESS TYPE SELECTOR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
show_business_type_selector()

btype = get_business_type()
show_tier_badge()

if is_sole_prop():
    st.info(
        "✅ We'll hide board-related, shareholder, and formal policy "
        "questions since they don't apply to sole proprietorships."
    )
elif is_listed():
    st.warning(
        "⚠️ Listed companies must complete the full BRSR. "
        "All Essential + Leadership indicators will be shown."
    )
    # ─────────────────────────────────────────────────────────────────────────────
# PRIMARY CTA — Start Section A
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("")
col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    if st.button(
        "🚀  Start with Section A — General Disclosures",
        type="primary",
        use_container_width=True,
        key="cta_start_section_a"
    ):
        st.switch_page("pages/1_Section_A.py")
    st.caption(
        "Takes about 10–15 minutes. Your progress is auto-saved.",
        unsafe_allow_html=False
    )

# ─────────────────────────────────────────────────────────────────────────────
# PROGRESS TRACKER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📊 Your BRSR Progress")

# Check what has been filled
sections = [
    ("Section A — General Disclosures", "data", "company_name",
     "1_📋_Section_A"),
    ("Section B — Management & Process", "data_b", None,
     "2_🧭_Section_B"),
    ("Principle 1 — Ethics & Integrity", "p1", None,
     "3_⚖️_Principle_1"),
    ("Principle 2 — Sustainable Products", "p2", None,
     "4_🔄_Principle_2"),
    ("Principle 3 — Employee Wellbeing", "p3", None,
     "5_👥_Principle_3"),
    ("Principles 4 & 5 — Stakeholders & Human Rights", "p4_5", None,
     "6_🤝_Principle_4_5"),
    ("Principle 6 — Environment", "p6", None,
     "7_🌿_Principle_6"),
    ("Principles 7, 8, 9 — Policy, Community & Customers", "p789", None,
     "8_🤝_Principle_7_8_9"),
]

completed = 0
total_sections = len(sections)

for name, key, subkey, page_name in sections:
    data = st.session_state.get(key, {})
    if subkey:
        is_done = bool(data.get(subkey))
    else:
        is_done = bool(data) and len(data) > 1

    mark = '<span class="done-tick">✅</span>' if is_done else '<span class="pending-tick">⭕</span>'
    if is_done:
        completed += 1

    st.markdown(
        f'<div class="section-link">{mark} &nbsp; {name}</div>',
        unsafe_allow_html=True
    )

st.markdown("")
progress_pct = completed / total_sections
st.progress(progress_pct)
st.caption(f"Completed: {completed} of {total_sections} sections")

# ─────────────────────────────────────────────────────────────────────────────
# OVERALL SCORE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🏆 Overall BRSR Readiness Score")


def collect_section_scores():
    """All 7 BRSR units -> 0-100 score (0 when a section is unfilled).

    Single source for the strict overall readiness number; the PDF builds the
    identical dict and both feed scoring.strict_overall, so they never drift.
    """
    data = st.session_state.get("data", {})
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

    return {
        "section_a": min(a_score, 100),
        "p1": st.session_state.get("c_p1", {}).get("score") or 0,
        "p2": st.session_state.get("c_p2", {}).get("score") or 0,
        "p3": st.session_state.get("p3", {}).get("score") or 0,
        "p45": st.session_state.get("p45", {}).get("score") or 0,
        "p6": st.session_state.get("p6", {}).get("score") or 0,
        "p789": st.session_state.get("p789", {}).get("score") or 0,
    }


section_scores = collect_section_scores()
overall = strict_overall(section_scores)

if any(section_scores.values()):
    colour = "#2e7d32" if overall >= 70 else "#ef6c00" if overall >= 40 else "#c62828"
    st.markdown(
        f'<div class="progress-card" style="text-align:center;">'
        f'<div class="score-big" style="color:{colour};">{overall}/100</div>'
        f'<div style="color:#666;font-size:14px;">'
        f'Overall readiness across all 7 BRSR sections '
        f'&mdash; unfilled sections count as 0</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Individual scores — all 7 units, so the breakdown reconciles with the
    # strict overall above (a 0 row shows exactly what's dragging it down).
    st.markdown("**Section-wise scores:**")
    cols = st.columns(4)
    for i, (key, label) in enumerate(BRSR_SECTION_LABELS):
        with cols[i % 4]:
            st.metric(label, f"{section_scores[key]}/100")
else:
    st.info(
        "📝 Start filling Section A using the sidebar to see your score."
    )

# ─────────────────────────────────────────────────────────────────────────────
# WHAT TO DO NEXT
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🧭 What to do next")

if completed == 0:
    st.info(
        "👉 Start with **Section A** in the sidebar. It captures your "
        "basic company information and auto-fills later sections."
    )
elif completed < total_sections:
    next_section = next(
        (name for name, key, subkey, _ in sections
         if not (st.session_state.get(key, {}) and
                 (st.session_state.get(key, {}).get(subkey) if subkey
                  else len(st.session_state.get(key, {})) > 1))),
        None
    )
    if next_section:
        st.info(f"👉 Continue with **{next_section}** from the sidebar.")
else:
    st.success(
        "🎉 **All sections complete!** Head to **'9 Generate Report'** "
        "in the sidebar to download your BRSR-ready PDF."
    )

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER — Ecosetu branding + Your details
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
st.markdown("---")

# Top row: Brand statement
st.markdown("""
<div style="text-align:center; padding:16px 0 8px 0;">
    <div style="font-size:14px; font-weight:600; color:#0F4C2C;
                letter-spacing:0.3px; margin-bottom:4px;">
        ECOSETU
    </div>
    <div style="font-size:12px; color:#64748B; font-style:italic;">
        Green compliance, bridged.
    </div>
</div>
""", unsafe_allow_html=True)

# Three-column info grid
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("""
<div style="padding:12px;">
    <div style="font-size:10px; font-weight:600; color:#94A3B8;
                letter-spacing:1.5px; margin-bottom:8px;">
        BUILT BY
    </div>
    <div style="font-size:13px; font-weight:600; color:#0F172A;
                margin-bottom:4px;">
        Meet Ketankumar Vaghani
    </div>
    <div style="font-size:11px; color:#64748B; line-height:1.5;">
        Certified ESG Professional<br/>
        Bhavnagar, Gujarat
    </div>
</div>
""", unsafe_allow_html=True)

with col_b:
    st.markdown("""
<div style="padding:12px;">
    <div style="font-size:10px; font-weight:600; color:#94A3B8;
                letter-spacing:1.5px; margin-bottom:8px;">
        AN INITIATIVE BY
    </div>
    <div style="font-size:13px; font-weight:600; color:#0F172A;
                margin-bottom:4px;">
        Keprin Overseas Corporation
    </div>
    <div style="font-size:11px; color:#64748B; line-height:1.5;">
        Bhavnagar, India
    </div>
</div>
""", unsafe_allow_html=True)

with col_c:
    st.markdown("""
<div style="padding:12px;">
    <div style="font-size:10px; font-weight:600; color:#94A3B8;
                letter-spacing:1.5px; margin-bottom:8px;">
        CONNECT
    </div>
    <a href="https://www.linkedin.com/in/meetvaghani/" target="_blank"
       style="font-size:13px; font-weight:500; color:#0F4C2C;
              text-decoration:none; display:block; margin-bottom:4px;">
        LinkedIn →
    </a>
    <a href="mailto:meet.vaghani9909@gmail.com"
       style="font-size:11px; color:#64748B; text-decoration:none;">
        meet.vaghani9909@gmail.com
    </a>
</div>
""", unsafe_allow_html=True)

# Bottom disclaimer
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:12px 0 24px 0;">
    <div style="font-size:11px; color:#94A3B8; line-height:1.6;
                max-width:560px; margin:0 auto;">
        Built on the SEBI BRSR framework. Ecosetu is a self-service tool for
        MSME ESG disclosure preparation and is not a substitute for qualified
        legal, financial, or ESG advisory services. For final BRSR submission
        to SEBI, listed entities should consult an authorised auditor.
    </div>
    <div style="font-size:10px; color:#CBD5E1; margin-top:12px;">
        © 2026 Ecosetu · An initiative by Keprin Overseas Corporation
    </div>
</div>
""", unsafe_allow_html=True)

render_sidebar_footer()