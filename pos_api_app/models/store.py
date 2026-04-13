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

from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    """
    Represents a store that belongs to a merchant.
    Each merchant can have multiple stores.
    """
    # Store name, e.g., "Downtown Branch"
    name = models.CharField(max_length=200)

    # Store number or identifier within the merchant's network
    store_number = models.CharField(max_length=100, null=True, blank=True)

    # Foreign key to the Merchant model (a store belongs to a merchant)
    merchant = models.ForeignKey('Merchant', on_delete=models.CASCADE, related_name='stores')

    # Address fields: street, block number, district (optional)
    street = models.CharField(max_length=150, null=True, blank=True)
    block_no = models.CharField(max_length=20, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    # Foreign key to the City model
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the State model, optional for countries without states
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the Country model
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='stores')

    # Postal code of the store's address
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    # Store contact phone number
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # Indicates if the store is active or closed
    is_active = models.BooleanField(default=True)

    # Foreign key to the Contact model, to link one or more contact persons associated with the store
    contacts = models.ManyToManyField('Contact', related_name='merchants')

    # Foreign key to the User model, represents the user who created this store record
    created_by = models.ForeignKey(User, related_name='store_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the store record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this store record
    updated_by = models.ForeignKey(User, related_name='store_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the store record is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Store'
        unique_together = ('merchant', 'store_number')  # Ensures no duplicate store numbers for the same merchant
