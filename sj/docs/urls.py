from django.urls import path, include
from rest_framework import routers


from .views import DocApi

router = routers.SimpleRouter()
router.register('', DocApi)

urlpatterns = [
    # path('', include(router.urls)),
    # path('', get_code),
    path('', include(router.urls)),
    # path('categories/', CategoriesApi.as_view()),
]