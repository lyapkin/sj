from django.urls import path, include
from rest_framework import routers


from .views import get_code, confirm, check_auth, logout_view

# router = routers.SimpleRouter()
# router.register('get_code', get_code, basename='get_code')

urlpatterns = [
    # path('', include(router.urls)),
    path('code/', get_code),
    path('confirmation/', confirm),
    path('check/', check_auth),
    path('logout/', logout_view),
]