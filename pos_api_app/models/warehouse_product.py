# MIT License
#
# Copyright (c) 2025-2026 Ferhat Mousavi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
