from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    # Name of the tag (e.g., VIP, Wholesale, etc.)
    name = models.CharField(max_length=100, unique=True)

    # Optional description of the tag
    description = models.TextField(blank=True, null=True)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='tag_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='tag_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
