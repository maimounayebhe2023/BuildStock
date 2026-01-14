from django.urls import path
from .views import ListCreateUserApiView

urlpatterns=[
    path('users/',ListCreateUserApiView.as_view ())
]