from django.db import models
from django.contrib.auth.models import User


class PosVat(models.Model):
    # VAT number (must be unique for a POS-Store-Merchant combination)
    no = models.IntegerField()

    # Name of the VAT category
    name = models.CharField(max_length=255)

    # VAT rate (percentage)
    rate = models.IntegerField()

    # Description of the VAT category
    description = models.CharField(max_length=255)

    # Foreign key to POS, optional, allows the form to be related to specific POS devices
    pos = models.ForeignKey('PointOfSale', on_delete=models.SET_NULL, null=True, blank=True, related_name='forms')

    # Foreign key to Store, optional, allows the form to be sent to all POS devices in a store
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='forms')

    # Foreign key to Merchant, optional, allows the form to be sent to all stores and POS devices under the merchant
    merchant = models.ForeignKey('Merchant', on_delete=models.SET_NULL, null=True, blank=True, related_name='forms')

    # A field to track if the VAT is currently active (could be useful if some VAT rates change over time)
    is_active = models.BooleanField(default=True)

    # Optional effective date for when the VAT rate becomes applicable
    effective_date = models.DateTimeField(null=True, blank=True)

    # Optional expiration date for when the VAT rate is no longer valid
    expiration_date = models.DateTimeField(null=True, blank=True)

    # Indicates if the VAT entry has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for deletion (if applicable)
    delete_description = models.CharField(max_length=255)

    # Foreign key to the User model, represents the user who created this VAT entry
    created_by = models.ForeignKey(User, related_name='vat_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the VAT entry is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this VAT entry
    updated_by = models.ForeignKey(User, related_name='vat_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the VAT entry is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['no', 'pos', 'merchant', 'store'], name='unique_vat_for_merchant_store')
        ]

    def __str__(self):
        return f"VAT {self.name} - {self.no}"

