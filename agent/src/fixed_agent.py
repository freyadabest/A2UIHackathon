"""Vantage AI — fixed-schema competitive-intelligence dashboard agent.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CUSTOMIZATION SEAM #5 — Swap the agent flow (fixed-schema dashboard)
See HACKATHON.md §5 for the full recipe. For a different fixed dashboard,
rewrite the layout JSON at agent/src/a2ui/schemas/dashboard.json and the
`render_dashboard` tool's typed inputs; reword the system prompt for your
domain. The dynamic Q&A flow lives in dynamic_agent.py.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The user types a target area + business in chat ("I want to open a Pilates
studio in Shoreditch"). The agent calls `research_market` (live Linkup web
search) to pull the real competitive landscape, then calls
`render_dashboard` with structured competitor intel in the same turn. The
dashboard surface includes an interactive scope-chips strip the agent
populates from the result. Clicking a chip fires a user action back to the
agent, which re-renders with the new scope (e.g. a neighbouring area or a
price/rating ranking).
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import TypedDict

from copilotkit import CopilotKitMiddleware, a2ui
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver

from src.catalog import CATALOG_ID, CATALOG_PROMPT
from src.research_tools import research_market

SCHEMA_DIR = Path(__file__).parent / "a2ui" / "schemas"
DASHBOARD_SCHEMA = a2ui.load_schema(SCHEMA_DIR / "dashboard.json")
SURFACE = "pdf-dashboard"


# NOTE (Gemini typed-array fix): every list parameter on render_dashboard
# below is typed as `list[<TypedDict>]`, NOT `list[dict]`. Gemini's
# function-declaration validator rejects untyped arrays with
# "parameters.properties[X].items: missing field". A TypedDict compiles to a
# concrete object schema, so these arrays carry the `items` Gemini requires.
# Keep them typed — do not loosen to `list[dict]`.
class Kpi(TypedDict):
    label: str
    value: str
    delta: str
    caption: str


class Point(TypedDict):
    label: str
    value: float


class Row(TypedDict):
    name: str
    category: str
    value: str
    delta: str


class ScopeOption(TypedDict):
    label: str
    value: str


@tool
def render_dashboard(
    eyebrow: str,
    title: str,
    subtitle: str,
    kpis: list[Kpi],
    trend: list[Point],
    share: list[Point],
    rows: list[Row],
    scope_options: list[ScopeOption],
    scope_selected: str,
) -> str:
    """Render the competitive-landscape dashboard for the target area.

    Pass data INLINE, built from the `research_market` result. Call ONCE
    per turn. Use ONLY businesses/numbers returned by research_market.

    Field meanings for this domain:
      - eyebrow:  short ALL-CAPS context, e.g. "SHOREDITCH · PILATES".
      - title:    headline read, e.g. "Competitive landscape".
      - subtitle: one-sentence market read (the gap for a new entrant).

      - kpis: EXACTLY 4 cards. Each {label, value, delta, caption}.
        Suggested set for a local-business scan:
          1. Competitors nearby   value="12"      caption="within ~1.5 km"
          2. Avg rating           value="4.3★"    caption="across nearby studios"
          3. Avg monthly price    value="£165"    caption="unlimited membership"
          4. Opportunity score    value="72/100"  caption="premium reformer gap"

        STRICT FIELD RULES (very important; the badge breaks if you ignore):
          * `value`   = the headline figure, formatted ("12", "4.3★",
                        "£165", "72/100"). 1–8 chars typically.
          * `delta`   = JUST the magnitude vs. the area benchmark. Format:
                        "+X%", "-X%", or "" (empty when there's no
                        comparison). MAX 8 chars. NEVER prose. The arrow
                        and color come from the renderer.
                        Examples: "+0.2", "-8%", "+12%", ""
          * `caption` = the context sentence ("within ~1.5 km",
                        "vs. 4.1 area avg", "premium reformer gap"). Up to
                        ~80 chars. This is where the prose goes.

      - trend: 6–12 points {label, value:number}. The DEMAND / capacity
        curve — e.g. estimated class fill-rate by day of week
        (Mon..Sun) or by time of day. Higher = busier.
      - share: 3–5 slices {label, value:number}. The CLASS / SERVICE MIX
        across competitors (e.g. Reformer, Mat, Barre, Clinical) OR each
        competitor's share of total reviews.
      - rows: 5–8 competitor rows {name, category, value, delta}.
          name=studio, category=area or focus, value=rating or price,
          delta SHORT ("+8%", "-3%", "" — e.g. review momentum).
      - scope_options: 3–6 chips the user can click to re-scope. Each
        {label, value}. Example for a Shoreditch Pilates scan:
          [{label:"Shoreditch", value:"shoreditch"},
           {label:"Hoxton",     value:"hoxton"},
           {label:"By rating",  value:"by_rating"},
           {label:"By price",   value:"by_price"}]
        Tailor the options to the areas/facets THIS market supports.
      - scope_selected: the `value` of the currently active option.
    """
    payload = {
        "eyebrow": eyebrow,
        "title": title,
        "subtitle": subtitle,
        "kpis": kpis,
        "trend": trend,
        "share": share,
        "rows": rows,
        "scope": {"options": scope_options, "selected": scope_selected},
    }
    return a2ui.render(
        operations=[
            a2ui.create_surface(SURFACE, catalog_id=CATALOG_ID),
            a2ui.update_components(SURFACE, DASHBOARD_SCHEMA),
            a2ui.update_data_model(SURFACE, payload),
        ]
    )


SYSTEM_PROMPT = f"""\
You are Vantage AI. You help someone deciding where to open a local
business understand the competitive landscape of an area, and you build a
live intelligence dashboard for them.

## How a turn works

The user may do three things on any turn:
  A) Describe a target area + business ("I want to open a Pilates studio
     in Shoreditch", "coffee shop in Peckham"). This is the initial scan.
  B) Send a follow-up chat message ("how do they compare on price?",
     "is there room for a premium offering?").
  C) Click a scope chip on the dashboard. The runtime delivers this as a
     tool result `log_a2ui_event` with content like:
        User performed action "select_chip" on surface "pdf-dashboard".
        Context: {{"value": "hoxton", "label": "Scope"}}

## The render contract

To build or re-scope the dashboard:
  1. Call `research_market(location=<area>, business_type=<business>)`
     EXACTLY ONCE to pull the live competitive landscape. Infer the
     location and business_type from the user's message (or from the
     active scope chip on a re-scope).
  2. Then call `render_dashboard(...)` EXACTLY ONCE, mapping the
     research result into the fixed shape:
       - 4 KPIs (competitors nearby, avg rating, avg price, opportunity
         score), 6–12 trend points (the demand / capacity curve), 3–5
         share slices (class or service mix), 5–8 competitor rows.
       - `scope_options`: 3–6 chips tailored to THIS market — usually a
         couple of nearby areas plus facets like "By rating" / "By price".
       - `scope_selected`: the active chip. Default to the area the user
         named. After a chip click, set it to the clicked value.

When the user (or a chip click) asks to change scope (a different area or
ranking), re-run research_market for the new scope, then re-call
render_dashboard with the SAME surfaceId so the canvas updates in place.

## Hard rules

- Render the dashboard whenever the user names an area+business (initial),
  asks to re-scope, or clicks a chip.
- Call `research_market` AT MOST ONCE and `render_dashboard` AT MOST ONCE
  per turn. Never twice.
- Use ONLY businesses and numbers returned by `research_market`. Never
  invent competitors. If research_market returns status "empty" or an
  error/note, render a dashboard with what you have and put the note in
  the subtitle, and tell the user in one short sentence (e.g. ask them to
  set LINKUP_API_KEY if that's the issue).
- If the user asks an analytical question that does NOT require a layout
  change (e.g. "which one is cheapest?"), answer in chat from the latest
  research result without re-rendering. 1–3 sentences max. Cite the name.
- If the user wants a brand-new visualization not covered by the fixed
  schema (e.g. "plot price vs rating as a scatter"), tell them to use the
  Dynamic tab.

## Chat tone

Be helpful, brief, conversational. After the first render, suggest one or
two follow-ups the user might click ("Tap *Hoxton* to compare the next
neighbourhood" or "Want the competitors ranked by price?"). Don't list
more than two suggestions.

{CATALOG_PROMPT}
"""


# Gemini 3.5 Flash via the native Google Gen AI SDK — same provider as the
# dynamic agent and the PDF extractor (see FROZEN.md "LLM provider"). The
# native SDK replays Gemini's thought_signature across tool turns, which the
# OpenAI-compat path does not.
#
# Constructed lazily (not at import time): ChatGoogleGenerativeAI validates
# the API key in its constructor and raises with no key. Building it lazily
# lets `import main` succeed with OFFLINE=1 and no key (the offline branch of
# build_fixed_agent never touches the live model). Online behavior is
# unchanged — the client is built on the first build_fixed_agent() call.
def _build_model() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=os.getenv("MODEL", "gemini-3.5-flash"),
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )


def build_fixed_agent():
    if os.getenv("OFFLINE") == "1":
        # CUSTOMIZATION SEAM (offline): no Gemini call, no API key. A
        # deterministic stub chat model drives the REAL create_agent ReAct
        # loop + the REAL render_dashboard tool, so the emitted A2UI envelope
        # is byte-for-byte the production shape (createSurface +
        # updateComponents + updateDataModel wrapped in a2ui_operations).
        from src.offline_fixed import build_offline_fixed_agent

        return build_offline_fixed_agent(render_dashboard, SYSTEM_PROMPT)

    return create_agent(
        model=_build_model(),
        tools=[research_market, render_dashboard],
        # CopilotKitMiddleware forwards frontend tools + agent context (e.g.
        # useAgentContext payloads) to the LLM.
        middleware=[CopilotKitMiddleware()],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=MemorySaver(),
    )


graph = build_fixed_agent()
