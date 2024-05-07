from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language, gettext_lazy as _
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from .models import *


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
    

class ProductImgsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImg
        fields = (
            'id',
            'img_url'
        )


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


class CharachteristicSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model= Charachteristic)

    class Meta:
        model = Charachteristic
        fields = ('translations',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        translations = rep['translations'].get(get_language(), None)
        if translations:
            rep = translations['name']
        else:
            return None

        return rep


class ProductCharachteristicValuesSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=CharachteristicValue)
    charachteristic_key = CharachteristicSerializer()

    class Meta:
        model = CharachteristicValue
        fields = ('id', 'translations', 'charachteristic_key')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        translations = rep['translations'].get(get_language(), None)
        if translations and rep['charachteristic_key']:
            rep['value'] = translations['value']
            del rep['translations']
        else:
            return None

        return rep
    

# class ProductCharachteristicSerializer(TranslatableModelSerializer):
#     translations = TranslatedFieldsField(shared_model=Charachteristic)

#     class Meta:
#         model = Charachteristic
#         fields = ('id', 'translations', 'charachteristic_key')

    # def to_representation(self, instance):
    #     charachteristic_key = CharachteristicSerializer(instance.charachteristic_key).data['translations'].get(get_language(), None)
    #     if charachteristic_key is None:
    #         return None
        
    #     charachteristic_value = CharachteristicValuesSerializer(instance).data
    #     print('!!!!!!!ERROR when None')
        
    #     if charachteristic_value is None:
    #         return None
    
    #     return {
    #         'id': instance.id,
    #         'key': charachteristic_key['name'],
    #         'value': charachteristic_value['value']
    #     }


# class BrandSerializer(TranslatableModelSerializer):
#     translations = TranslatedFieldsField(shared_model=Brand)

#     class Meta:
#         model = Brand
#         fields = (
#             'id',
#             'translations'
#         )


# class BrandCountrySerializer(TranslatableModelSerializer):
#     translations = TranslatedFieldsField(shared_model=BrandCountry)

#     class Meta:
#         model = BrandCountry
#         fields = (
#             'id',
#             'translations'
#         )


# class ProductBrandSerializer(serializers.BaseSerializer):
#     def to_representation(self, instance):
        
#         brand = BrandSerializer(instance).data['translations'].get(get_language(), None)
#         if brand is None: return None

#         country = BrandCountrySerializer(instance.country).data['translations'].get(get_language(), None)
#         if country is None: return None
        
#         return {
#             'id': instance.id,
#             'name': brand['name'],
#             'country': country['name']
#         }


class ProductItemSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type.name')
    charachteristics = ProductCharachteristicValuesSerializer(many=True)
    img_urls = ProductImgsSerializer(many=True)
    brand = serializers.CharField(source='brand.name')
    brand_country = serializers.CharField(source='brand.country.name')
    
    class Meta:
        model = Product
        fields = (
            'id',
            'slug',
            'type',
            'name',
            'code',
            'brand',
            'brand_country',
            'description',
            'is_present',
            'actual_price',
            'current_price',
            'charachteristics',
            'img_urls',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['charachteristics'] = list(filter(lambda c: c is not None, rep['charachteristics']))
        return rep


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
    

class BrandFilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug')


class BrandCountryFilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug')
    

class TypeFilterSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ('id', 'name', 'slug')
    

class CharachteristicValuesFilterSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=CharachteristicValue)

    class Meta:
        model = CharachteristicValue
        fields = (
            'id',
            'translations'
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        translations = rep['translations'].get(get_language(), None)
        if translations:
            rep['slug'] = translations['slug']
            rep['name'] = translations['value']
            del rep['translations']
        else:
            return None
        
        return rep
    

class CharachteristicsFilterSerializer(serializers.ModelSerializer):
    values = CharachteristicValuesFilterSerializer(many=True)

    class Meta:
        model = Charachteristic
        fields = (
            'id',
            'slug',
            'name',
            'values'
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {
            'title': rep['name'],
            'request_key': rep['slug'],
            'id': rep['id'],
            'values': list(filter(lambda v: v is not None, rep['values']))
        }