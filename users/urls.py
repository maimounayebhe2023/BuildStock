from django.urls import path
from .views import ListCreateUserApiView

urlpatterns=[
    path('',ListCreateUserApiView.as_view ())
]