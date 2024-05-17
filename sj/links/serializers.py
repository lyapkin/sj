from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language, gettext_lazy as _
from rest_framework import serializers

from .models import *


class SliderSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Slider
        fields = (
            'id',
            'title',
            'text',
            'button_text',
            'type',
            'link',
            'img',
        )

    def get_type(self, obj):
        return obj.get_type_display()
    

class TabSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = PopularTab
        fields = (
            'id',
            'title',
            'type',
            'link',
            'img',
            'background'
        )

    def get_type(self, obj):
        return obj.get_type_display()


class ModuleSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = (
            'id',
            'title',
            'text',
            'button_text',
            'type',
            'link',
            'img',
            'background'
        )

    def get_type(self, obj):
        return obj.get_type_display()