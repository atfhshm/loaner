from django.urls import path

from .views import UserRegisterView, UserDataView


urlpatterns = [
    path("register", UserRegisterView.as_view(), name="users-registeration"),
    path("me", UserDataView.as_view(), name="user-data"),
]
