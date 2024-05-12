from django.shortcuts import render
from rest_framework import mixins, viewsets


from .models import FAQCategory
from .serializers import FAQCategorySerializer


class FAQApi(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = FAQCategory.objects.translated().all()
    serializer_class = FAQCategorySerializer

    def get_queryset(self):
        return super().get_queryset().translated()
