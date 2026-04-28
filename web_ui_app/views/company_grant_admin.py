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
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from ..company_permissions import is_privileged
from ..models import CompanyMembership
from .company_helpers import company_and_membership


@login_required
@require_POST
def company_grant_admin(request: HttpRequest, slug: str, user_id: int) -> HttpResponse:
    company, m = company_and_membership(request, slug)
    if not is_privileged(m):
        messages.error(request, "Only owners or administrators can grant administrator.")
        return redirect("company_detail", slug=slug)
    target = get_object_or_404(CompanyMembership, company=company, user_id=user_id)
    if target.is_admin:
        messages.info(request, "That member is already an administrator.")
    else:
        target.is_admin = True
        target.save(update_fields=("is_admin",))
        messages.success(request, "Administrator access granted.")
    return redirect("company_detail", slug=slug)
