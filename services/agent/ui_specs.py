"""Builders for A2UI panel specs emitted back to the frontend.

Each spec names a panel registered in apps/web/lib/registerPanels.ts and carries
the props that panel expects. The agent generatively decides which panels to
emit; the frontend maps each name to a React component and renders it.
"""
from typing import Any


def panel(name: str, props: dict[str, Any]) -> dict[str, Any]:
    return {"type": "panel", "name": name, "props": props}


def competitor_table(competitors: list[dict]) -> dict[str, Any]:
    return panel("CompetitorTable", {"competitors": competitors})


def market_summary(
    business_type: str, area: str, competitors: list[dict]
) -> dict[str, Any]:
    rated = [c for c in competitors if isinstance(c.get("rating"), (int, float))]
    reviewed = [
        c for c in competitors if isinstance(c.get("reviews"), (int, float))
    ]
    avg_rating = round(sum(c["rating"] for c in rated) / len(rated), 2) if rated else None
    total_reviews = int(sum(c["reviews"] for c in reviewed)) if reviewed else 0
    top = max(reviewed, key=lambda c: c["reviews"], default=None)

    count = len(competitors)
    if count == 0:
        saturation = "Unknown"
    elif count <= 4:
        saturation = "Low — room to enter"
    elif count <= 9:
        saturation = "Moderate — competitive"
    else:
        saturation = "High — crowded market"

    return panel(
        "MarketSummary",
        {
            "businessType": business_type,
            "area": area,
            "competitorCount": count,
            "avgRating": avg_rating,
            "totalReviews": total_reviews,
            "topPlayer": top.get("name") if top else None,
            "saturation": saturation,
        },
    )


def ratings_chart(competitors: list[dict]) -> dict[str, Any]:
    bars = [
        {"name": c.get("name", "?"), "rating": float(c["rating"])}
        for c in competitors
        if isinstance(c.get("rating"), (int, float))
    ]
    bars.sort(key=lambda b: b["rating"], reverse=True)
    return panel("RatingsChart", {"bars": bars[:10], "max": 5})
