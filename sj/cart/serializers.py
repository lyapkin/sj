from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language, gettext_lazy as _
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from .models import *
from products.models import Product
from products.serializers import ProductImgsSerializer


class CartProductSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type.name')
    img_urls = ProductImgsSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'type',
            'name',
            'actual_price',
            'current_price',
            'img_urls',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['img_url'] = rep['img_urls'][0]['img_url']
        del rep['img_urls']
        return rep


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('id', 'user', 'product', 'quantity')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['product'] = CartProductSerializer(Product.objects.get(id=rep['product'])).data

        return {
            **rep['product'],
            'quantity': rep['quantity']
        }
    
