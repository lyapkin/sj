from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language, gettext_lazy as _
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from .models import *
from users.models import FavoriteProduct, FavoriteBrand


class DocSectionSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=DocSection)

    class Meta:
        model = DocSection
        fields = ('id', 'translations')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        translations = rep['translations'].get(get_language(), None)
        if translations:
            rep['title'] = translations['title']
            rep['content'] = translations['content']
            del rep['translations']
        else:
            return None

        return rep
    

class DocSerializer(serializers.ModelSerializer):
    sections = DocSectionSerializer(many=True)

    class Meta:
        model = Doc
        fields = (
            'id',
            'name',
            'sections',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['sections'] = list(filter(lambda s: s is not None, rep['sections']))
        return rep