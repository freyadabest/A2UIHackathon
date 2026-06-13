"""Canned dashboard inputs for OFFLINE=1 mode.

When OFFLINE=1 is set, the /fixed agent serves a deterministic sample
dashboard with NO Gemini call and no API key (see fixed_agent.py). These
args are passed verbatim to `render_dashboard(**OFFLINE_DASHBOARD_ARGS)`,
so they MUST satisfy that tool's typed inputs:

  - eyebrow / title / subtitle: str
  - kpis: EXACTLY 4 × {label, value, delta, caption}     (Kpi)
  - trend: 6-12 × {label, value: float}                  (Point)
  - share: 3-5 × {label, value: float}                   (Point)
  - rows: 5-8 × {name, category, value, delta}           (Row)
  - scope_options: 3-6 × {label, value}                  (ScopeOption)
  - scope_selected: str (one of scope_options' values)

Dataset: a Vantage AI competitive scan for opening a Pilates studio in
Shoreditch. The numbers are illustrative-but-plausible (competitor count,
average rating, average monthly price, an opportunity score, a weekly
demand curve, a service-mix share, and a competitor row table). This
mirrors the live Linkup-backed shape the online /fixed agent produces, so
the OFFLINE fallback stays on-domain.
"""
from __future__ import annotations

from typing import Any

# Keep this a plain dict of JSON-ish primitives so it round-trips cleanly as
# tool-call args and through a2ui.render(...). Field names match the
# TypedDicts in fixed_agent.py (Kpi / Point / Row / ScopeOption) exactly.
OFFLINE_DASHBOARD_ARGS: dict[str, Any] = {
    "eyebrow": "SHOREDITCH · PILATES",
    "title": "Competitive landscape",
    "subtitle": "11 studios within ~1.5km. The market is busy on mat classes but mid-tier ratings leave a premium reformer gap.",
    "kpis": [
        {
            "label": "Competitors nearby",
            "value": "11",
            "delta": "",
            "caption": "within ~1.5 km of Shoreditch",
        },
        {
            "label": "Avg rating",
            "value": "4.3\u2605",
            "delta": "+0.2",
            "caption": "vs. 4.1 London avg",
        },
        {
            "label": "Avg monthly price",
            "value": "\u00a3165",
            "delta": "+9%",
            "caption": "unlimited mat + reformer",
        },
        {
            "label": "Opportunity score",
            "value": "72/100",
            "delta": "+12%",
            "caption": "premium reformer gap",
        },
    ],
    # Weekly demand curve — estimated class fill-rate by day. 7 points.
    "trend": [
        {"label": "Mon", "value": 68},
        {"label": "Tue", "value": 74},
        {"label": "Wed", "value": 81},
        {"label": "Thu", "value": 77},
        {"label": "Fri", "value": 64},
        {"label": "Sat", "value": 89},
        {"label": "Sun", "value": 58},
    ],
    # Service mix across nearby studios (% of classes). 4 slices.
    "share": [
        {"label": "Reformer", "value": 42},
        {"label": "Mat", "value": 33},
        {"label": "Barre", "value": 15},
        {"label": "Clinical", "value": 10},
    ],
    # Competitor table. 6 rows (within the 5-8 range).
    "rows": [
        {
            "name": "Shoreditch Pilates Lab",
            "category": "Shoreditch",
            "value": "4.7\u2605 · \u00a3189",
            "delta": "+14%",
        },
        {
            "name": "Hoxton Reformer Co.",
            "category": "Hoxton",
            "value": "4.5\u2605 · \u00a3175",
            "delta": "+8%",
        },
        {
            "name": "Core Collective EC2",
            "category": "Shoreditch",
            "value": "4.2\u2605 · \u00a3160",
            "delta": "+3%",
        },
        {
            "name": "Bethnal Green Body",
            "category": "Bethnal Green",
            "value": "4.0\u2605 · \u00a3135",
            "delta": "-2%",
        },
        {
            "name": "Old Street Studio",
            "category": "Old Street",
            "value": "4.4\u2605 · \u00a3155",
            "delta": "+6%",
        },
        {
            "name": "Brick Lane Mat Club",
            "category": "Shoreditch",
            "value": "3.9\u2605 · \u00a3120",
            "delta": "-5%",
        },
    ],
    # Scope chips tailored to a local-market scan (3-6 chips).
    "scope_options": [
        {"label": "Shoreditch", "value": "shoreditch"},
        {"label": "Hoxton", "value": "hoxton"},
        {"label": "Bethnal Green", "value": "bethnal_green"},
        {"label": "By rating", "value": "by_rating"},
        {"label": "By price", "value": "by_price"},
    ],
    "scope_selected": "shoreditch",
}
