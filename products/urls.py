from django.urls import path
from .views import (
    ProductCategoryListCreateAPIView,
    ProductListCreateAPIView,
    ProductDetailAPIView,
    UnitListCreateAPIView,
)

urlpatterns = [
    path('categories/', ProductCategoryListCreateAPIView.as_view(), name='categories-list-create'),
    path('products/', ProductListCreateAPIView.as_view(), name='products-list-create'),
    path('products/<int:product_id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('units/', UnitListCreateAPIView.as_view(), name='units-list-create'),
]