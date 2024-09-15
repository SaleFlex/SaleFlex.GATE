from django.db import models
from django.contrib.auth.models import User


class LabelValue(models.Model):
    """
    Represents key-value pairs that display messages on POS device screens.
    Each message is localized using the CultureInfo field.
    """

    # Key and Value for the message to display on POS screens
    key = models.CharField(max_length=255)
    value = models.TextField()

    # ISO format culture info, e.g., "en-GB"
    culture_info = models.CharField(max_length=10)

    # Foreign key to POS, optional, allows sending the message to specific POS devices
    pos = models.ForeignKey('PointOfSale', on_delete=models.SET_NULL, null=True, blank=True, related_name='label_values')

    # Foreign key to Store, optional, allows sending the message to all POS devices in the store
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='label_values')

    # Foreign key to Merchant, optional, allows sending the message to all stores and POS devices under the merchant
    merchant = models.ForeignKey('Merchant', on_delete=models.SET_NULL, null=True, blank=True, related_name='label_values')

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='label_value_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='label_value_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'LabelValue'
        unique_together = ('key', 'culture_info', 'pos', 'store', 'merchant')  # Ensures no duplicate keys for the same POS/store/merchant with the same culture
