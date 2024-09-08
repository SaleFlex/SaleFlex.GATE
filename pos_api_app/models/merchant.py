from django.db import models
from django.contrib.auth.models import User


class Merchant(models.Model):
    # Merchant name, e.g., "ABC Corp"
    name = models.CharField(max_length=200)

    # Optional abbreviation or short name of the merchant
    short_name = models.CharField(max_length=100, null=True, blank=True)

    # Merchant registration number (optional field)
    registration_number = models.CharField(max_length=100, null=True, blank=True)

    # Tax identification number
    tax_id_number = models.CharField(max_length=100, null=True, blank=True)

    # MERSIS number or other relevant business registration identifier (optional)
    business_id_number = models.CharField(max_length=100, null=True, blank=True)

    # Web address of the merchant
    website = models.URLField(max_length=200, null=True, blank=True)

    # Address fields: street, block number, district (optional)
    street = models.CharField(max_length=150, null=True, blank=True)
    block_no = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    # Foreign key to the City model
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the State model, optional for countries without states
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the Country model
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='merchants')

    # Postal code of the merchant's address
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    # Foreign key to the MerchantBusinessOperationType model to define how the merchant operates (e.g., Wholesaler, Retailer)
    operation_type = models.ForeignKey('MerchantBusinessOperationType', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the MerchantCompanyType model to define the type of company
    company_type = models.ForeignKey('MerchantCompanyType', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the MerchantActivitySector model to define the business sector the merchant operates in
    activity_sector = models.ForeignKey('MerchantActivitySector', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the Contact model, to link one or more contact persons associated with the merchant
    contacts = models.ManyToManyField('Contact', related_name='merchants')

    # Indicates if the merchant has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for why the merchant was deleted
    delete_description = models.TextField(null=True, blank=True)

    # Foreign key to the User model, represents the user who created this merchant record
    created_by = models.ForeignKey(User, related_name='merchant_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the merchant record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this merchant record
    updated_by = models.ForeignKey(User, related_name='merchant_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the merchant record is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Merchant'
        unique_together = ('name', 'registration_number')  # Ensures no duplicate merchant names with the same registration number
