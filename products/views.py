from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProductCategory, Product
from .serializers import ProductCategorySerializer, ProductSerializer

# Create your views here.
class ProductCategoryListCreateAPIView(APIView):

    def get(self, request):
        categories= ProductCategory.objects.all()
        serializer=ProductCategorySerializer(categories, many=True)
        return Response (serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer=ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class ProductListCreateAPIView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
