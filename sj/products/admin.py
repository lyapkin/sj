from typing import Any
from django.contrib import admin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import get_language
from parler.admin import TranslatableAdmin, TranslatableTabularInline, SortedRelatedFieldListFilter
from parler.forms import TranslatableModelForm
from itertools import chain
from common.utils import generate_unique_slug, generate_unique_slug_translated

from .models import Product, ProductImg, Category, SubCategory, SuperCategory, ProductType

# Register your models here.
class ImgInline(admin.TabularInline):
    model = ProductImg
    min_num = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset
    

class ProductTypeAdmin(TranslatableAdmin):
    list_display = ['name']
    exclude = ('slug',)

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(ProductTypeAdmin, self).get_queryset(request).translated(language_code).order_by('translations__name')


class ProductForm(TranslatableModelForm):

    class Meta:
        model = Product
        exclude = ['slug']
        # fields = '__all__'
    
    def clean_slug(self):
        slug = self.cleaned_data['slug']
        name = self.cleaned_data['name']
        if not slug:
            slug = generate_unique_slug_translated(Product, name)
        return slug


class ProductAdmin(TranslatableAdmin):
    list_display = ["name", 'type', "code", 'actual_price', 'current_price']
    inlines = [ImgInline]
    form = ProductForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['category'].queryset = SubCategory.objects.filter(children__isnull=True)
        form.base_fields['type'].queryset = ProductType.objects.translated().all()
        return form

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(ProductAdmin, self).get_queryset(request).translated(language_code)
    

class CategoryAdmin(TranslatableAdmin):
    list_display = ["name",]
    exclude = ('slug', 'top', 'second')

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(CategoryAdmin, self).get_queryset(request).translated(language_code).order_by('translations__name')


class SubCategoryAdmin(TranslatableAdmin):
    list_display = ["name", 'parent',]
    exclude = ('slug', 'top', 'second')

    def get_form(self, request, obj=None, **kwargs):
        form = super(SubCategoryAdmin, self).get_form(request, obj, **kwargs)
        obj = request.resolver_match.kwargs.get('object_id')
        form.base_fields['parent'].queryset = SuperCategory.objects.filter(Q(products__isnull=True), Q(top=True) | Q(second=True)).exclude(id=obj)
        return form

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(SubCategoryAdmin, self).get_queryset(request).translated(language_code).order_by('translations__name')
    

admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
