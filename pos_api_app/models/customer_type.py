from django.db import models
from django.contrib.auth.models import User


class CustomerType(models.Model):
    # Customer type name (e.g., Individual, Corporate, VIP)
    name = models.CharField(max_length=50, unique=True)

    # Description for the customer type (optional)
    description = models.TextField(blank=True, null=True)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='label_value_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='label_value_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
