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

class City(models.Model):
    # Name of the city, e.g., "Istanbul", "Los Angeles"
    name = models.CharField(max_length=150)

    # Foreign key to the Country model, mandatory since every city belongs to a country
    country = models.ForeignKey('Country', on_delete=models.CASCADE, related_name='cities')

    # Foreign key to the State model, optional since not all countries have states
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True, blank=True, related_name='cities')

    # Postal code for the city
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    # Time zone(s) for the city, which may differ within states or regions
    time_zones = models.JSONField(null=True, blank=True)

    # Population of the city
    population = models.IntegerField(null=True, blank=True)

    # Indicates if the city has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Description or reason for why the city was deleted
    delete_description = models.TextField(null=True, blank=True)

    # Foreign key to the User model, represents the user who created this city record
    created_by = models.ForeignKey(User, related_name='city_created', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the city record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this city record
    updated_by = models.ForeignKey(User, related_name='city_updated', on_delete=models.SET_NULL, null=True, blank=True)

    # Automatically set when the city record is updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'City'
        unique_together = ('name', 'country', 'state')  # Prevent duplicate city names in the same state or country
