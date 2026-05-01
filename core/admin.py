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
    CashierStoreAssignment,
    Company,
    CompanyDeletionApproval,
    CompanyDeletionRequest,
    CompanyJoinRequest,
    CompanyMembership,
    GateUser,
)


# ---------------------------------------------------------------------------
# GateUser
# ---------------------------------------------------------------------------

class CashierStoreAssignmentInline(admin.TabularInline):
    model = CashierStoreAssignment
    extra = 0
    fields = ("store", "can_access_all_pos", "is_active")


@admin.register(GateUser)
class GateUserAdmin(admin.ModelAdmin):
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "User"
    get_username.admin_order_field = "user__username"

    list_display = (
        "get_username",
        "cashier_number",
        "is_cashier",
        "is_store_manager",
        "is_office_user",
        "is_company_admin",
        "is_company_owner",
        "is_active",
    )
    list_display_links = ("get_username",)
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    list_filter = (
        "is_cashier",
        "is_store_manager",
        "is_office_user",
        "is_company_admin",
        "is_company_owner",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("user",)}),
        ("Portal", {"fields": ("avatar",)}),
        (
            "POS / Operations",
            {"fields": ("cashier_number", "pin_code"), "classes": ("collapse",)},
        ),
        (
            "Roles",
            {
                "fields": (
                    "is_cashier",
                    "is_store_manager",
                    "is_office_user",
                    "is_company_admin",
                    "is_company_owner",
                )
            },
        ),
        ("Status", {"fields": ("is_active", "is_deleted")}),
        (
            "Audit",
            {
                "fields": ("created_by", "updated_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")
    inlines = (CashierStoreAssignmentInline,)


@admin.register(CashierStoreAssignment)
class CashierStoreAssignmentAdmin(admin.ModelAdmin):
    def get_gate_user(self, obj):
        return obj.gate_user.user.username
    get_gate_user.short_description = "Gate User"
    get_gate_user.admin_order_field = "gate_user__user__username"

    def get_store(self, obj):
        return str(obj.store)
    get_store.short_description = "Store"
    get_store.admin_order_field = "store__name"

    list_display = ("get_gate_user", "get_store", "can_access_all_pos", "is_active", "created_at")
    list_display_links = ("get_gate_user",)
    list_filter = ("can_access_all_pos", "is_active")
    search_fields = ("gate_user__user__username", "store__name")
    filter_horizontal = ("pos_devices",)


# ---------------------------------------------------------------------------
# Company
# ---------------------------------------------------------------------------

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    list_display_links = ("name",)
    search_fields = ("name", "slug", "companies_house_number", "vat_number")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (None, {"fields": ("name", "slug")}),
        (
            "Registration",
            {
                "fields": ("companies_house_number", "vat_number", "registered_office"),
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
    def get_company(self, obj):
        return obj.company.name
    get_company.short_description = "Company"
    get_company.admin_order_field = "company__name"

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = "User"
    get_user.admin_order_field = "user__username"

    list_display = ("get_company", "get_user", "is_owner", "is_admin", "joined_at")
    list_display_links = ("get_company",)
    list_filter = ("is_owner", "is_admin")
    search_fields = ("company__name", "company__slug", "user__username")


@admin.register(CompanyJoinRequest)
class CompanyJoinRequestAdmin(admin.ModelAdmin):
    def get_company(self, obj):
        return obj.company.name
    get_company.short_description = "Company"
    get_company.admin_order_field = "company__name"

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = "User"
    get_user.admin_order_field = "user__username"

    list_display = ("get_company", "get_user", "status", "created_at")
    list_display_links = ("get_company",)
    list_filter = ("status",)
    search_fields = ("company__slug", "user__username")


class CompanyDeletionApprovalInline(admin.TabularInline):
    model = CompanyDeletionApproval
    extra = 0


@admin.register(CompanyDeletionRequest)
class CompanyDeletionRequestAdmin(admin.ModelAdmin):
    def get_company(self, obj):
        return obj.company.name
    get_company.short_description = "Company"
    get_company.admin_order_field = "company__name"

    def get_requested_by(self, obj):
        return obj.requested_by.username
    get_requested_by.short_description = "Requested By"
    get_requested_by.admin_order_field = "requested_by__username"

    list_display = ("get_company", "get_requested_by", "created_at", "completed_at")
    list_display_links = ("get_company",)
    inlines = (CompanyDeletionApprovalInline,)
