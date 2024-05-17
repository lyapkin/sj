from django.urls import path, include
from rest_framework import routers


from .views import LinksApi


urlpatterns = [
    path('', LinksApi.as_view()),
]