from django.urls import path

from .views import TokenPairObtainView, TokenRefreshObtainView, VerifyTokenView

urlpatterns = [
    path("tokens", TokenPairObtainView.as_view(), name="user-tokens"),
    path("tokens/refresh", TokenRefreshObtainView.as_view(), name="generate-token"),
    path("tokens/verify", VerifyTokenView.as_view(), name="verify-token"),
]
