from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableTabularInline

from .models import *


class FAQCategoryAdmin(TranslatableAdmin):
    list_display = ['name']

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(FAQCategoryAdmin, self).get_queryset(request).translated(language_code)
    

class FAQAdmin(TranslatableAdmin):
    list_display = ['question']
    
    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(FAQAdmin, self).get_queryset(request).translated(language_code)


admin.site.register(FAQCategory, FAQCategoryAdmin)
admin.site.register(FAQ, FAQAdmin)