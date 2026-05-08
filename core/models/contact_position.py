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

from .base import BaseModel


class ContactPosition(BaseModel):
    # Position or role within a company, e.g., "Manager", "Sales Representative"
    name = models.CharField(max_length=100, unique=True)

    # Indicates if the position has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)


    # Automatically set when the contact record is created


    # Automatically set when the contact record is updated

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ContactPosition'
