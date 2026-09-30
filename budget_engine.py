"""Deterministic budget allocation and safe fallback recommendations."""

from __future__ import annotations

from datetime import datetime, timezone
from math import floor
from uuid import uuid4

from app.models import (
    BudgetItem,
    Category,
    GeminiDraft,
    GeminiDraftItem,
    Preference,
    RecommendationRequest,
    RecommendationResponse,
)


CATEGORY_META = {
    Category.HOME: {
        "title": "Home Interior",
        "description": "Furniture, lighting, décor and practical storage.",
        "icons": ["🛋️", "🪵", "💡", "🖼️", "🪴", "🧺", "🪑", "✨"],
        "items": [
            ("Sofa or seating", "Comfortable everyday seating", 34),
            ("Coffee table", "A practical centre-piece", 14),
            ("Lighting", "Warm and efficient lighting", 13),
            ("Wall décor", "Adds personality to the room", 11),
            ("Indoor plants", "A fresh, low-cost finishing touch", 8),
            ("Storage basics", "Keeps the space organised", 10),
        ],
    },
    Category.PARTY: {
        "title": "Party Planner",
        "description": "Venue, food, decoration and event essentials.",
        "icons": ["🏛️", "🍽️", "🎈", "📸", "🔊", "🎁", "🎂", "✨"],
        "items": [
            ("Venue setup", "Space and basic arrangements", 22),
            ("Food & refreshments", "The main guest experience", 30),
            ("Decoration", "Theme-focused visual setup", 14),
            ("Photography", "Captures important moments", 12),
            ("Music & sound", "Simple event entertainment", 8),
            ("Return gifts", "A small thank-you for guests", 4),
        ],
    },
    Category.JEWELLERY: {
        "title": "Jewellery",
        "description": "A balanced purchase plan with quality and storage checks.",
        "icons": ["💎", "✨", "🪙", "📦", "🧾", "💍", "🔒", "⭐"],
        "items": [
            ("Main jewellery piece", "The priority item for your style", 46),
            ("Matching accessory", "Completes the selected set", 20),
            ("Everyday piece", "Useful for regular wear", 14),
            ("Storage box", "Protects and organises the items", 5),
            ("Quality check", "Covers hallmark and purchase checks", 5),
        ],
    },
}

SPEND_RATIOS = {
    Preference.ESSENTIAL: 0.84,
    Preference.BALANCED: 0.90,
    Preference.PREMIUM: 0.94,
}


def fallback_draft(request: RecommendationRequest) -> GeminiDraft:
    meta = CATEGORY_META[request.category]
    items = [
        GeminiDraftItem(name=name, reason=reason, weight=weight)
        for name, reason, weight in meta["items"]
    ]
    note_hint = f" Your request — {request.notes} — has been considered." if request.notes else ""
    summary = (
        f"A practical {request.preference.value.lower()} {meta['title'].lower()} plan "
        f"that protects a safety reserve.{note_hint}"
    )
    return GeminiDraft(summary=summary[:240], items=items)


def _allocate_units(total_rupees: int, weights: list[float]) -> list[int]:
    """Allocate a ₹100-aligned target using a largest-remainder method."""
    units = total_rupees // 100
    safe_weights = [max(float(weight), 0.01) for weight in weights]
    weight_total = sum(safe_weights)
    exact = [(units * weight) / weight_total for weight in safe_weights]
    allocated = [floor(value) for value in exact]

    # Keep every displayed recommendation meaningful where the target permits it.
    if units >= len(allocated):
        allocated = [max(value, 1) for value in allocated]

    difference = units - sum(allocated)
    if difference > 0:
        order = sorted(range(len(exact)), key=lambda index: exact[index] - floor(exact[index]), reverse=True)
        for offset in range(difference):
            allocated[order[offset % len(order)]] += 1
    elif difference < 0:
        order = sorted(range(len(allocated)), key=lambda index: allocated[index], reverse=True)
        while difference < 0:
            changed = False
            for index in order:
                if allocated[index] > 1:
                    allocated[index] -= 1
                    difference += 1
                    changed = True
                    if difference == 0:
                        break
            if not changed:
                break

    return [value * 100 for value in allocated]


def build_plan(
    request: RecommendationRequest,
    draft: GeminiDraft,
    *,
    source: str,
    model: str | None = None,
) -> RecommendationResponse:
    meta = CATEGORY_META[request.category]
    spend_ratio = SPEND_RATIOS[request.preference]
    target = round((request.budget * spend_ratio) / 100) * 100
    target = min(request.budget, max(0, target))

    amounts = _allocate_units(target, [item.weight for item in draft.items])
    icons = meta["icons"]
    items = [
        BudgetItem(
            icon=(item.icon or icons[index % len(icons)])[:8],
            name=item.name,
            reason=item.reason,
            amount=amounts[index],
        )
        for index, item in enumerate(draft.items)
    ]
    total = sum(item.amount for item in items)

    return RecommendationResponse(
        plan_id=str(uuid4()),
        category=request.category,
        title=meta["title"],
        preference=request.preference,
        budget=request.budget,
        notes=request.notes,
        summary=draft.summary,
        items=items,
        total=total,
        remaining=request.budget - total,
        source=source,
        model=model,
        generated_at=datetime.now(timezone.utc),
    )


def build_fallback_plan(request: RecommendationRequest) -> RecommendationResponse:
    return build_plan(request, fallback_draft(request), source="smart_fallback")
