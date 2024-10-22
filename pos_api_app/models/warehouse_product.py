from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class WarehouseProduct(models.Model):
    # Associated Warehouse Id (ForeignKey to a Warehouse model)
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='warehouse_products')

    # Product Id (ForeignKey to a Product model)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='warehouse_products')

    # Current stock quantity in the warehouse
    stock = models.IntegerField()

    # Minimum stock level
    min_stock = models.IntegerField()

    # Maximum stock level
    max_stock = models.IntegerField()

    # Last updated date of the product (stock or information change)
    last_updated = models.DateTimeField(default=timezone.now)

    # User information: who created/updated the message
    created_by = models.ForeignKey(User, related_name='warehouse_product_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='warehouse_product_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Timestamps for record creation and last update
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} in {self.warehouse.name}"
