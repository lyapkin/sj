from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import get_categories, get_products
from .serializers import ProductListSerializer, CategorySerializer


class CategoriesApi(APIView):

    def get(self, request):
        categories = get_categories()
        categorySerializer = CategorySerializer(categories, many=True)
        return Response(categorySerializer.data, status=200)


class CatalogApi(APIView):
     
    def get(self, request, category=None, sub=None, sub2=None, format=None):
        products = get_products(category, sub, sub2)
        productSerializer = ProductListSerializer(products, many=True)
        return Response(productSerializer.data, status=200)