from decimal import Decimal

from django.test import TestCase

from reconciliation.models import (
    Location,
    Organization,
    SystemARecord,
    SystemBRecord,
)
from reconciliation.services.comparison import (
    DUPLICATE_IN_B,
    MISSING_IN_B,
    ORPHAN_IN_B,
    VALUE_MISMATCH,
    find_disagreements,
)

class ComparisonTests(TestCase):

    def setUp(self):
        self.organization = Organization.objects.create(
            org_id="ORG-A"
        )

        self.location = Location.objects.create(
            location_id="LOC-101",
            organization=self.organization,
            name="Test Location",
            raw_data={},
        )

    def test_value_mismatch(self):
        SystemARecord.objects.create(
            record_id="REC-1001",
            location=self.location,
            total_value=Decimal("100.00"),
            raw_data={},
            import_errors=[],
        )

        SystemBRecord.objects.create(
            entry_id="ENT-001",
            raw_record_ref="REC-1001",
            normalized_record_ref="REC-1001",
            location=self.location,
            value=Decimal("200.00"),
            raw_data={},
            import_errors=[],
        )

        disagreements = find_disagreements()

        self.assertEqual(len(disagreements), 1)
        self.assertEqual(
            disagreements[0]["reason"],
            VALUE_MISMATCH,
        )

    def test_missing_in_b(self):
        SystemARecord.objects.create(
            record_id="REC-1002",
            location=self.location,
            total_value=Decimal("100.00"),
            raw_data={},
            import_errors=[],
        )

        disagreements = find_disagreements()

        self.assertEqual(len(disagreements), 1)
        self.assertEqual(
            disagreements[0]["reason"],
            MISSING_IN_B,
        )

    def test_orphan_in_b(self):
        SystemBRecord.objects.create(
            entry_id="ENT-002",
            raw_record_ref="REC-9999",
            normalized_record_ref="REC-9999",
            location=self.location,
            value=Decimal("100.00"),
            raw_data={},
            import_errors=[],
        )

        disagreements = find_disagreements()

        self.assertEqual(len(disagreements), 1)
        self.assertEqual(
            disagreements[0]["reason"],
            ORPHAN_IN_B,
        )

    def test_duplicate_in_b(self):
        SystemARecord.objects.create(
            record_id="REC-1003",
            location=self.location,
            total_value=Decimal("100.00"),
            raw_data={},
            import_errors=[],
        )

        SystemBRecord.objects.create(
            entry_id="ENT-003",
            raw_record_ref="REC-1003",
            normalized_record_ref="REC-1003",
            location=self.location,
            value=Decimal("100.00"),
            raw_data={},
            import_errors=[],
        )

        SystemBRecord.objects.create(
            entry_id="ENT-004",
            raw_record_ref="REC-1003",
            normalized_record_ref="REC-1003",
            location=self.location,
            value=Decimal("100.00"),
            raw_data={},
            import_errors=[],
        )

        disagreements = find_disagreements()

        self.assertEqual(len(disagreements), 1)
        self.assertEqual(
            disagreements[0]["reason"],
            DUPLICATE_IN_B,
        )
        self.assertEqual(
            disagreements[0]["duplicate_count"],
            2,
        )

    def test_same_record_id_different_org_is_not_matched(self):
        organization_b = Organization.objects.create(
            org_id="ORG-B"
        )

        location_b = Location.objects.create(
            location_id="LOC-201",
            organization=organization_b,
            name="Another Location",
            raw_data={},
        )

        SystemARecord.objects.create(
            record_id="REC-1077",
            location=self.location,
            total_value=Decimal("100.00"),
            raw_data={},
            import_errors=[],
        )

        SystemBRecord.objects.create(
            entry_id="ENT-1077",
            raw_record_ref="REC-1077",
            normalized_record_ref="REC-1077",
            location=location_b,
            value=Decimal("100.00"),
            raw_data={},
            import_errors=[],
        )

        disagreements = find_disagreements()

        reasons = {
            disagreement["reason"]
            for disagreement in disagreements
        }

        self.assertIn(MISSING_IN_B, reasons)
        self.assertIn(ORPHAN_IN_B, reasons)



    