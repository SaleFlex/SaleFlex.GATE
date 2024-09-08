from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    # First name of the contact person
    first_name = models.CharField(max_length=100)

    # Last name of the contact person
    last_name = models.CharField(max_length=100)

    # Email address of the contact person
    email = models.EmailField(max_length=150, unique=True)

    # Mobile phone number of the contact person
    mobile_phone = models.CharField(max_length=20)

    # Optional landline phone number
    landline_phone = models.CharField(max_length=20, null=True, blank=True)

    # Optional fax number
    fax_number = models.CharField(max_length=20, null=True, blank=True)

    # Foreign key to the Position model to indicate the person's role within the company
    position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the Authority model to indicate the person's responsibility or authority level
    authority = models.ForeignKey('Authority', on_delete=models.SET_NULL, null=True, blank=True)

    # Address fields: Street, BlockNo, District (optional)
    street = models.CharField(max_length=150, null=True, blank=True)
    block_no = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    # Foreign key to the City model, nullable to handle cases where only a state or country is provided
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the State model, nullable in case the country doesn’t have states (e.g., Turkey)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the Country model, mandatory as each contact belongs to a country
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='contacts')

    # Postal code of the contact's address
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    # Company name this contact is associated with
    company_name = models.CharField(max_length=150, null=True, blank=True)

    # Indicates if the contact has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for why the contact was deleted
    delete_description = models.TextField(null=True, blank=True)

    # Foreign key to the User model, represents the user who created this contact record
    created_by = models.ForeignKey(User, related_name='contact_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the contact record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this contact record
    updated_by = models.ForeignKey(User, related_name='contact_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the contact record is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Contact'
