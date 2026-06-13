"""Builders for A2UI panel specs emitted back to the frontend over AG-UI.

Each spec names a panel registered in apps/web/lib/registerPanels.ts and carries
the props that panel expects.
"""
from typing import Any


def panel(name: str, props: dict[str, Any]) -> dict[str, Any]:
    return {"type": "panel", "name": name, "props": props}


def competitor_table(competitors: list[dict]) -> dict[str, Any]:
    return panel("CompetitorTable", {"competitors": competitors})
