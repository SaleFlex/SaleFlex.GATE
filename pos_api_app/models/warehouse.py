from django.contrib.auth.models import User
from django.db import models


class Warehouse(models.Model):
    # Warehouse Id (Automatically generated in Django)
    id = models.AutoField(primary_key=True)

    # Warehouse Name
    name = models.CharField(max_length=255)

    # Warehouse Location
    location = models.CharField(max_length=255)

    # Foreign key to the Merchant model (a store belongs to a merchant)
    merchant = models.ForeignKey('Merchant', on_delete=models.SET_NULL, related_name='merchant_warehouses', null=True, blank=True)

    # Foreign key to the Store model (a Warehouse belongs to a store)
    store = models.ForeignKey('Store', on_delete=models.SET_NULL, related_name='store_warehouses', null=True, blank=True)

    # Warehouse Type (Main Warehouse, Branch Warehouse, etc.)
    WAREHOUSE_TYPES = [
        ('main', 'Main Warehouse'),
        ('branch', 'Branch Warehouse')
    ]
    warehouse_type = models.CharField(max_length=50, choices=WAREHOUSE_TYPES)

    # List of products in the warehouse (related to WarehouseProduct model)
    products = models.ManyToManyField('WarehouseProduct', related_name='warehouse_products')

    # Address fields: street, block number, district (optional)
    street = models.CharField(max_length=150, null=True, blank=True)
    block_no = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    # Foreign key to the City model
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the State model, optional for countries without states
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the Country model
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, related_name='warehouse_counties', null=True, blank=True)

    # Postal code of the store's address
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    # Warehouse contact phone number
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # Region or zone of the warehouse
    region = models.CharField(max_length=255, null=True, blank=True, help_text="Region or zone where the warehouse is located.")

    # Indicates if the store is active or closed
    is_active = models.BooleanField(default=True)

    # Foreign key to the Contact model, to link one or more contact persons associated with the warehouse
    contacts = models.ManyToManyField('Contact', related_name='warehouse_contacts')

    # Indicates if the warehouse has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='warehouse_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='warehouse_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
