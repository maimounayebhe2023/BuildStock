from django.urls import path
from .views import (
    ProductCategoryListCreateAPIView,
    ProductListCreateAPIView,
    ProductUnitListCreateAPIView,
    UnitListCreateAPIView
)

urlpatterns=[
    path('categories/', ProductCategoryListCreateAPIView.as_view()),
    path('products/', ProductListCreateAPIView.as_view() ),
    path('products/<int:product_id>/units/', ProductUnitListCreateAPIView.as_view(), name='product-units')
]
urlpatterns = [
path('categories/', ProductCategoryListCreateAPIView.as_view(), name='categories-list-create'),
path('products/', ProductListCreateAPIView.as_view(), name='products-list-create'),
path('products/<int:product_id>/units/', ProductUnitListCreateAPIView.as_view(), name='product-units-list-create'),
path('units/', UnitListCreateAPIView.as_view(), name='units-list-create'),
]