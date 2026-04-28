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

from ..forms import GateUserAccountForm, GateUserAvatarForm
from ..models import UserProfile


@login_required
def profile_edit(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = GateUserAccountForm(request.POST, instance=request.user)
        avatar_form = GateUserAvatarForm(
            request.POST,
            request.FILES,
            instance=profile,
        )
        if user_form.is_valid() and avatar_form.is_valid():
            user_form.save()
            avatar_form.save()
            messages.success(request, "Your profile was updated.")
            return redirect("profile_edit")
    else:
        user_form = GateUserAccountForm(instance=request.user)
        avatar_form = GateUserAvatarForm(instance=profile)
    return render(
        request,
        "web_ui_app/profile_edit.html",
        {"user_form": user_form, "avatar_form": avatar_form},
    )
