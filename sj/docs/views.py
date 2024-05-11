from django.shortcuts import render
from rest_framework import views, mixins, viewsets, status

from .models import Doc
from .serializers import DocSerializer

# Create your views here.
class DocApi(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Doc.objects.translated().all()
    serializer_class = DocSerializer