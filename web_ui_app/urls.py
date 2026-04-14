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

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import GateAuthenticationForm

urlpatterns = [
    path("", views.landing, name="landing"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("accounts/profile/", views.profile_edit, name="profile_edit"),
    path("accounts/register/", views.register, name="register"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=GateAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "accounts/password/change/",
        views.password_change,
        name="password_change",
    ),
    path(
        "accounts/password/change/done/",
        views.password_change_done,
        name="password_change_done",
    ),
    path("companies/", views.company_list, name="company_list"),
    path("companies/create/", views.company_create, name="company_create"),
    path("companies/join/", views.company_join, name="company_join"),
    path("companies/<slug:slug>/", views.company_detail, name="company_detail"),
    path(
        "companies/<slug:slug>/join/<int:pk>/approve/",
        views.company_join_approve,
        name="company_join_approve",
    ),
    path(
        "companies/<slug:slug>/join/<int:pk>/reject/",
        views.company_join_reject,
        name="company_join_reject",
    ),
    path(
        "companies/<slug:slug>/members/<int:user_id>/grant-admin/",
        views.company_grant_admin,
        name="company_grant_admin",
    ),
    path(
        "companies/<slug:slug>/members/<int:user_id>/revoke-admin/",
        views.company_revoke_admin,
        name="company_revoke_admin",
    ),
    path(
        "companies/<slug:slug>/owners/grant/",
        views.company_grant_owner,
        name="company_grant_owner",
    ),
    path(
        "companies/<slug:slug>/owners/self-remove/",
        views.company_self_remove_owner,
        name="company_self_remove_owner",
    ),
    path(
        "companies/<slug:slug>/delete/initiate/",
        views.company_delete_initiate,
        name="company_delete_initiate",
    ),
    path(
        "companies/<slug:slug>/delete/approve/",
        views.company_delete_approve,
        name="company_delete_approve",
    ),
]
