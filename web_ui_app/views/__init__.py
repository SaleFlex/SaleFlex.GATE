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

from .company_create import company_create
from .company_delete_approve import company_delete_approve
from .company_delete_initiate import company_delete_initiate
from .company_detail import company_detail
from .company_grant_admin import company_grant_admin
from .company_grant_owner import company_grant_owner
from .company_join import company_join
from .company_join_approve import company_join_approve
from .company_join_reject import company_join_reject
from .company_list import company_list
from .company_revoke_admin import company_revoke_admin
from .company_self_remove_owner import company_self_remove_owner
from .dashboard import dashboard
from .landing import landing
from .password_change import password_change
from .password_change_done import password_change_done
from .profile_edit import profile_edit
from .register import register

__all__ = [
    "company_create",
    "company_delete_approve",
    "company_delete_initiate",
    "company_detail",
    "company_grant_admin",
    "company_grant_owner",
    "company_join",
    "company_join_approve",
    "company_join_reject",
    "company_list",
    "company_revoke_admin",
    "company_self_remove_owner",
    "dashboard",
    "landing",
    "password_change",
    "password_change_done",
    "profile_edit",
    "register",
]
