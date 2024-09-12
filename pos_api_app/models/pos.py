from django.db import models
from django.contrib.auth.models import User


class PointOfSale(models.Model):
    """
    Represents a Point of Sale (POS) device that belongs to a store.
    Each store can have multiple POS devices.
    """
    # POS device identifier or serial number
    pos_serial_number = models.CharField(max_length=100, unique=True)

    # Name or description for the POS device (optional)
    name = models.CharField(max_length=100, null=True, blank=True)

    # Foreign key to the Store model (a POS belongs to a store)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='pos_devices')

    # Indicates if the POS device is active or deactivated
    is_active = models.BooleanField(default=True)

    # IP address of the POS device (optional)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    # MAC address of the POS device (optional)
    mac_address = models.CharField(max_length=50, null=True, blank=True)

    # Foreign key to the User model, represents the user who created this POS record
    created_by = models.ForeignKey(User, related_name='pos_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the POS record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this POS record
    updated_by = models.ForeignKey(User, related_name='pos_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the POS record is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PointOfSale'
        unique_together = ('store', 'pos_serial_number')  # Ensures no duplicate POS serial numbers in the same store
