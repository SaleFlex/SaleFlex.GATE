from django.contrib.auth.models import User
from django.db import models


class MerchantActivitySector(models.Model):
    # Sector the merchant operates in, e.g., "Electronics", "Clothing", "Food & Beverage"
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)

    # Foreign key to the User model, represents the user who created this country record
    created_by = models.ForeignKey(User, related_name='country_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the country record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this country record
    updated_by = models.ForeignKey(User, related_name='country_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the country record is updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'MerchantActivitySector'
