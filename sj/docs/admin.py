from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableTabularInline

from .models import Doc, DocSection

# Register your models here.
class DocSectionInline(TranslatableTabularInline):
    model = DocSection


class DocAdmin(TranslatableAdmin):
    list_display = ['name']
    inlines = [DocSectionInline]

    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(DocAdmin, self).get_queryset(request).translated(language_code)
    

class DocSectionAdmin(TranslatableAdmin):
    list_display = []
    
    def get_queryset(self, request):
        # Limit to a single language!
        language_code = self.get_queryset_language(request)
        return super(DocSectionAdmin, self).get_queryset(request).translated(language_code)


admin.site.register(Doc, DocAdmin)
# admin.site.register(DocSection, DocSectionAdmin)