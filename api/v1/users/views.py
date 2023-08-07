from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.utils import timezone

from drf_spectacular.utils import extend_schema, OpenApiResponse

from users.models import User


from api.utils.tokens import get_tokens_for_user
from .serializers import UserRegisterSerializer, UserLoginSerializer


__all__ = ["UserRegisterView", "UserLoginView"]


@extend_schema(
    tags=["auth"],
    request=UserRegisterSerializer,
    responses={
        201: OpenApiResponse(UserRegisterSerializer),
        406: OpenApiResponse(description="validation error"),
    },
)
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE
            )


class UserLoginView(APIView):
    @extend_schema(
        tags=["auth"],
        request=UserLoginSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(UserLoginSerializer),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(description="Unauthorized"),
        },
    )
    def post(self, request: Request):
        username = request.data.get("username")
        password = request.data.get("password")
        user: User = User.objects.filter(username=username).first()
        tokens = get_tokens_for_user(user=user)

        if user and user.check_password(password):
            user.last_login = timezone.now()
            user.save()

            serializer = UserLoginSerializer(instance=user)
            payload = serializer.data | tokens

            return Response(data=payload, status=status.HTTP_202_ACCEPTED)

        else:
            return Response(
                data={"msg": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserDataView(APIView):
    def get(self, request):
        ...

    def update(self, request):
        ...


class UserChangePasswordView(APIView):
    def post(self, request):
        ...
