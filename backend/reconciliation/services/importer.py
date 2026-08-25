import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from django.db import transaction

from reconciliation.models import (
    Location,
    Organization,
    SystemARecord,
    SystemBRecord,
)

def parse_decimal (value):
    """
    Convert a CSV value into decimal

    retrun: Decimal value when parsing succeeds, none when value is blank or invalid.
    """

    if value is None: 
        return None

    value = value.strip()

    if not value:
        return None

    normalized = value.replace(",", "")

    try:
        return Decimal(normalized)
    except InvalidOperation:
        return None

def parse_date(value):
    """
    Convert YYYY-MM-DD text into a python date
    returns: 
        date when parsing succeeds
        None when blank or invalid
    """

    if not value:
        return None

    value = value.strip()

    if not value:
        return None

    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None

def import_locations(file_path):
    imported = 0

    with open(file_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            raw_date = dict(row)

            org_id = row["org_id"].strip()
            location_id = row["location_id"].strip()
            location_name = row["location_name"].strip()

            organization, _ = Organization.objects.get_or_create(org_id=org_id)

            Location.objects.update_or_create(
                location_id=location_id,
                defaults={
                    "organization": organization,
                    "name": location_name,
                    "raw_data": raw_date,
                }
            )

            imported += 1

        return imported

def import_system_a(file_path):
    processed = 0
    imported = 0

    with open(file_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            processed += 1
            raw_data = dict(row)
            errors = []

            location_id = row["location_id"].strip()

            location = Location.objects.filter(
                location_id=location_id
            ).first()

            if location is None:
                errors.append(
                    f"Unknown location_id: {location_id}"
                )
                continue

            event_date = parse_date(row.get("event_date"))

            if row.get("event_date") and event_date is None:
                errors.append(
                    f"Invalid event_date: {row['event_date']}"
                )

            base_value = parse_decimal(row.get("base_value"))
            adjustment = parse_decimal(row.get("adjustment"))
            total_value = parse_decimal(row.get("total_value"))

            SystemARecord.objects.update_or_create(
                record_id=row["record_id"].strip(),
                defaults={
                    "location": location,
                    "event_date": event_date,
                    "category_code": row["category_code"].strip(),
                    "actor_id": row["actor_id"].strip() or None,
                    "base_value": base_value,
                    "adjustment": adjustment,
                    "total_value": total_value,
                    "state": row["state"].strip(),
                    "raw_data": raw_data,
                    "import_errors": errors,
                },
            )

            imported += 1

    return processed, imported
def import_system_b(file_path):
    processed = 0
    imported = 0

    with open(file_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            processed += 1
            raw_data = dict(row)
            errors = []

            location_id = row["location_id"].strip()

            location = Location.objects.filter(
                location_id=location_id
            ).first()

            if location is None:
                errors.append(
                    f"Unknown location_id: {location_id}"
                )
                continue

            recorded_on = parse_date(row.get("recorded_on"))

            if row.get("recorded_on") and recorded_on is None:
                errors.append(
                    f"Invalid recorded_on: {row['recorded_on']}"
                )

            value = parse_decimal(row.get("value"))

            if row.get("value") and value is None:
                errors.append(
                    f"Invalid value: {row['value']}"
                )

            record_ref = row["record_ref"].strip()

            SystemBRecord.objects.update_or_create(
                entry_id=row["entry_id"].strip(),
                raw_record_ref=record_ref,
                normalized_record_ref=record_ref,
                location=location,
                recorded_on=recorded_on,
                value=value,
                label=row["label"].strip() or None,
                raw_data=raw_data,
                import_errors=errors,
            )

            imported += 1

    return processed, imported
@transaction.atomic
def import_all(data_dir):
    data_dir = Path(data_dir)

    locations_count = import_locations(
        data_dir / "locations.csv"
    )

    system_a_processed, system_a_imported = import_system_a(
        data_dir / "system_a.csv"
    )

    system_b_processed, system_b_imported = import_system_b(
        data_dir / "system_b.csv"
    )

    return {
        "locations": locations_count,
        "system_a_processed": system_a_processed,
        "system_a_imported": system_a_imported,
        "system_b_processed": system_b_processed,
        "system_b_imported": system_b_imported,
    }


