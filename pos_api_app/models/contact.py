# SaleFlex.GATE - Point of Sale Application Gateway
# Copyright (C) 2025-2026 Mousavi.Tech
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
    position = models.ForeignKey('ContactPosition', on_delete=models.SET_NULL, null=True, blank=True)

    # Foreign key to the Authority model to indicate the person's responsibility or authority level
    authority = models.ForeignKey('ContactAuthority', on_delete=models.SET_NULL, null=True, blank=True)

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
