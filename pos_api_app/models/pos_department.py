from django.db import models
from django.contrib.auth.models import User


class PosDepartment(models.Model):
    # Department number (required)
    no = models.IntegerField()

    # Name of the department (required)
    name = models.CharField(max_length=255)

    # Default price for the department (required)
    default_price = models.IntegerField()

    # Default quantity for the department (required)
    default_quantity = models.IntegerField()

    # Maximum price for items in this department (optional)
    max_price = models.IntegerField(null=True, blank=True)

    # Foreign key to the VAT (required), assuming a related model for VAT
    vat = models.ForeignKey('PosVat', on_delete=models.CASCADE)

    # Keyboard value (optional), allows null
    keyboard_value = models.CharField(max_length=255, null=True, blank=True)

    # Foreign key to POS, optional, allows the department to be related to specific POS devices
    pos = models.ForeignKey('PointOfSale', on_delete=models.SET_NULL, null=True, blank=True, related_name='departments')

    # Foreign key to Store, optional, allows the department to be sent to all POS devices in a store
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='departments')

    # Foreign key to Merchant, optional, allows the department to be sent to all stores and POS devices under the merchant
    merchant = models.ForeignKey('Merchant', on_delete=models.SET_NULL, null=True, blank=True, related_name='departments')

    # Indicates if the department has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for deletion (if applicable)
    delete_description = models.CharField(max_length=255, default=False, null=True)

    # Foreign key to the User model, represents the user who created this department
    created_by = models.ForeignKey(User, related_name='department_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the department is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this department
    updated_by = models.ForeignKey(User, related_name='department_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the VAT entry is updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Department {self.name} ({self.no}-%{self.vat.rate})"
