from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from .models import Product, ProductCategory, ProductUnit 
from .serializers import ProductCategorySerializer, ProductSerializer, ProductUnitSerializer
from drf_spectacular.utils import extend_schema,OpenApiExample,OpenApiParameter


# Create your views here.
class ProductCategoryListCreateAPIView(APIView):
    permission_classes=[IsAuthenticated]
    
    @extend_schema(
    responses=ProductCategorySerializer,
    description="Retrieve all product categories"
    )

    def get(self, request):
        categories= ProductCategory.objects.all()
        serializer=ProductCategorySerializer(categories, many=True)
        return Response (serializer.data, status=status.HTTP_200_OK)


    @extend_schema(
        request=ProductCategorySerializer,
        responses={201: ProductCategorySerializer, 400: None},
        description="Create a new product category",
        examples=[
            OpenApiExample(
                "Example Category",
                summary="Example of a category creation",
                value={"name": "Cement"}
            )
        ]
    )

    def post(self, request):
        serializer=ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ProductListCreateAPIView(APIView):
    permission_classes=[IsAuthenticated]

    
    @extend_schema(
        responses=ProductSerializer,
        description="Retrieve all products"
    )

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


    @extend_schema(
        request=ProductSerializer,
        responses={201: ProductSerializer, 400: None},
        description="Create a new product. If the category doesn't exist, it will be created automatically.",
        examples=[
            OpenApiExample(
                "Example Product",
                summary="Creating a product with category",
                value={
                    "name": "Cement 50kg",
                    "category": "Fer",
                    "description": "High quality cement"
                }
            )
        ]
    )
    def post(self, request):
        category_name= request.data.get('category')
        data=request.data.copy()
        if category_name:
            category, created = ProductCategory.objects.get_or_create(
                name=category_name.strip()
            )
            data['category']= category.id
        else :
            data['category'] = None
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUnitListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses=ProductUnitSerializer,
        parameters=[
            OpenApiParameter(
                name="product_id",
                type=int,
                description="ID of the product for which to retrieve units",
                required=True,
                examples=[
                    OpenApiExample(
                        name="Example Product ID",
                        value=1
                    )
                ]      
            )  
        ],
        description="Retrieve all units for a given product"
    )
    def get(self, request, product_id):
        units = ProductUnit.objects.filter(product_id=product_id)
        serializer = ProductUnitSerializer(units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        request=ProductUnitSerializer,
        responses={201: ProductUnitSerializer, 400: None},
        description="Create a new unit for a given product. Only one base unit is allowed per product.",
        examples=[
           OpenApiExample(
                "Example Unit",
                summary="Creating a unit",
                value={
                    "unit_name": "Tonne",
                    "factor_to_base": 1000,
                    "is_base": True 
                }
            )
        ]
    )
    def post(self, request, product_id):
        data = request.data.copy()
        data['product'] = product_id

        serializer = ProductUnitSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)