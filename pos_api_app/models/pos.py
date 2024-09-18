from django.db import models
from django.contrib.auth.models import User


class PointOfSale(models.Model):
    """
    Represents a Point of Sale (POS) device that belongs to a store.
    Each store can have multiple POS devices with various hardware and configuration details.
    """

    # POS device identifier or serial number
    pos_serial_number = models.CharField(max_length=100, unique=True)

    # Name or description for the POS device (optional)
    name = models.CharField(max_length=100, null=True, blank=True)

    # Brand and model details
    brand = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)

    # Operating system version running on the POS
    operating_system_version = models.CharField(max_length=100, null=True, blank=True)

    # Owner information
    owner_national_id_number = models.CharField(max_length=50, null=True, blank=True)
    owner_tax_id_number = models.CharField(max_length=50, null=True, blank=True)
    owner_mersis_id_number = models.CharField(max_length=50, null=True, blank=True)
    owner_commercial_record_no = models.CharField(max_length=50, null=True, blank=True)
    owner_web_address = models.URLField(null=True, blank=True)
    owner_registration_number = models.CharField(max_length=50, null=True, blank=True)

    # MAC address of the POS device (optional)
    mac_address = models.CharField(max_length=50, null=True, blank=True)

    # Cashier and customer screen configurations
    cashier_screen_type = models.CharField(max_length=50, null=True, blank=True)
    customer_screen_type = models.CharField(max_length=50, null=True, blank=True)

    # Customer display configurations
    customer_display_type = models.CharField(max_length=50, null=True, blank=True)
    customer_display_port = models.CharField(max_length=50, null=True, blank=True)

    # Printer configurations
    receipt_printer_type = models.CharField(max_length=50, null=True, blank=True)
    receipt_printer_port_name = models.CharField(max_length=50, null=True, blank=True)
    invoice_printer_type = models.CharField(max_length=50, null=True, blank=True)
    invoice_printer_port_name = models.CharField(max_length=50, null=True, blank=True)

    # Scale configurations
    scale_type = models.CharField(max_length=50, null=True, blank=True)
    scale_port_name = models.CharField(max_length=50, null=True, blank=True)

    # Barcode reader configuration
    barcode_reader_port = models.CharField(max_length=50, null=True, blank=True)

    # Server connection details
    server_ip_1 = models.GenericIPAddressField(null=True, blank=True)
    server_port_1 = models.CharField(max_length=50, null=True, blank=True)
    server_ip_2 = models.GenericIPAddressField(null=True, blank=True)
    server_port_2 = models.CharField(max_length=50, null=True, blank=True)

    # Indicates if the POS device is forced to work online
    force_to_work_online = models.BooleanField(default=False)

    # Foreign key to the Store model (a POS belongs to a store)
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='pos_devices')

    # Foreign key to the Country model for default country (optional)
    default_country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True)

    # Indicates if the POS device is active or deactivated
    is_active = models.BooleanField(default=True)

    # Indicates if the pos has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

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
