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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..forms import CashierAccountForm, CashierAvatarForm


@login_required
def profile_edit(request):
    if request.method == "POST":
        account_form = CashierAccountForm(request.POST, instance=request.user)
        avatar_form = CashierAvatarForm(
            request.POST,
            request.FILES,
            instance=request.user,
        )
        if account_form.is_valid() and avatar_form.is_valid():
            account_form.save()
            avatar_form.save()
            messages.success(request, "Your profile was updated.")
            return redirect("profile_edit")
    else:
        account_form = CashierAccountForm(instance=request.user)
        avatar_form = CashierAvatarForm(instance=request.user)
    return render(
        request,
        "web_ui_app/profile_edit.html",
        {"user_form": account_form, "avatar_form": avatar_form},
    )
