from django.db import models
from django.contrib.auth.models import User


class State(models.Model):
    # Name of the state or region, e.g., "California", "Bavaria"
    name = models.CharField(max_length=150)

    # Abbreviation for the state, e.g., "CA" for California, "BY" for Bavaria
    abbreviation = models.CharField(max_length=10, null=True, blank=True)

    # Foreign key to the Country model to link this state to a specific country
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='states')

    # ISO 3166-2 code, e.g., "US-CA" for California, "DE-BY" for Bavaria
    iso_code = models.CharField(max_length=10, null=True, blank=True)

    # Capital city of the state or region
    capital_city = models.CharField(max_length=100, null=True, blank=True)

    # Time zone or multiple time zones in this state
    time_zones = models.JSONField(null=True, blank=True)

    # Indicates if the state has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for why the state was deleted
    delete_description = models.TextField(null=True, blank=True)

    # Foreign key to the User model, represents the user who created this state record
    created_by = models.ForeignKey(User, related_name='state_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the state record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this state record
    updated_by = models.ForeignKey(User, related_name='state_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the state record is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'State'
        unique_together = ('name', 'country')  # Ensures no duplicate state names within the same country
