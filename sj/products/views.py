from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .services import get_categories, get_products
from .serializers import ProductListSerializer, CategorySerializer


class CategoriesApi(APIView):

    def get(self, request):
        categories = get_categories()
        categorySerializer = CategorySerializer(categories, many=True)
        return Response(categorySerializer.data, status=200)
    

class ProductAPIListPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 50


class CatalogApi(APIView):
    pagination_class = ProductAPIListPagination
     
    def get(self, request, category=None, sub=None, sub2=None, format=None):
        products = get_products(category, sub, sub2, request.query_params)
        paginator = self.pagination_class()
        result_products = paginator.paginate_queryset(products, request, view=self)
        productSerializer = ProductListSerializer(result_products, many=True)
        paginated_response = paginator.get_paginated_response(productSerializer.data)
        return paginated_response