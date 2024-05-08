from django.urls import path, include
from rest_framework import routers


from .views import CatalogApi, CategoriesApi, ProductApi, FiltersApi, BrandApi, SearchApi

router = routers.SimpleRouter()
router.register('', ProductApi)

urlpatterns = [
    # path('', include(router.urls)),
    # path('', get_code),
    path('item/', include(router.urls)),
    path('categories/', CategoriesApi.as_view()),
    path('categories/<str:category>/', CategoriesApi.as_view()),
    path('catalog/', CatalogApi.as_view()),
    path('catalog/<str:category>/', CatalogApi.as_view()),
    path('catalog/<str:category>/<str:sub>/', CatalogApi.as_view()),
    path('catalog/<str:category>/<str:sub>/<str:sub2>/', CatalogApi.as_view()),
    path('brands/', BrandApi.as_view()),
    path('brands/<str:brandname>/', CatalogApi.as_view()),
    path('filters/', FiltersApi.as_view()),
    path('search/', SearchApi.as_view()),
    # path('check/', check_auth),
    # path('logout/', logout_view),
]