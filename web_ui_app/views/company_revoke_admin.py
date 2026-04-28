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

from ..company_permissions import is_admin, is_owner
from ..models import CompanyMembership
from .company_helpers import company_and_membership


@login_required
@require_POST
def company_revoke_admin(request: HttpRequest, slug: str, user_id: int) -> HttpResponse:
    company, m = company_and_membership(request, slug)
    target = get_object_or_404(CompanyMembership, company=company, user_id=user_id)
    if target.is_owner:
        messages.error(request, "Cannot change administrator flag on an owner from here.")
        return redirect("company_detail", slug=slug)
    if not target.is_admin:
        messages.info(request, "That user is not an administrator.")
        return redirect("company_detail", slug=slug)
    if is_owner(m):
        pass
    elif is_admin(m) and m.user_id != target.user_id and is_admin(target):
        pass
    else:
        messages.error(
            request,
            "Only another administrator can revoke administrator from a peer, or an owner may revoke it.",
        )
        return redirect("company_detail", slug=slug)
    if is_admin(m) and not is_owner(m) and m.user_id == target.user_id:
        messages.error(request, "Use another administrator or an owner to revoke your own administrator access.")
        return redirect("company_detail", slug=slug)
    target.is_admin = False
    target.save(update_fields=("is_admin",))
    messages.success(request, "Administrator access removed.")
    return redirect("company_detail", slug=slug)
