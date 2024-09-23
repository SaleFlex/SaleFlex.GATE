from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import User


class Closure(models.Model):
    # Unique ID for Closure
    closure_unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Currency used for the transactions (ISO numeric currency code (e.g., 840 for USD))
    closure_currency_code = models.IntegerField(default=840)

    # Date and time of closure
    closure_date_time = models.DateTimeField(default=timezone.now)

    # Foreign key to Cash Register and Cashier (assuming related models exist)
    pos = models.ForeignKey('PointOfSale', on_delete=models.CASCADE)
    cashier = models.ForeignKey('Cashier', on_delete=models.CASCADE)

    # Receipt and group-number information
    receipt_number = models.IntegerField()
    group_number = models.IntegerField()

    # Start and end date/time for the day
    daily_start_date = models.DateTimeField()
    daily_end_date = models.DateTimeField()

    # Financial details
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    total_vat = models.DecimalField(max_digits=12, decimal_places=2)
    total_discount = models.DecimalField(max_digits=12, decimal_places=2)
    total_surcharge = models.DecimalField(max_digits=12, decimal_places=2)
    cumulative_total = models.DecimalField(max_digits=12, decimal_places=2)
    cumulative_vat = models.DecimalField(max_digits=12, decimal_places=2)

    # Total sales in the base currency
    total_sales_base_currency = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    # Indicates if the closure has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for deletion (if applicable)
    delete_description = models.CharField(max_length=255, null=True, blank=True)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='closure_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='closure_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Closure {self.closure_unique_id} - {self.closure_date_time}"
