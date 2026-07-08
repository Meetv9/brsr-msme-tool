"""
scoring.py — Single source of truth for the OVERALL BRSR readiness score.

Both the Home screen and the generated PDF import from here, so the headline
number can never drift between the two. Pure Python: no Streamlit, no fpdf.

Strict readiness: every BRSR unit counts. A section the user has not filled
scores 0 and is still part of the denominator, so the overall number reflects
whole-report readiness — not just an average of the sections done so far.
"""

# The 7 scoreable BRSR units (Section B carries no numeric score of its own).
# Order matters only for display; the overall uses all of them as denominator.
BRSR_SECTION_KEYS = ("section_a", "p1", "p2", "p3", "p45", "p6", "p789")

# Human labels for the section-wise breakdown, in the same order.
BRSR_SECTION_LABELS = (
    ("section_a", "Section A"),
    ("p1", "P1"),
    ("p2", "P2"),
    ("p3", "P3"),
    ("p45", "P4+5"),
    ("p6", "P6"),
    ("p789", "P7+8+9"),
)


def strict_overall(section_scores):
    """Return the strict overall BRSR readiness score (0-100, rounded int).

    section_scores: dict mapping each key in BRSR_SECTION_KEYS to a 0-100 score.
    Missing keys or falsy values (None / 0) count as 0 across the FULL
    denominator of all 7 units, so unfilled sections drag the score down.
    """
    total = sum((section_scores.get(k) or 0) for k in BRSR_SECTION_KEYS)
    return round(total / len(BRSR_SECTION_KEYS))
