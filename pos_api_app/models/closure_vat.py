from django.db import models
from django.contrib.auth.models import User


class ClosureVat(models.Model):
    # Foreign key to Closure
    closure = models.ForeignKey('Closure', on_delete=models.CASCADE)

    vat = models.ForeignKey('PosVat', on_delete=models.CASCADE)

    # VAT details (assuming this structure based on context)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2)
    vat_sales_count = models.IntegerField()
    vat_sales_amount = models.DecimalField(max_digits=12, decimal_places=2)

    # Soft delete flag to indicate if this record has been marked as deleted
    is_deleted = models.BooleanField(default=False, null=True)

    # Reason or description for deletion (if applicable)
    delete_description = models.CharField(max_length=255, null=True, blank=True)

    # Tracks the user who created the record
    created_by = models.ForeignKey(User, related_name='closure_vat_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Tracks the user who last updated the record
    updated_by = models.ForeignKey(User, related_name='closure_vat_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically stores the timestamp when the record was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically stores the timestamp when the record was last updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"VAT {self.vat_rate}% - Sales Count: {self.vat_sales_count}, Sales Amount: {self.vat_sales_amount}"
