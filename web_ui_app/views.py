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

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    GatePasswordChangeForm,
    GateUserAccountForm,
    GateUserAvatarForm,
    GateUserCreationForm,
)
from .models import UserProfile


def landing(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "web_ui_app/landing.html")


@login_required
def dashboard(request):
    return render(request, "web_ui_app/dashboard.html")


@login_required
def password_change(request):
    if request.method == "POST":
        form = GatePasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("password_change_done")
    else:
        form = GatePasswordChangeForm(user=request.user)
    return render(
        request,
        "web_ui_app/password_change.html",
        {"form": form},
    )


@login_required
def password_change_done(request):
    return render(request, "web_ui_app/password_change_done.html")


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


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = GateUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = GateUserCreationForm()
    return render(request, "registration/register.html", {"form": form})
