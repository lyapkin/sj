from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language, gettext_lazy as _
from rest_framework import serializers

from .models import *


class SliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slider
        fields = (
            'id',
            'title',
            'text',
            'button_text',
            'link',
            'img',
        )
    

class TabSerializer(serializers.ModelSerializer):

    class Meta:
        model = PopularTab
        fields = (
            'id',
            'title',
            'link',
            'img',
            'background'
        )


class ModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Module
        fields = (
            'id',
            'title',
            'text',
            'button_text',
            'link',
            'img',
            'background'
        )