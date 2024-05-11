from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Doc(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_('doc_name'), max_length=150, unique=True)
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("site_doc")
        verbose_name_plural = _("site_docs")


class DocSection(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_('doc_section_title'), max_length=150),
        content = CKEditor5Field(_("doc_section_text"), config_name='extends'),
    )
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='sections')

    def __str__(self):
        return self.doc.name + " / " + self.title
    
    class Meta:
        verbose_name = _("site_doc_section")
        verbose_name_plural = _("site_doc_sections")