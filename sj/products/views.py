from django.shortcuts import render
from rest_framework import views, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .services import *
from .serializers import ProductListSerializer, CategorySerializer, ProductItemSerializer, SubCategoryFeedSerializer, BrandSerializer
from .models import Product


class CategoriesApi(views.APIView):

    def get(self, request, category=None):
        categories = get_categories(category)
        if category:
            category_serializer = ParentCategoryFeedSerializer(categories)
        else:
            category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data, status=200)
    

class CatalogApiPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 50


class CatalogApi(views.APIView):
    pagination_class = CatalogApiPagination
     
    def get(self, request, category=None, sub=None, sub2=None, brandname=None, format=None):
        products = get_products(category, sub, sub2, brandname, request.query_params)
        paginator = self.pagination_class()
        result_products = paginator.paginate_queryset(products, request, view=self)
        product_serializer = ProductListSerializer(result_products, many=True)
        paginated_response = paginator.get_paginated_response(product_serializer.data)
        return paginated_response
    

class ProductApi(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Product.objects.translated().all()
    serializer_class = ProductItemSerializer
    lookup_field = 'translations__slug'


class FiltersApi(views.APIView):

    def get(self, request, format=None):
        brands = get_brands()
        types = get_types()
        charachteristics = get_charachteristics()
        countries = get_brand_countries()
        filters = serialize_filters(types, brands, countries, charachteristics)
        return Response(filters, status=200)


class BrandApi(views.APIView):

    def get(self, request, format=None):
        brands = get_brands()
        brands_serializer = BrandSerializer(brands, many=True)
        response_representation = alphabet_brands(brands_serializer.data)
        return Response(response_representation, status=200)
    

class SearchApi(views.APIView):

    def get(self, request, format=None):
        products = search_products(request.query_params.get('q'))
        products_code = serach_products_by_code(request.query_params.get('q'))
        brands = search_brands(request.query_params.get('q'))
        categories = serach_categories(request.query_params.get('q'))
        search = serialize_search(products, products_code, brands, categories)
        return Response(search, status=200)