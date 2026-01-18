from django.urls import path
from .views import(ProductCategoryListCreateAPIView, ProductListCreateAPIView)

urlpatterns=[
    path('categories/', ProductCategoryListCreateAPIView.as_view),
    path('products/', ProductListCreateAPIView.as_view )
]