from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_spectacular.utils import extend_schema, OpenApiResponse


from .serializers import UserRegisterSerializer, UserDataSerializer


__all__ = ["UserRegisterView", "UserDataView"]


@extend_schema(
    tags=["user-register"],
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
