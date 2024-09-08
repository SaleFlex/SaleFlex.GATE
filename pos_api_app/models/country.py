from django.contrib.auth.models import User
from django.db import models


class Country(models.Model):
    # Full name of the country, e.g., "United States", "Turkey"
    name = models.CharField(max_length=150)

    # Short code of the country, e.g., "US" or "TR"
    code = models.CharField(max_length=50, null=True, blank=True)

    # Abbreviation or short name of the country, e.g., "USA" or "Türkiye"
    short_name = models.CharField(max_length=50, null=True, blank=True)

    # Currency code of the country, e.g., "USD" or "TRY"
    currency_code = models.CharField(max_length=3, null=True, blank=True)

    # International phone code of the country, e.g., "+1" or "+90"
    phone_code = models.CharField(max_length=5, null=True, blank=True)

    # ISO 3166-1 alpha-2 country code, e.g., "US" or "TR"
    iso_alpha2 = models.CharField(max_length=2, null=True, blank=True)

    # ISO 3166-1 alpha-3 country code, e.g., "USA" or "TUR"
    iso_alpha3 = models.CharField(max_length=3, null=True, blank=True)

    # ISO 3166-1 numeric country code, e.g., "840" for the US or "792" for Turkey
    iso_numeric = models.CharField(max_length=3, null=True, blank=True)

    # ISO culture code, e.g., "en-US", "tr-TR"
    iso_culture_code = models.CharField(max_length=10, null=True, blank=True)

    # Time zone or multiple time zones of the country, e.g., "UTC-5" or ["UTC+3", "UTC+2"]
    time_zones = models.JSONField(null=True, blank=True)  # Can handle multiple time zones

    # Geographical region of the country, e.g., "Europe" or "Asia"
    region = models.CharField(max_length=100, null=True, blank=True)

    # Sub-region of the country, e.g., "Northern Europe" or "Western Asia"
    subregion = models.CharField(max_length=100, null=True, blank=True)

    # Official languages spoken in the country, e.g., ["English", "Spanish"] or ["Turkish"]
    languages = models.JSONField(null=True, blank=True)  # Can handle multiple languages

    # URL to the country's flag, useful for displaying flags in UI
    flag_url = models.URLField(max_length=500, null=True, blank=True)

    # The capital city of the country, e.g., "Washington, D.C." or "Ankara"
    capital_city = models.CharField(max_length=100, null=True, blank=True)

    # Indicates if the country has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for why the country was deleted
    delete_description = models.TextField(null=True, blank=True)

    # Foreign key to the User model, represents the user who created this country record
    created_by = models.ForeignKey(User, related_name='country_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the country record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this country record
    updated_by = models.ForeignKey(User, related_name='country_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the country record is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Country'
