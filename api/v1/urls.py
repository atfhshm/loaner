from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("users/", include("api.v1.users.urls")),
    path("funds/", include("api.v1.funds.urls")),
]
