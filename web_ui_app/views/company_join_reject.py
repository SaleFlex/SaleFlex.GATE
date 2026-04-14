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
