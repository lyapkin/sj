from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class FAQCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("question_category"), max_length=50, unique=True)
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("question_category")
        verbose_name_plural = _("question_categories")


class FAQ(TranslatableModel):
    translations = TranslatedFields(
        question = models.CharField(_("question"), max_length=255, unique=True),
        answer = CKEditor5Field(_("answer"), config_name='extends')
    )
    categories = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name="faqs", verbose_name=_("question_category"))

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name = _("faq")
        verbose_name_plural = _("faqs")

