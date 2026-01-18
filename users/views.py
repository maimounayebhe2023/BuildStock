from rest_framework.views import APIView
from .userSerializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import User
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample


@extend_schema_view(
    get=extend_schema(
        summary="List Users",
        description="Returns the list of all users registered in the system.",
        responses=UserSerializer(many=True),
    ),
    post=extend_schema(
        summary="Create a User",
        description=(
            "Creates a new user in the system.\n\n"
            "Password rules:\n"
            "- Minimum 8 characters\n"
            "- At least one uppercase letter\n"
            "- At least one lowercase letter\n"
            "- At least one number\n"
            "- At least one special character"
        ),
        request=UserSerializer,
        examples=[
            OpenApiExample(
                name="User creation example",
                summary="Example of a valid request body",
                description="All required fields for creating a user",
                value={
                    "username": "john",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "user@example.com",
                    "role": "storekeeper",
                    "phone": "1234567890",
                    "password": "P@ssword123!"
                },
                request_only=True
            )
        ],
        responses={
            201: UserSerializer,
            400: dict
        },
    )
)
class ListCreateUserApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
