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
