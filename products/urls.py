from django.urls import path
from .views import(ProductCategoryListCreateAPIView, ProductListCreateAPIView,
                ProductUnitListCreateAPIView   )

urlpatterns=[
    path('categories/', ProductCategoryListCreateAPIView.as_view()),
    path('products/', ProductListCreateAPIView.as_view() ),
    path('products/<int:product_id>/units/', ProductUnitListCreateAPIView.as_view(), name='product-units')
]