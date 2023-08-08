from django.urls import path

from .views import UserRegisterView, UserLoginView, UserDataView


urlpatterns = [
    path("auth/register", UserRegisterView.as_view(), name="users-registeration"),
    path("auth/login", UserLoginView.as_view(), name="users-login"),
    path("me", UserDataView.as_view(), name="user-data"),
]
