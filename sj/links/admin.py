from typing import Any
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django import forms
from parler.admin import TranslatableAdmin, TranslatableTabularInline, SortedRelatedFieldListFilter
from parler.forms import TranslatableModelForm

from .models import Slider, PopularTab, Module
from products.models import Product, SuperCategory, Brand
from products.constants import POPULARITY_SORT

# Register your models here.
class SliderForm(TranslatableModelForm):
    CATEGORY = 'category'
    BRAND = 'brand'
    PRODUCT = 'product'
    types = set([CATEGORY, BRAND, PRODUCT])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.CATEGORY] = forms.ModelChoiceField(queryset=SuperCategory.objects.active_translations(language_code=self.language_code).order_by('-top', '-second', 'translations__name'), required=False)
        self.fields[self.BRAND] = forms.ModelChoiceField(queryset=Brand.objects.active_translations(language_code=self.language_code).all().order_by('translations__name'), required=False)
        self.fields[self.PRODUCT] = forms.ModelChoiceField(queryset=Product.objects.active_translations(language_code=self.language_code).all().order_by('translations__name'), required=False)

    category = forms.ChoiceField()
    brand = forms.ChoiceField()
    product = forms.ChoiceField()

    def clean(self) -> dict[str, Any]:
        # Проверяет, что выбрано только одно поле из types, иначе выбрасывает исключение валидации
        if len(self.types.intersection(set(map(lambda t: t[0] if t[1] is not None else None, self.cleaned_data.items())))) != 1:
            raise ValidationError(_('links_type_validation'))
        return super().clean()

    def save(self, commit: bool = ...) -> Any:
        type = list(filter(lambda t: t[0] in self.types and t[1] is not None, self.cleaned_data.items()))[0][1]
        self.instance.link = type.construct_link(self.language_code)
        return super().save(commit)

    class Meta:
        model = Slider
        exclude = ('link',)
        # fields = '__all__'


class SliderAdmin(TranslatableAdmin):
    list_display = ['title']
    form = SliderForm
    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'button_text', )
        },),
        (None, {
            'fields': ('img',)
        }),
        (_('links_type'), {
            'fields': ('category', 'brand', 'product')
        }),
    )
    
    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(SliderAdmin, self).get_queryset(request).translated(language_code).order_by('translations__title')
    

class TabForm(TranslatableModelForm):
    CATEGORY = 'category'
    BRAND = 'brand'
    types = set([CATEGORY, BRAND])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.CATEGORY] = forms.ModelChoiceField(queryset=SuperCategory.objects.active_translations(language_code=self.language_code).order_by('-top', '-second', 'translations__name'), required=False)
        self.fields[self.BRAND] = forms.ModelChoiceField(queryset=Brand.objects.active_translations(language_code=self.language_code).all().order_by('translations__name'), required=False)

    category = forms.ChoiceField()
    brand = forms.ChoiceField()

    def clean(self) -> dict[str, Any]:
        # Проверяет, что выбрано только одно поле из types, иначе выбрасывает исключение валидации
        if len(self.types.intersection(set(map(lambda t: t[0] if t[1] is not None else None, self.cleaned_data.items())))) != 1:
            raise ValidationError(_('links_type_validation'))
        return super().clean()

    def save(self, commit: bool = ...) -> Any:
        type = list(filter(lambda t: t[0] in self.types and t[1] is not None, self.cleaned_data.items()))[0][1]
        self.instance.link = type.construct_link(self.language_code, POPULARITY_SORT)
        return super().save(commit)

    class Meta:
        model = PopularTab
        exclude = ('link',)
        # fields = '__all__'


class TabAdmin(TranslatableAdmin):
    list_display = ['title']
    form = TabForm
    fieldsets = (
        (None, {
            'fields': ('title', )
        },),
        (None, {
            'fields': ('img', 'background')
        }),
        (_('links_type'), {
            'fields': ('category', 'brand')
        }),
    )
    
    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(TabAdmin, self).get_queryset(request).translated(language_code).order_by('translations__title')
    

class ModuleForm(TranslatableModelForm):
    CATEGORY = 'category'
    BRAND = 'brand'
    types = set([CATEGORY, BRAND])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.CATEGORY] = forms.ModelChoiceField(queryset=SuperCategory.objects.active_translations(language_code=self.language_code).order_by('-top', '-second', 'translations__name'), required=False)
        self.fields[self.BRAND] = forms.ModelChoiceField(queryset=Brand.objects.active_translations(language_code=self.language_code).all().order_by('translations__name'), required=False)

    category = forms.ChoiceField()
    brand = forms.ChoiceField()

    def clean(self) -> dict[str, Any]:
        # Проверяет, что выбрано только одно поле из types, иначе выбрасывает исключение валидации
        if len(self.types.intersection(set(map(lambda t: t[0] if t[1] is not None else None, self.cleaned_data.items())))) != 1:
            raise ValidationError(_('links_type_validation'))
        return super().clean()

    def save(self, commit: bool = ...) -> Any:
        type = list(filter(lambda t: t[0] in self.types and t[1] is not None, self.cleaned_data.items()))[0][1]
        self.instance.link = type.construct_link(self.language_code)
        return super().save(commit)

    class Meta:
        model = Module
        exclude = ('link',)
        # fields = '__all__'


class ModuleAdmin(TranslatableAdmin):
    list_display = ['title']
    form = ModuleForm
    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'button_text', )
        },),
        (None, {
            'fields': ('img', 'background')
        }),
        (_('links_type'), {
            'fields': ('category', 'brand')
        }),
    )
    
    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(ModuleAdmin, self).get_queryset(request).translated(language_code).order_by('translations__title')


admin.site.register(Slider, SliderAdmin)
admin.site.register(PopularTab, TabAdmin)
admin.site.register(Module, ModuleAdmin)