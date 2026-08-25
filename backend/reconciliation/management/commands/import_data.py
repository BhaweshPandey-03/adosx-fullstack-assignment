from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from reconciliation.services.importer import import_all


class Command(BaseCommand):
    help = "Import the ADOSX CSV dataset into the database."

    def handle(self, *args, **options):
        data_dir = Path(settings.BASE_DIR).parent / "data"

        self.stdout.write("Starting data import...")

        result = import_all(data_dir)

        self.stdout.write(
            self.style.SUCCESS(
                f"Locations imported: {result['locations']}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "System A: "
                f"{result['system_a_imported']}/"
                f"{result['system_a_processed']} rows imported"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "System B: "
                f"{result['system_b_imported']}/"
                f"{result['system_b_processed']} rows imported"
            )
        )

        self.stdout.write(
            self.style.SUCCESS("Import completed successfully.")
        )