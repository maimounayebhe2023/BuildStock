from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter

from .models import Product, ProductCategory, ProductUnit, Unit
from .serializers import ProductSerializer, ProductCategorySerializer, ProductUnitSerializer, UnitSerializer


# Pagination class
class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# --- ProductCategory ---
class ProductCategoryListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ProductCategorySerializer, description="Retrieve all product categories")
    def get(self, request):
        categories = ProductCategory.objects.all()
        serializer = ProductCategorySerializer(categories, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ProductCategorySerializer,
        responses={201: ProductCategorySerializer, 400: None},
        description="Create a new product category",
        examples=[OpenApiExample("Example Category", summary="Category creation", value={"name": "Cement"})]
    )
    def post(self, request):
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Product ---
class ProductListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ProductSerializer, description="Retrieve all products")
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ProductSerializer,
        responses={201: ProductSerializer, 400: None},
        description="Create a new product with optional category creation.",
        examples=[OpenApiExample("Example Product", summary="Create product", value={
            "name": "Cement 50kg",
            "category": "Fer",
            "description": "High quality cement",
            "is_active": True
        })]
    )
    def post(self, request):
        data = request.data.copy()
        category_name = data.get('category')
        if category_name:
            category, _ = ProductCategory.objects.get_or_create(name=category_name.strip())
            data['category'] = category.id
        else:
            data['category'] = None

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- ProductUnit ---
class ProductUnitListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=ProductUnitSerializer,
        parameters=[OpenApiParameter("product_id", type=int, description="Product ID")],
        description="Retrieve all units for a given product"
    )
    def get(self, request, product_id):
        units = ProductUnit.objects.filter(product_id=product_id)
        serializer = ProductUnitSerializer(units, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=ProductUnitSerializer,
        responses={201: ProductUnitSerializer, 400: None},
        description="Create a new ProductUnit for a product"
    )
    def post(self, request, product_id):
        data = request.data.copy()
        data['product'] = product_id
        serializer = ProductUnitSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Unit ---
class UnitListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    @extend_schema(
        responses=UnitSerializer,
        description="List all units with optional search and pagination."
    )
    def get(self, request):
        search = request.query_params.get('search', '')
        queryset = Unit.objects.all().order_by('name')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(symbol__icontains=search))

        paginator = StandardPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = UnitSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        request=UnitSerializer,
        responses={201: UnitSerializer, 400: None},
        description="Create a new unit",
        examples=[OpenApiExample("Example Unit", summary="Create unit", value={"name": "Carton", "symbol": "ctn"})]
    )
    def post(self, request):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)