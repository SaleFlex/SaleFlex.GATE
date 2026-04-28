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
