"""Auth api views"""

from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerifyResponseSerializer,
)


class TokenPairObtainView(TokenObtainPairView):
    @extend_schema(
        tags=["auth"], responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshObtainView(TokenRefreshView):
    @extend_schema(
        tags=["auth"],
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="invalid or expired refresh token"
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VerifyTokenView(TokenVerifyView):
    @extend_schema(
        tags=["auth"],
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
