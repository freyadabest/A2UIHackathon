"""
This is the main entry point for the agent.
It defines the workflow graph, state, tools, nodes and edges.
"""

import os

from copilotkit import CopilotKitMiddleware, StateStreamingMiddleware, StateItem
from langchain.agents import create_agent

# State schema is domain-agnostic; tools are loaded per-domain below.
from src.todos import AgentState
from src.middleware.normalize_tools import NormalizeToolShapeMiddleware

from langchain_openai import ChatOpenAI

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CUSTOMIZATION SEAM ⊥ — LLM provider (FROZEN — do NOT change without instruction)
# See HACKATHON.md "If you get rate-limited" for the runbook.
# Pattern to copy: this block IS the canonical example; for provider swaps
# (OpenAI / Anthropic / LiteLLM) see .env.example.
#
# Default: Gemini 2.5 Flash via Google's OpenAI-compatible endpoint.
# Why 2.5 (not 3.5): Gemini 3.x requires thought_signature replay across
# tool turns (https://ai.google.dev/gemini-api/docs/thought-signatures);
# langchain-openai 1.1.9 does not implement this, so 3.5 Flash 400s after
# the first tool call. 2.5 Flash has no such requirement.
# Model ID empirically verified 2026-05-28 via scripts/probe-gemini.sh.
# See FROZEN.md for the full probe results and the 3.x upgrade path.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
model = ChatOpenAI(
    model=os.getenv("MODEL", "gemini-2.5-flash"),
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("MODEL_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/"),
    model_kwargs={"parallel_tool_calls": False},
)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# END CUSTOMIZATION SEAM ⊥ (LLM provider)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CUSTOMIZATION SEAM #5 — Switch domain (DOMAIN env)
# See HACKATHON.md §5 for the full recipe.
# Pattern to copy: agent/src/domains/shopping/ (canonical stub).
#
# Set DOMAIN=<name> in .env to swap the whole tool bundle + system prompt.
# Ships with two domains:
#   - default  → flights + dashboards + todos (inherited base demo)
#   - shopping → canonical stub: product search + order dashboards
# To add your own, copy agent/src/domains/shopping/ and add an elif branch.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOMAIN = os.getenv("DOMAIN", "default")
if DOMAIN == "default":
    from src.domains.default.tools import default_tools as _tools
    from src.domains.default.prompts import SYSTEM_PROMPT as _system_prompt
elif DOMAIN == "shopping":
    from src.a2ui_dynamic_schema import generate_a2ui
    from src.domains.shopping.tools import shopping_tools
    from src.domains.shopping.prompts import SYSTEM_PROMPT as _system_prompt
    _tools = [generate_a2ui, *shopping_tools]
else:
    raise ValueError(
        f"Unknown DOMAIN={DOMAIN!r}. Set DOMAIN=default or DOMAIN=shopping in .env, "
        f"or add a new branch in agent/main.py. See HACKATHON.md §5."
    )

agent = create_agent(
    model=model,
    tools=_tools,
    middleware=[
        CopilotKitMiddleware(),
        StateStreamingMiddleware(
            StateItem(state_key="todos", tool="manage_todos", tool_argument="todos")
        ),
        # Last so it sees the merged tools after CopilotKitMiddleware injects
        # frontend tools — reshapes them to strict OpenAI form for Gemini.
        NormalizeToolShapeMiddleware(),
    ],
    state_schema=AgentState,
    system_prompt=_system_prompt,
)

graph = agent
