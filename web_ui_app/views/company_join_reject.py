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
from django.utils import timezone
from django.views.decorators.http import require_POST

from ..company_permissions import is_privileged
from ..models import CompanyJoinRequest
from .company_helpers import company_and_membership


@login_required
@require_POST
def company_join_reject(request: HttpRequest, slug: str, pk: int) -> HttpResponse:
    company, m = company_and_membership(request, slug)
    if not is_privileged(m):
        messages.error(request, "You cannot reject join requests for this company.")
        return redirect("company_detail", slug=slug)
    jr = get_object_or_404(
        CompanyJoinRequest,
        pk=pk,
        company=company,
        status=CompanyJoinRequest.Status.PENDING,
    )
    jr.status = CompanyJoinRequest.Status.REJECTED
    jr.resolved_by = request.user
    jr.resolved_at = timezone.now()
    jr.save(update_fields=("status", "resolved_by", "resolved_at"))
    messages.info(request, "Join request was rejected.")
    return redirect("company_detail", slug=slug)
