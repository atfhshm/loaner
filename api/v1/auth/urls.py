from django.urls import path

from .views import TokenPairObtainView, TokenRefreshObtainView, VerifyTokenView

urlpatterns = [
    path("auth/tokens", TokenPairObtainView.as_view(), name="user-tokens"),
    path(
        "auth/tokens/refresh", TokenRefreshObtainView.as_view(), name="generate-token"
    ),
    path("auth/tokens/verify", VerifyTokenView.as_view(), name="verify-token"),
]
