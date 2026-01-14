from rest_framework.views import APIView
from .userSerializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import User
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class ListCreateUserApiView(APIView) :
    permission_classes = [IsAuthenticated]
    def get(self, *args, **kwargs):
        users=User.objects.all()
        serializer=UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request, *args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({
                "id": user.id,
                "username": user.username,
                "role": user.role
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)