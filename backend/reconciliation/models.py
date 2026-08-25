from django.db import models

# Create your models here.
class Organization (models.Model):
    org_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.org_id


class Location (models.Model):
    location_id = models.CharField(max_length=50, unique=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="locations",
    )
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.location_id


class SystemARecord(models.Model):
    record_id = models.CharField(max_length=50)
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="system_a_records",
    )
    event_date = models.DateField(null=True, blank=True)
    category_code = models.CharField(max_length=50, null=True, blank=True)
    actor_id = models.CharField(max_length=50, null=True, blank=True)
    base_value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True
    )
    adjustment = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True
    )
    total_value = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        blank=True,
        null=True
    )
    state = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.record_id


class SystemBRecord(models.Model):
    entry_id = models.CharField(max_length=50)
    raw_record_ref = models.CharField(max_length=100)
    normalized_record_ref = models.CharField(max_length=100)
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name="system_b_records"
    )
    recorded_on = models.DateField(null=True, blank=True)
    value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
    )
    label = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.entry_id
    