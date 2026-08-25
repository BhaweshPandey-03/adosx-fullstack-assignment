from django.shortcuts import render
from decimal import Decimal

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from reconciliation.models import Organization
from reconciliation.services.comparison import (
    DUPLICATE_IN_B,
    MISSING_IN_B,
    ORPHAN_IN_B,
    VALUE_MISMATCH,
    find_disagreements,
)


VALID_REASONS = {
    MISSING_IN_B,
    ORPHAN_IN_B,
    DUPLICATE_IN_B,
    VALUE_MISMATCH,
}


def serialize_value(value):
    if isinstance(value, Decimal):
        return str(value)

    return value


def serialize_disagreement(item):
    return {
        "reason": item["reason"],
        "record_id": item["record_id"],
        "org_id": item["org_id"],
        "location_id": item["location_id"],
        "system_a_value": serialize_value(
            item["system_a_value"]
        ),
        "system_b_value": serialize_value(
            item["system_b_value"]
        ),
        "duplicate_count": item.get("duplicate_count"),
    }


@require_GET
def organizations(request):
    organizations = Organization.objects.order_by(
        "org_id"
    ).values("org_id")

    return JsonResponse(
        list(organizations),
        safe=False,
    )


@require_GET
def disagreements(request):
    org_id = request.GET.get("org_id")
    reason = request.GET.get("reason")
    sort = request.GET.get("sort")

    if reason and reason not in VALID_REASONS:
        return JsonResponse(
            {
                "error": "Invalid reason",
                "allowed_reasons": sorted(VALID_REASONS),
            },
            status=400,
        )

    items = find_disagreements()

    if org_id:
        items = [
            item
            for item in items
            if item["org_id"] == org_id
        ]

    if reason:
        items = [
            item
            for item in items
            if item["reason"] == reason
        ]

    if sort in {"value_asc", "value_desc"}:
        def sort_value(item):
            value = item["system_a_value"]

            if value is None:
                value = item["system_b_value"]

            return (
                value is None,
                value if value is not None else Decimal("0"),
            )

        items = sorted(
            items,
            key=sort_value,
            reverse=(sort == "value_desc"),
        )

    return JsonResponse(
        [serialize_disagreement(item) for item in items],
        safe=False,
    )