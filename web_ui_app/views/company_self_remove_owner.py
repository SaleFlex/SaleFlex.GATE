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
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from ..company_permissions import owner_count
from .company_helpers import company_and_membership


@login_required
@require_POST
def company_self_remove_owner(request: HttpRequest, slug: str) -> HttpResponse:
    company, m = company_and_membership(request, slug)
    if not m.is_owner:
        messages.error(request, "You are not an owner of this company.")
        return redirect("company_detail", slug=slug)
    if owner_count(company) < 2:
        messages.error(
            request,
            "This company must keep at least one owner. Add another owner or delete the company instead.",
        )
        return redirect("company_detail", slug=slug)
    m.is_owner = False
    m.save(update_fields=("is_owner",))
    messages.success(request, "You removed your ownership tag. Your other roles are unchanged.")
    return redirect("company_detail", slug=slug)
