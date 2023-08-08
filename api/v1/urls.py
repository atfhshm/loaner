from django.urls import path, include

urlpatterns = [
    path("users/", include("api.v1.users.urls")),
    path("funds/", include("api.v1.fund.urls")),
]
