"""
progress_io.py — Save & Resume for the Ecosetu BRSR tool.

No backend, no accounts, zero server storage. A user can DOWNLOAD a small
"progress file" at any point and later RE-UPLOAD it to restore every input
exactly where they left off.

The file is a base64-encoded JSON "envelope":

    {
        "schema":    "ecosetu-brsr/v1",
        "saved_utc": "2026-06-30T12:34:56.789012+00:00",
        "state":     { ...only the allowlisted keys... }
    }

This module deliberately does NOT import Streamlit, so the round-trip
(dump -> load) can be unit-tested in isolation with a plain dict.
`dump_progress` / `load_progress` accept any dict-like object, so the live
`st.session_state` works too.
"""

import base64
import json
from datetime import datetime, timezone

# ─────────────────────────────────────────────────────────────────────────────
# Envelope schema. Bump the version if the saved shape ever changes in a way
# that older files can't be read; load_progress checks this and refuses
# unknown schemas with a friendly message.
# ─────────────────────────────────────────────────────────────────────────────
SCHEMA = "ecosetu-brsr/v1"

# ─────────────────────────────────────────────────────────────────────────────
# SAVE_KEYS — the actual ANSWER DATA. These are the working dicts/lists that
# hold everything the user has typed. Confirmed by reading each page's
# `<var> = st.session_state.<key>` binding.
#
#   data          Section A working dict (pages/1_Section_A.py)
#   data_b        Section B working dict (pages/2_Section_B.py)
#   c_p1          Principle 1 (pages/3_Principle_1.py)
#   c_p2          Principle 2 (pages/4_Principle_2.py)
#   p3 / c_p3     Principle 3 live dict + mirror (pages/5_Principle_3.py)
#   p45 / c_p45   Principle 4&5 live dict + mirror (pages/6_Principle_4_5.py)
#   p6 / c_p6     Principle 6 live dict + mirror (pages/7_Principle_6.py)
#   p789 / c_p789 Principle 7,8,9 live dict + mirror (pages/8_Principle_7_8_9.py)
#   lca_entries, risk_entries, reclaimed_categories
#                 P2 dynamic lists (pages/4_Principle_2.py)
#   business_type top-level business mode string (business_profile.py)
#
# We save BOTH the live dict and its `c_*` mirror wherever both exist, so no
# data is lost regardless of which one a page reads on the next run.
# ─────────────────────────────────────────────────────────────────────────────
SAVE_KEYS = [
    "data",
    "data_b",
    "c_p1",
    "c_p2",
    "p3", "c_p3",
    "p45", "c_p45",
    "p6", "c_p6",
    "p789", "c_p789",
    "lca_entries", "risk_entries", "reclaimed_categories",
    "business_type",
]

# ─────────────────────────────────────────────────────────────────────────────
# NAV_KEYS — the user's POSITION (which page/step/mode they were on). Restoring
# these drops them back exactly where they left off rather than at step 1.
# ─────────────────────────────────────────────────────────────────────────────
NAV_KEYS = [
    "step",
    "step_b",
    "step_c_p1",
    "step_c_p2",
    "p3_mode", "p3_quick_step", "p3_full_step",
    "p45_mode", "p45_quick_step", "p45_full_step",
    "p6_mode", "p6_quick_step", "p6_full_step",
    "p789_mode", "p789_quick_step", "p789_full_step",
]

# Everything we persist = data + navigation.
PERSIST_KEYS = SAVE_KEYS + NAV_KEYS

# Reserved bookkeeping key the page uses to avoid re-applying the same upload
# on every rerun. Never cleared, never persisted.
UPLOAD_TRACKER_KEY = "_resume_applied_file_id"

# Keys that must survive a restore even though they aren't persisted. The
# whitelist-clear step below deletes everything NOT in this set so that keyed
# widgets re-seed from the restored `value=`. We must keep our own tracker and
# the persisted keys themselves.
_KEEP_ON_CLEAR = set(PERSIST_KEYS) | {UPLOAD_TRACKER_KEY}


def _json_default(o):
    """Best-effort serializer for odd types (sets, etc.). Tuples/lists/dicts/
    primitives go through json natively; this is a safety net."""
    if isinstance(o, set):
        return list(o)
    # Fall back to string so a stray exotic object never breaks the save.
    return str(o)


def dump_progress(state):
    """
    Build the downloadable progress token (a base64 ASCII string) from a
    dict-like `state` (st.session_state or a plain dict).

    Only PERSIST_KEYS that are actually present are included.
    """
    snapshot = {}
    for k in PERSIST_KEYS:
        if k in state:
            snapshot[k] = state[k]

    envelope = {
        "schema": SCHEMA,
        "saved_utc": datetime.now(timezone.utc).isoformat(),
        "state": snapshot,
    }

    raw = json.dumps(envelope, default=_json_default, ensure_ascii=False)
    token = base64.b64encode(raw.encode("utf-8")).decode("ascii")
    return token


def load_progress(token, state):
    """
    Restore a progress token into `state` (dict-like; supports __setitem__,
    __delitem__, __contains__, and key iteration via list(state.keys())).

    Returns (ok: bool, message: str) — a friendly message either way; never
    raises on bad input.

    CRITICAL widget-clearing step: Streamlit keyed widgets store their value in
    session_state[key], and `value=` only seeds on the FIRST render. After we
    write the restored answer data, we delete every session_state key that is
    NOT one of our persisted/reserved keys, forcing every widget to re-seed
    from the restored working dicts on the next run. Without this, the screen
    would still show the old widget values.
    """
    # 1) base64 decode
    try:
        raw = base64.b64decode(token, validate=True).decode("utf-8")
    except Exception:
        return False, ("This doesn't look like a valid Ecosetu progress file. "
                       "Please upload the .ecosetu file you downloaded earlier.")

    # 2) JSON parse
    try:
        envelope = json.loads(raw)
    except Exception:
        return False, ("This file is corrupted and couldn't be read. "
                       "Try the original .ecosetu file you downloaded.")

    # 3) shape / schema check
    if not isinstance(envelope, dict) or "schema" not in envelope or "state" not in envelope:
        return False, ("This file isn't an Ecosetu progress file. "
                       "Please upload the .ecosetu file you downloaded from this tool.")

    if envelope.get("schema") != SCHEMA:
        return False, (f"This progress file was made by a different version "
                       f"({envelope.get('schema')!r}) and can't be opened here.")

    snapshot = envelope.get("state")
    if not isinstance(snapshot, dict):
        return False, "This progress file is empty or damaged."

    # 4) write restored values (only known keys; ignore anything unexpected)
    restored = 0
    for k in PERSIST_KEYS:
        if k in snapshot:
            state[k] = snapshot[k]
            restored += 1

    # 5) CRITICAL: clear transient widget keys so widgets re-seed from value=
    for k in list(state.keys()):
        if k not in _KEEP_ON_CLEAR:
            try:
                del state[k]
            except Exception:
                # Some Streamlit-internal keys can't be deleted; ignore them.
                pass

    saved = envelope.get("saved_utc", "")
    when = f" (saved {saved})" if saved else ""
    return True, f"Progress restored{when}. {restored} section(s) loaded."
