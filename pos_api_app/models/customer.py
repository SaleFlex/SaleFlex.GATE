from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    # Customer code, optional field
    code = models.CharField(max_length=255, blank=True, null=True)

    # Customer name
    name = models.CharField(max_length=255)

    # Customer last name
    last_name = models.CharField(max_length=255)

    # ForeignKey to CustomerType to store customer type dynamically
    customer_type = models.ForeignKey('CustomerType', on_delete=models.SET_NULL, null=True, blank=True)

    # Description of the customer, optional field
    description = models.TextField(blank=True, null=True)

    # Address lines for the customer (address split into three fields)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    address_line3 = models.CharField(max_length=255, blank=True, null=True)

    # Zip code of the customer’s address, optional field
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    # Foreign key relationships for district, city, and country. Allows for setting geographical hierarchy.
    district = models.ForeignKey('District', on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True)

    # Bonus points for the customer (an integer field representing loyalty or promotional points)
    bonus = models.IntegerField(default=0)

    # Preferred currency for transactions, stored as an ISO numeric currency code (e.g., 840 for USD)
    preferred_currency_code = models.IntegerField()

    # National identity number, optional field
    national_identity_number = models.CharField(max_length=50, blank=True, null=True)

    # Tax information: tax office and tax number for the customer, optional fields
    tax_office = models.CharField(max_length=255, blank=True, null=True)
    tax_number = models.CharField(max_length=50, blank=True, null=True)

    # Email and phone number for the customer, optional fields
    email_address = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Alternate contact details for corporate customers (optional fields)
    alternate_contact_name = models.CharField(max_length=255, blank=True, null=True)
    alternate_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    alternate_contact_email = models.EmailField(blank=True, null=True)

    # Financial details for managing credit limits and outstanding balances
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    outstanding_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Internal rating system to prioritize services (1-5 star rating)
    rating = models.IntegerField(default=5, blank=True, null=True)

    # For customers who are VAT or tax-exempt (e.g., businesses, non-profits)
    is_tax_exempt = models.BooleanField(default=False)
    tax_exempt_certificate = models.CharField(max_length=100, blank=True, null=True)

    # Tags for customer segmentation or special designations (Many-to-Many relationship with Tag model)
    tags = models.ManyToManyField('Tag', blank=True)

    # Foreign key to POS, optional, allows the form to be related to specific POS devices
    pos = models.ForeignKey('PointOfSale', on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')

    # Foreign key to Store, optional, allows the form to be sent to all POS devices in a store
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')

    # Foreign key to Merchant, optional, allows the form to be sent to all stores and POS devices under the merchant
    merchant = models.ForeignKey('Merchant', on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')

    # Optional date of birth for personalization and special offers (e.g., birthday discounts)
    date_of_birth = models.DateField(blank=True, null=True)

    # Track the date of the customer's last purchase.
    last_purchase_date = models.DateTimeField(blank=True, null=True)

    # Indicates if the pos form has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for deletion (if applicable)
    delete_description = models.CharField(max_length=255, null=True, blank=True)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='customer_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='customer_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['merchant', 'name', 'last_name'], name='unique_customer_name')
        ]

    def __str__(self):
        return f"{self.name} {self.last_name}"
