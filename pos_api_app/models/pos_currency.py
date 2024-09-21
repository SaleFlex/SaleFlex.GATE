from django.db import models
from django.contrib.auth.models import User


class PosCurrency(models.Model):
    # Currency number (unique for each currency)
    no = models.IntegerField()

    # Name of the currency (e.g., United States Dollar)
    name = models.CharField(max_length=255)

    # Currency rate (e.g., exchange rate)
    rate_of_currency = models.DecimalField(max_digits=10, decimal_places=2)

    # ISO currency code (e.g., 840 for USD)
    currency_code = models.IntegerField()

    # Currency sign (e.g., $)
    sign = models.CharField(max_length=10)

    # Sign direction (e.g., 'R' for right, 'L' for left)
    sign_direction = models.CharField(max_length=1)

    # Currency symbol (e.g., USD)
    currency_symbol = models.CharField(max_length=10)

    # Foreign key to POS, optional, allows the form to be related to specific POS devices
    pos = models.ForeignKey('PointOfSale', on_delete=models.SET_NULL, null=True, blank=True, related_name='currencies')

    # Foreign key to Store, optional, allows the form to be sent to all POS devices in a store
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='currencies')

    # Foreign key to Merchant, optional, allows the form to be sent to all stores and POS devices under the merchant
    merchant = models.ForeignKey('Merchant', on_delete=models.SET_NULL, null=True, blank=True, related_name='currencies')

    # A field to track if the currency is currently active
    is_active = models.BooleanField(default=True)

    # Optional effective date for when the currency rate becomes applicable
    effective_date = models.DateTimeField(null=True, blank=True)

    # Optional expiration date for when the currency rate is no longer valid
    expiration_date = models.DateTimeField(null=True, blank=True)

    # Indicates if the currency entry has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for deletion (if applicable)
    delete_description = models.CharField(max_length=255)

    # Foreign key to the User model, represents the user who created this currency entry
    created_by = models.ForeignKey(User, related_name='currency_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the currency entry is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this currency entry
    updated_by = models.ForeignKey(User, related_name='currency_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the currency entry is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['no', 'pos', 'merchant', 'store'], name='unique_currency_for_merchant_store')
        ]

    def __str__(self):
        return f"Currency {self.name} - {self.currency_symbol} ({self.no})"
