from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language, gettext_lazy as _
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from .models import *


class FAQSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=FAQ)

    class Meta:
        model = FAQ
        fields = ('id', 'translations')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        translations = rep['translations'].get(get_language(), None)
        if translations:
            rep['question'] = translations['question']
            rep['answer'] = translations['answer']
            del rep['translations']
        else:
            return None

        return rep
    

class FAQCategorySerializer(serializers.ModelSerializer):
    faqs = FAQSerializer(many=True)

    class Meta:
        model = FAQCategory
        fields = (
            'id',
            'name',
            'faqs',
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['faqs'] = list(filter(lambda s: s is not None, rep['faqs']))
        return rep