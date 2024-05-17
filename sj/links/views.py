from django.shortcuts import render
from django.utils.translation import get_language
from rest_framework import mixins, viewsets, views, status
from rest_framework.response import Response

from .models import Slider, PopularTab, Module
from .serializers import SliderSerializer, TabSerializer, ModuleSerializer

# Create your views here.
class LinksApi(views.APIView):
    
    def get(self, request):
        sliders_serializer = SliderSerializer(Slider.objects.translated().order_by('-id'), many=True)
        tabs_serializer = TabSerializer(PopularTab.objects.translated(), many=True)
        modules_serializer = ModuleSerializer(Module.objects.translated(), many=True)
        return Response({
            'slides': sliders_serializer.data,
            'tabs': tabs_serializer.data,
            'modules': modules_serializer.data
        }, status=status.HTTP_200_OK)