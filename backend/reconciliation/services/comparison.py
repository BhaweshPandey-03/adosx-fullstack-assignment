from collections import defaultdict

from reconciliation.models import SystemARecord, SystemBRecord


MISSING_IN_B = "MISSING_IN_B"
ORPHAN_IN_B = "ORPHAN_IN_B"
DUPLICATE_IN_B = "DUPLICATE_IN_B"
VALUE_MISMATCH = "VALUE_MISMATCH"


def build_b_lookup(system_b_records):
    """
    Group System B entries by tenant-aware record key.
    """

    lookup = defaultdict(list)

    for record in system_b_records:
        org_id = record.location.organization.org_id
        key = (org_id, record.normalized_record_ref)

        lookup[key].append(record)

    return lookup


def record_key(org_id, record_id):
    return org_id, record_id

def get_record_key_from_a(record):
    org_id = record.location.organization.org_id
    return record_key(org_id, record.record_id)

def find_disagreements():
    system_a_records = list(
        SystemARecord.objects.select_related(
            "location",
            "location__organization",
        )
    )

    system_b_records = list(
        SystemBRecord.objects.select_related(
            "location",
            "location__organization",
        )
    )

    b_lookup = build_b_lookup(system_b_records)

    disagreements = []
    matched_b_keys = set()

    for a_record in system_a_records:
        key = get_record_key_from_a(a_record)
        b_entries = b_lookup.get(key, [])

        if not b_entries:
            disagreements.append({
                "reason": MISSING_IN_B,
                "record_id": a_record.record_id,
                "org_id": a_record.location.organization.org_id,
                "location_id": a_record.location.location_id,
                "system_a_value": a_record.total_value,
                "system_b_value": None,
            })

            continue

        matched_b_keys.add(key)

        if len(b_entries) > 1:
            disagreements.append({
                "reason": DUPLICATE_IN_B,
                "record_id": a_record.record_id,
                "org_id": a_record.location.organization.org_id,
                "location_id": a_record.location.location_id,
                "system_a_value": a_record.total_value,
                "system_b_value": b_entries[0].value,
                "duplicate_count": len(b_entries),
            })

            continue

        b_record = b_entries[0]

        if a_record.total_value != b_record.value:
            disagreements.append({
                "reason": VALUE_MISMATCH,
                "record_id": a_record.record_id,
                "org_id": a_record.location.organization.org_id,
                "location_id": a_record.location.location_id,
                "system_a_value": a_record.total_value,
                "system_b_value": b_record.value,
            })

    for key, b_entries in b_lookup.items():
        if key in matched_b_keys:
            continue

        for b_record in b_entries:
            disagreements.append({
                "reason": ORPHAN_IN_B,
                "record_id": b_record.normalized_record_ref,
                "org_id": b_record.location.organization.org_id,
                "location_id": b_record.location.location_id,
                "system_a_value": None,
                "system_b_value": b_record.value,
            })

    return disagreements