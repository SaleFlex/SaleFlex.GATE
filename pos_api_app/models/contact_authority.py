from django.db import models
from django.contrib.auth.models import User


class ContactAuthority(models.Model):
    # Authority or responsibility level, e.g., "Decision Maker", "Point of Contact"
    name = models.CharField(max_length=150, unique=True)

    # Indicates if the authority has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Foreign key to the User model, represents the user who created this contact record
    created_by = models.ForeignKey(User, related_name='contact_authority_created', on_delete=models.SET_NULL, null=True,
                                   blank=True)

    # Automatically set when the contact record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this contact record
    updated_by = models.ForeignKey(User, related_name='contact_authority_updated', on_delete=models.SET_NULL, null=True,
                                   blank=True)

    # Automatically set when the contact record is updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ContactAuthority'
