"""
Shared sidebar footer for Ecosetu.
Import and call render_sidebar_footer() at the top of every page.
"""
import streamlit as st

# Founder WhatsApp contact (Indian B2B audience defaults to WhatsApp)
WHATSAPP_NUMBER = "919409417490"
WHATSAPP_MESSAGE = "Hi%20Meet%2C%20I%27m%20using%20Ecosetu%20for%20BRSR%20and%20have%20a%20question."


def render_save_resume_link():
    """Prominent 'Save / Resume progress' link in the sidebar.

    Called from render_whatsapp_fab() so it appears on EVERY page (every page runs
    render_whatsapp_fab, directly or via render_sidebar_footer). Streamlit's default
    multipage nav also lists the page; this gives it a clear, always-visible entry.
    """
    try:
        with st.sidebar:
            st.page_link(
                "pages/10_Save_and_Resume.py",
                label="Save / Resume progress",
                icon="💾",
            )
    except Exception:
        # st.page_link unavailable or page not found — default nav still covers it.
        pass


def render_whatsapp_fab():
    """Floating WhatsApp contact button, fixed to the bottom-right of the viewport.

    Call exactly once per page. render_sidebar_footer() already calls it, so pages
    that render the sidebar footer should NOT call this directly as well.
    """
    render_save_resume_link()
    st.markdown(
        f"""
        <a href="https://wa.me/{WHATSAPP_NUMBER}?text={WHATSAPP_MESSAGE}"
           target="_blank" rel="noopener"
           aria-label="Chat with us on WhatsApp"
           style="position:fixed; bottom:22px; right:22px; z-index:99999;
                  width:56px; height:56px; border-radius:50%;
                  background:#25D366; box-shadow:0 4px 14px rgba(0,0,0,0.25);
                  display:flex; align-items:center; justify-content:center;
                  text-decoration:none;">
            <svg viewBox="0 0 32 32" width="30" height="30" fill="#ffffff"
                 xmlns="http://www.w3.org/2000/svg">
                <path d="M16.04 3C9.4 3 4 8.4 4 15.04c0 2.12.55 4.18 1.6 6L4 29l8.13-1.55a12 12 0 0 0 3.9.65h.01C22.68 28.1 28 22.7 28 16.06 28 9.42 22.68 4 16.04 4zm0 22.06h-.01a10 10 0 0 1-5.1-1.4l-.36-.22-4.82.92.96-4.7-.24-.38a10 10 0 1 1 9.57 5.78zm5.49-7.5c-.3-.15-1.77-.87-2.04-.97-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.07-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51l-.57-.01c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.87 1.22 3.07.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.69.63.71.22 1.36.19 1.87.12.57-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.13-.27-.2-.57-.35z"/>
            </svg>
        </a>
        """,
        unsafe_allow_html=True,
    )


# Ordered journey: the 9 pages a user moves through, in app order.
JOURNEY_STEPS = [
    ("A", "Section A — Company Profile"),
    ("B", "Section B — Management & Process"),
    ("1", "Principle 1 — Ethics & Transparency"),
    ("2", "Principle 2 — Sustainable Products"),
    ("3", "Principle 3 — Employee Wellbeing"),
    ("4·5", "Principles 4 & 5 — Stakeholders & Human Rights"),
    ("6", "Principle 6 — Environment"),
    ("7·8·9", "Principles 7, 8 & 9 — Policy, Growth & Consumers"),
    ("✓", "Generate Report"),
]


def render_journey_progress(step):
    """Compact 'Step N of 9' stepper for the top of each page.

    `step` is the 1-based position in JOURNEY_STEPS.
    """
    total = len(JOURNEY_STEPS)
    idx = max(1, min(step, total))
    label = JOURNEY_STEPS[idx - 1][1]

    pills = []
    for i, (mark, _) in enumerate(JOURNEY_STEPS, 1):
        if i < idx:
            bg, color, border = "#DCFCE7", "#0F4C2C", "#16A34A"
        elif i == idx:
            bg, color, border = "#16A34A", "#ffffff", "#0F4C2C"
        else:
            bg, color, border = "#f3f4f6", "#9ca3af", "#e5e7eb"
        pills.append(
            f"<span style='display:inline-flex; align-items:center; "
            f"justify-content:center; min-width:24px; height:24px; padding:0 7px; "
            f"border-radius:12px; background:{bg}; color:{color}; "
            f"border:1px solid {border}; font-size:11px; font-weight:700; "
            f"line-height:1;'>{mark}</span>"
        )
    connector = ("<span style='flex:1; height:2px; background:#e5e7eb; "
                 "min-width:4px;'></span>")
    row = connector.join(pills)

    st.markdown(
        f"""
        <div style='margin:0 0 6px 0;'>
            <div style='font-size:12px; font-weight:600; color:#0F4C2C;
                        margin-bottom:6px;'>
                Step {idx} of {total} · {label}
            </div>
            <div style='display:flex; align-items:center; gap:3px;'>
                {row}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pagehead(step, title, subtitle=""):
    """Polished gradient page header for an inner page (replaces a bare st.title).

    `step`     short kicker, e.g. "Step 3 of 9 · Principle 1"
    `title`    the page title, e.g. "Ethics & Transparency"
    `subtitle` optional one-line description.

    Visual layer only — emits CSS + the header markup. The CSS is bundled here
    (including the Sora font @import and the `ecospin` keyframe) so it renders
    correctly on every inner page, not just Home. Emitted each run because
    Streamlit re-renders markup on every rerun.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&display=swap');
        @keyframes ecospin { to { transform: rotate(360deg); } }
        .eco-pagehead {
            position: relative; overflow: hidden;
            border-radius: 18px; padding: 22px 26px; margin: 2px 0 16px;
            background:
                radial-gradient(120% 160% at 0% 0%, rgba(22,163,74,0.26) 0%, rgba(22,163,74,0) 55%),
                radial-gradient(130% 160% at 100% 100%, rgba(99,102,241,0.18) 0%, rgba(99,102,241,0) 55%),
                linear-gradient(135deg, #07291A 0%, #0F4C2C 60%, #0B3A22 100%);
            box-shadow: 0 16px 40px -26px rgba(15,76,44,0.6);
        }
        .eco-pagehead::after {
            content:""; position:absolute; inset:-40%;
            background: conic-gradient(from 0deg at 50% 50%, transparent 0deg, rgba(220,252,231,0.07) 120deg, transparent 240deg);
            animation: ecospin 22s linear infinite; pointer-events:none;
        }
        .eco-pagehead > * { position: relative; z-index: 1; }
        .eco-pagehead .step { font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase;
                              color:#BBF7D0; margin-bottom:6px; }
        .eco-pagehead h2 { font-family:'Sora',sans-serif; font-weight:800; font-size:24px;
                           color:#FFFFFF !important; margin:0 0 4px; letter-spacing:-0.02em; }
        .eco-pagehead p { font-size:13.5px; color:#CDEAD9; line-height:1.5; margin:0; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="eco-pagehead">
            <div class="step">{step}</div>
            <h2>{title}</h2>
            {sub}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_footer():
    render_whatsapp_fab()
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align:center; padding: 4px 0;'>
                <a href='https://forms.gle/ZAvGwN25sCPT3gU3A' target='_blank'
                   style='display:inline-block; padding:8px 14px;
                          background:#0F4C2C; color:white;
                          border-radius:8px; text-decoration:none;
                          font-size:13px; font-weight:600;'>
                    🌱 Join the Founding 100
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div style='font-size:11.5px; color:#666; text-align:center;
                        line-height:1.6; padding: 10px 4px 4px;'>
                Built by <b style='color:#0F4C2C;'>Meet Vaghani</b><br>
                Certified ESG Professional<br><br>
                <a href='mailto:meet.vaghani9909@gmail.com'
                   style='color:#666; text-decoration:none;'>
                   meet.vaghani9909@gmail.com
                </a><br>
                <a href='https://ecosetu.co.in'
                   style='color:#0F4C2C; text-decoration:none; font-weight:600;'>
                   ecosetu.co.in
                </a>
            </div>
            <div style='font-size:10.5px; color:#999; text-align:center;
                        margin-top:14px; padding-top:8px;
                        border-top:1px solid #eee;'>
                Made in India 🇮🇳<br>
                An initiative by Keprin Overseas Corporation<br>
                © 2026 Ecosetu
            </div>
            """,
            unsafe_allow_html=True,
        )