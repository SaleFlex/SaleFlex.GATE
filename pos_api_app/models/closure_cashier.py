from django.db import models
from django.contrib.auth.models import User


class ClosureCashier(models.Model):
    # Foreign key to Closure
    closure = models.ForeignKey('Closure', on_delete=models.CASCADE)

    # Cashier information
    cashier_no = models.IntegerField()
    cashier_name = models.CharField(max_length=50)

    # Transaction details for the cashier
    cashier_count = models.IntegerField()
    cashier_amount = models.DecimalField(max_digits=9, decimal_places=2)

    # Indicates if the closure has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for deletion (if applicable)
    delete_description = models.CharField(max_length=255, null=True, blank=True)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='closure_cashier_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='closure_cashier_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cashier {self.cashier_name} - Count: {self.cashier_count}, Amount: {self.cashier_amount}"
