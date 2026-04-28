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

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MerchantTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Deferred import: ``MerchantAPIToken`` references ``Merchant`` and related
        # models that are not registered until those submodules are imported.
        from pos_api_app.models.merchant_api_token import MerchantAPIToken

        # Expect the token in the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # Split the token from the 'Bearer' scheme
        try:
            token_key = auth_header.split(' ')[1]
        except IndexError:
            raise AuthenticationFailed('Invalid token header. No token provided.')

        # Try to find the token in the database
        try:
            token = MerchantAPIToken.objects.get(token=token_key, is_active=True)
        except MerchantAPIToken.DoesNotExist:
            raise AuthenticationFailed('Invalid or expired token.')

        # Optionally, check if the token has expired
        if token.has_expired():
            raise AuthenticationFailed('Token has expired.')

        # Return the merchant and token for DRF's request.user and request.auth
        return token.merchant, token

    def authenticate_header(self, request):
        return 'Bearer'
