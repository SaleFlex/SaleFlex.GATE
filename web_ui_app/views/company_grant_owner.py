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

from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from ..company_permissions import is_owner
from ..forms import GrantOwnerForm
from ..models import CompanyMembership
from .company_helpers import company_and_membership

User = get_user_model()


@login_required
@require_POST
def company_grant_owner(request: HttpRequest, slug: str) -> HttpResponse:
    company, m = company_and_membership(request, slug)
    if not is_owner(m):
        messages.error(request, "Only an owner can assign the ownership tag.")
        return redirect("company_detail", slug=slug)
    form = GrantOwnerForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Enter a valid username.")
        return redirect("company_detail", slug=slug)
    username = form.cleaned_data["username"].strip()
    user = User.objects.filter(username__iexact=username).first()
    if not user:
        messages.error(request, "No user with that username.")
        return redirect("company_detail", slug=slug)
    target, _created = CompanyMembership.objects.get_or_create(
        company=company,
        user=user,
        defaults={"is_owner": False, "is_admin": False},
    )
    if target.is_owner:
        messages.info(request, "That member already has the ownership tag.")
    else:
        target.is_owner = True
        target.is_admin = True
        target.save(update_fields=("is_owner", "is_admin"))
        messages.success(request, f"Ownership tag assigned to {user.username}.")
    return redirect("company_detail", slug=slug)
