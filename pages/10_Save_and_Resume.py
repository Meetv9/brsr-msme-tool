import re
import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Save & Resume | Ecosetu BRSR",
    page_icon="💾",
    layout="centered",
)

from sidebar_footer import render_sidebar_footer
from business_profile import show_sidebar_logo
from progress_io import dump_progress, load_progress, UPLOAD_TRACKER_KEY

show_sidebar_logo()       # Ecosetu logo (sidebar + top-left), same as every page
render_sidebar_footer()

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .sr-hero {
        background: linear-gradient(135deg, #e8f5e9, #f1f8e9);
        border-left: 5px solid #2e7d32;
        padding: 16px 20px;
        border-radius: 0 12px 12px 0;
        margin: 6px 0 20px 0;
    }
    .sr-hero h3 { color: #1b5e20; margin: 0 0 4px 0; }
    .sr-hero p  { color: #2e7d32; margin: 0; font-size: 14px; line-height: 1.55; }
    /* Slightly tighter, card-like step containers */
    [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

st.title("💾 Save & Resume")

st.markdown("""
<div class='sr-hero'>
    <h3>Pick up exactly where you left off — no account needed</h3>
    <p>Your answers live only in your browser. Download a small <b>progress file</b>
    any time, and re-upload it later (on any device) to restore every answer and
    land back on the exact step you were on. Nothing is ever stored on our servers.</p>
</div>
""", unsafe_allow_html=True)

ss = st.session_state


def _has_content(v):
    """Defensive 'is this answer actually filled in?' check used only for the
    friendly summary below. Never raises."""
    try:
        if isinstance(v, dict):
            return any(_has_content(x) for x in v.values())
        if isinstance(v, (list, tuple, set)):
            return any(_has_content(x) for x in v)
        if isinstance(v, str):
            return v.strip() != ""
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return v != 0
        return v is not None
    except Exception:
        return False


# Friendly section labels for the "what's saved" summary (live dicts only).
_SECTION_LABELS = [
    ("data",   "Section A"),
    ("data_b", "Section B"),
    ("c_p1",   "Principle 1"),
    ("c_p2",   "Principle 2"),
    ("p3",     "Principle 3"),
    ("p45",    "Principles 4 & 5"),
    ("p6",     "Principle 6"),
    ("p789",   "Principles 7, 8 & 9"),
]

# ─────────────────────────────────────────────────────────────────────────────
# 1) DOWNLOAD — save current progress
# ─────────────────────────────────────────────────────────────────────────────
with st.container(border=True):
    st.subheader("1 · Save your progress")

    # Reassure the user what they're about to save.
    _filled = [label for key, label in _SECTION_LABELS if _has_content(ss.get(key))]
    if _filled:
        st.markdown(
            "Currently holding answers for: "
            + " ".join(
                f"<span style='display:inline-block; background:#e8f5e9; color:#1b5e20; "
                f"border:1px solid #a5d6a7; border-radius:12px; padding:1px 10px; "
                f"margin:2px 4px 2px 0; font-size:12px; font-weight:600;'>{s}</span>"
                for s in _filled
            ),
            unsafe_allow_html=True,
        )
    else:
        st.info("No answers entered yet. Fill in a section first, then come back to save — "
                "but you can still download an (empty) file to test it.")

    # Build a friendly filename from the company name, if entered.
    _company = ""
    if isinstance(ss.get("data"), dict):
        _company = (ss["data"].get("company_name") or "").strip()
    _slug = re.sub(r"[^A-Za-z0-9]+", "_", _company).strip("_").lower() if _company else ""
    _fname = f"{_slug}_brsr_progress.ecosetu" if _slug else "ecosetu_brsr_progress.ecosetu"

    _token = dump_progress(ss)

    st.download_button(
        label="⬇\ufe0f  Download progress file",
        data=_token,
        file_name=_fname,
        mime="application/octet-stream",
        use_container_width=True,
        type="primary",
    )
    st.caption(f"Saves as **{_fname}** — keep this file safe. Anyone with it can open your answers.")

    # ── Share the file (email / WhatsApp) ────────────────────────────────────
    with st.expander("📤  Email or WhatsApp this file to yourself"):
        st.markdown(
            "Browsers can't attach a file to an email or chat automatically, so do this "
            "in two quick steps:"
        )
        st.markdown(
            "1. **Download** the progress file above (it goes to your Downloads folder).\n"
            "2. Tap a button below — it opens your email / WhatsApp with the message "
            "ready. **Attach the downloaded `.ecosetu` file** before sending."
        )
        _subject = "My Ecosetu BRSR progress file"
        _body = ("Hi,%0A%0AHere is my Ecosetu BRSR progress file. "
                 "To continue, open the Ecosetu tool, go to Save %26 Resume, and upload "
                 "this file.%0A%0A(Remember to attach the .ecosetu file to this message.)")
        _wa = ("Here%27s%20my%20Ecosetu%20BRSR%20progress%20file.%20"
               "Open%20the%20tool%20%E2%86%92%20Save%20%26%20Resume%20%E2%86%92%20"
               "upload%20it%20to%20continue.%20(Attach%20the%20.ecosetu%20file%20here.)")
        c1, c2 = st.columns(2)
        c1.markdown(
            f"<a href='mailto:?subject={_subject.replace(' ', '%20')}&body={_body}' "
            "style='display:block; text-align:center; padding:9px 12px; "
            "background:#0F4C2C; color:#fff; border-radius:8px; text-decoration:none; "
            "font-weight:600; font-size:14px;'>✉️ Email it</a>",
            unsafe_allow_html=True,
        )
        c2.markdown(
            f"<a href='https://wa.me/?text={_wa}' target='_blank' rel='noopener' "
            "style='display:block; text-align:center; padding:9px 12px; "
            "background:#25D366; color:#fff; border-radius:8px; text-decoration:none; "
            "font-weight:600; font-size:14px;'>💬 WhatsApp it</a>",
            unsafe_allow_html=True,
        )

st.write("")

# ─────────────────────────────────────────────────────────────────────────────
# 2) UPLOAD — restore progress
# ─────────────────────────────────────────────────────────────────────────────
with st.container(border=True):
    st.subheader("2 · Resume from a saved file")
    st.caption("Upload a `.ecosetu` file you downloaded earlier to restore your answers.")

    uploaded = st.file_uploader(
        "Choose your progress file",
        type=["ecosetu"],
        label_visibility="collapsed",
    )

    if uploaded is not None:
        # Once-per-file guard: only apply each distinct upload a single time, so
        # reruns don't keep overwriting fresh edits.
        file_id = f"{uploaded.name}:{uploaded.size}"
        if ss.get(UPLOAD_TRACKER_KEY) != file_id:
            try:
                token = uploaded.getvalue().decode("ascii")
            except Exception:
                token = ""
            ok, msg = load_progress(token, ss)
            if ok:
                # Mark applied AFTER restoring (load keeps this key on its clear step).
                ss[UPLOAD_TRACKER_KEY] = file_id
                st.success("✅ " + msg)
                st.info("Your answers are restored. Open any section from the sidebar to continue.")
                st.balloons()
            else:
                st.error("⚠️ " + msg)
        else:
            st.success("✅ This file is already loaded. Open any section from the sidebar to continue.")

st.write("")

# ─────────────────────────────────────────────────────────────────────────────
# HOW IT WORKS
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("ℹ️  How does this work? (and is my data private?)"):
    st.markdown("""
**Everything stays in your browser.** This tool has no login and no database.
While you fill in answers, they live only in your current browser tab.

- **Save** bundles all your answers into one small file you download to your device.
- **Resume** reads that file back and restores every answer — including which step
  you were on — so you continue seamlessly, even on a different computer.
- We **never** see, store, or transmit your data. The file is yours alone.

**A few tips:**
- Download a fresh progress file before closing the tab, especially on shared/public
  computers (closing the tab clears unsaved answers).
- The file is plain text under the hood. Keep it private — anyone who opens it can
  read your answers.
- Always keep the **latest** file; uploading an older one restores older answers.
""")
