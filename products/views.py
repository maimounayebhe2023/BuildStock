from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from .pagination import GlobalPagination
from .models import Product, ProductCategory, Unit
from .serializers import ProductSerializer, ProductCategorySerializer, UnitSerializer


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
    pagination_class = GlobalPagination

    @extend_schema(responses=ProductSerializer, description="List all products with optional search and pagination")
    def get(self, request):
        search_query = request.GET.get('search', '')
        products = Product.objects.all().order_by('name')

        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(request=ProductSerializer, responses={201: ProductSerializer, 400: None}, description="Create a new product")
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=ProductSerializer, responses={200: ProductSerializer, 400: None}, description="Update a product fully")
    def put(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=ProductSerializer, responses={200: ProductSerializer, 400: None}, description="Update a product partially")
    def patch(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- Unit ---
class UnitListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = GlobalPagination

    @extend_schema(
        responses=UnitSerializer,
        description="List all units with optional search and pagination."
    )
    def get(self, request):
        search_query = request.query_params.get('search', '')
        queryset = Unit.objects.all().order_by('name')
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(symbol__icontains=search_query))

        paginator = self.pagination_class()
        paginated_units = paginator.paginate_queryset(queryset, request)
        serializer = UnitSerializer(paginated_units, many=True)
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