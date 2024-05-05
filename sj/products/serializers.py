from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from .models import *


class ProductImgsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImg
        fields = (
            'id',
            'img_url'
        )


class ProductTypeSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=ProductType)

    class Meta:
        model = SubCategory
        fields = ('id', 'translations')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        translations = rep['translations'].get(get_language(), None)
        if translations:
            rep['name'] = translations['name']
            rep['slug'] = translations['slug']
            del rep['translations']
        else:
            return None

        return rep


class ProductListSerializer(serializers.ModelSerializer):
    img_urls = ProductImgsSerializer(many=True)
    type = ProductTypeSerializer()

    class Meta:
        model = Product
        fields = (
            "id",
            "slug",
            "name",
            'type',
            "actual_price",
            "current_price",
            "img_urls",
            'is_present',
            'is_prioritized',
        )
        lookup_field = 'slug'


class ProductItemSerializerr(serializers.ModelSerializer):
    pass


class SubCategorySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=SubCategory)

    class Meta:
        model = SubCategory
        fields = ('id', 'translations', 'children')

    def get_fields(self):
        fields = super(SubCategorySerializer, self).get_fields()
        fields['children'] = SubCategorySerializer(many=True)
        return fields
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        translations = rep['translations'].get(get_language(), None)
        if translations:
            rep['name'] = translations['name']
            rep['slug'] = translations['slug']
            del rep['translations']
        else:
            return None
        children = list(filter(lambda c: c is not None, rep['children']))
        del rep['children']
        rep['children'] = children

        return rep


class CategorySerializer(serializers.ModelSerializer):
    children = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'children')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['children'] = list(filter(lambda c: c is not None, rep['children']))
        return rep