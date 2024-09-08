from django.contrib.auth.models import User
from django.db import models


class MerchantBusinessOperationType(models.Model):
    # Name of the business operation type, e.g., "Wholesaler", "Retailer"
    name = models.CharField(max_length=100, unique=True)

    # Optional description of the business operation type
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
        db_table = 'MerchantBusinessOperationType'
        verbose_name = 'Merchant Business Operation Type'
        verbose_name_plural = 'Merchant Business Operation Types'
