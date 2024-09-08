from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from pos_api_app.models.merchant_api_token import MerchantAPIToken


class MerchantTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
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
