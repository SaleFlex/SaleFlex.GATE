from django.db import models
from django.contrib.auth.models import User


class PosForm(models.Model):
    """
    Represents a configuration for forms that are displayed on POS devices.
    This model stores various settings related to the appearance and functionality of each form.
    """

    # Form number (must be unique)
    form_no = models.IntegerField()

    # Name of the form
    name = models.CharField(max_length=255)

    # Function or purpose of the form
    function = models.CharField(max_length=255)

    # Indicates whether login is required to access the form
    need_login = models.BooleanField(default=False)

    # Indicates whether authorization is required to access the form
    need_auth = models.BooleanField(default=False)

    # Dimensions of the form
    width = models.IntegerField(default=1024)
    height = models.IntegerField(default=768)

    # Border style for the form (e.g., 'SINGLE', 'NONE', etc.)
    form_border_style = models.CharField(max_length=50, default='SINGLE')

    # Position of the form when it starts (e.g., 'CENTERSCREEN')
    start_position = models.CharField(max_length=50, default='CENTERSCREEN')

    # Caption for the form window
    caption = models.CharField(max_length=255, null=True, blank=True)

    # Icon for the form (optional)
    icon = models.CharField(max_length=255, null=True, blank=True)

    # Background image for the form (optional)
    image = models.CharField(max_length=255, null=True, blank=True)

    # Background color for the form
    back_color = models.CharField(max_length=50, default='AliceBlue')

    # Indicates whether to show a status bar
    show_status_bar = models.BooleanField(default=True)

    # Indicates whether the form should appear in the taskbar
    show_in_taskbar = models.BooleanField(default=True)

    # Indicates whether a virtual keyboard should be used
    use_virtual_keyboard = models.BooleanField(default=True)

    # Foreign key to POS, optional, allows the form to be related to specific POS devices
    pos = models.ForeignKey('PointOfSale', on_delete=models.SET_NULL, null=True, blank=True, related_name='forms')

    # Foreign key to Store, optional, allows the form to be sent to all POS devices in a store
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='forms')

    # Foreign key to Merchant, optional, allows the form to be sent to all stores and POS devices under the merchant
    merchant = models.ForeignKey('Merchant', on_delete=models.SET_NULL, null=True, blank=True, related_name='forms')

    # Indicates if the pos form has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='pos_form_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='pos_form_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PosForm'
        unique_together = ('form_no', 'pos', 'store', 'merchant')  # Ensures no duplicate forms for the same POS/store/merchant
