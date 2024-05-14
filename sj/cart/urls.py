from django.urls import path, include
from rest_framework import routers


from .views import CartApi

router = routers.SimpleRouter()
router.register('', CartApi)

urlpatterns = [
    path('', include(router.urls)),
]