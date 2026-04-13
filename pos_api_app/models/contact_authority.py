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


class ContactAuthority(models.Model):
    # Authority or responsibility level, e.g., "Decision Maker", "Point of Contact"
    name = models.CharField(max_length=150, unique=True)

    # Indicates if the authority has been marked as deleted (soft delete)
    is_deleted = models.BooleanField(default=False, null=True)

    # Foreign key to the User model, represents the user who created this contact record
    created_by = models.ForeignKey(User, related_name='contact_authority_created', on_delete=models.SET_NULL, null=True,
                                   blank=True)

    # Automatically set when the contact record is created
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign key to the User model, represents the user who last updated this contact record
    updated_by = models.ForeignKey(User, related_name='contact_authority_updated', on_delete=models.SET_NULL, null=True,
                                   blank=True)

    # Automatically set when the contact record is updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'ContactAuthority'
