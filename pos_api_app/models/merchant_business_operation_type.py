from django.contrib.auth.models import User
from django.db import models


class MerchantBusinessOperationType(models.Model):
    # Name of the business operation type, e.g., "Wholesaler", "Retailer"
    name = models.CharField(max_length=100, unique=True)

    # Optional description of the business operation type
    description = models.TextField(null=True, blank=True)

    # Indicates if the business operation type has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='label_value_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='label_value_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'MerchantBusinessOperationType'
        verbose_name = 'Merchant Business Operation Type'
        verbose_name_plural = 'Merchant Business Operation Types'
