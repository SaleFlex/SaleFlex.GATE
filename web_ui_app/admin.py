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

from django.contrib import admin

from .models import (
    Company,
    CompanyDeletionApproval,
    CompanyDeletionRequest,
    CompanyJoinRequest,
    CompanyMembership,
    UserProfile,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "avatar")
    search_fields = ("user__username", "user__email")


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = (
        "name",
        "slug",
        "companies_house_number",
        "vat_number",
    )
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (None, {"fields": ("name", "slug")}),
        (
            "Registration",
            {
                "fields": (
                    "companies_house_number",
                    "vat_number",
                    "registered_office",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):
    list_display = ("company", "user", "is_owner", "is_admin", "joined_at")
    list_filter = ("is_owner", "is_admin")
    search_fields = ("company__name", "company__slug", "user__username")


@admin.register(CompanyJoinRequest)
class CompanyJoinRequestAdmin(admin.ModelAdmin):
    list_display = ("company", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("company__slug", "user__username")


class CompanyDeletionApprovalInline(admin.TabularInline):
    model = CompanyDeletionApproval
    extra = 0


@admin.register(CompanyDeletionRequest)
class CompanyDeletionRequestAdmin(admin.ModelAdmin):
    list_display = ("company", "requested_by", "created_at", "completed_at")
    inlines = (CompanyDeletionApprovalInline,)
