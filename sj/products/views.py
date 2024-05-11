from rest_framework.permissions import IsAuthenticated
from rest_framework import views, mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


from .services import *
from .serializers import ProductListSerializer, CategorySerializer, ProductItemSerializer, SubCategoryFeedSerializer, BrandSerializer
from .models import Product
from users.models import FavoriteProduct, FavoriteBrand


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
        section = get_section(category, sub, sub2, brandname)
        paginated_response = paginator.get_paginated_response(product_serializer.data)
        paginated_response.data['section'] = section
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
        brands = search_brands(request.query_params.get('q'))
        categories = serach_categories(request.query_params.get('q'))
        search = serialize_search(products, brands, categories)
        return Response(search, status=200)
    

class FavoriteProductsApi(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = FavoriteProduct.objects.all()
    pagination_class = CatalogApiPagination
    serializer_class = FavoriteProductSerilizer
    
    def list(self, request, format=None):
        profile = request.user.profile
        products = profile.favorite_products.all().order_by('-created_at').translated()
        paginator = self.pagination_class()
        result_products = paginator.paginate_queryset(products, request, view=self)
        product_serializer = ProductListSerializer(result_products, many=True)
        paginated_response = paginator.get_paginated_response(product_serializer.data)
        return paginated_response
    
    def create(self, request, *args, **kwargs):
        product_id = request.data['id']
        profile_id = request.user.profile.id
        serializer = self.get_serializer(data={'product': product_id, 'user': profile_id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_kwargs = {'user': self.request.user.profile.id, 'product': self.kwargs['pk']}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
        

class FavoriteBrandsApi(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = FavoriteBrand.objects.all()
    serializer_class = FavoriteBrandSerilizer
    
    def list(self, request, format=None):
        profile = request.user.profile
        brands = profile.favorite_brands.all().order_by('translations__name').translated()
        brand_serializer = BrandSerializer(brands, many=True)
        return Response(brand_serializer.data, status=200)
    
    def create(self, request, *args, **kwargs):
        brand_id = request.data['id']
        profile_id = request.user.profile.id
        serializer = self.get_serializer(data={'brand': brand_id, 'user': profile_id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter_kwargs = {'user': self.request.user.profile.id, 'brand': self.kwargs['pk']}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
