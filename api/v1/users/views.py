from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone

from drf_spectacular.utils import extend_schema, OpenApiResponse

from users.models import User


from api.utils.tokens import get_tokens_for_user
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserDataSerializer


__all__ = ["UserRegisterView", "UserLoginView", "UserDataView"]


@extend_schema(
    tags=["auth"],
    request=UserRegisterSerializer,
    responses={
        201: OpenApiResponse(UserRegisterSerializer),
        406: OpenApiResponse(description="validation error"),
    },
)
class UserRegisterView(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["users"],
        responses={
            status.HTTP_200_OK: UserDataSerializer,
            status.HTTP_406_NOT_ACCEPTABLE: OpenApiResponse(
                description="validation errors"
            ),
        },
    )
    def get(self, request):
        serializer = UserDataSerializer(instance=request.user)
        return Response(data=serializer.data)

    @extend_schema(
        tags=["users"],
        request=UserDataSerializer,
        responses={
            status.HTTP_200_OK: UserDataSerializer,
            status.HTTP_406_NOT_ACCEPTABLE: OpenApiResponse(
                description="validation errors"
            ),
        },
    )
    def patch(self, request):
        serializer = UserDataSerializer(
            data=self.request.data, instance=self.request.user, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE
            )
