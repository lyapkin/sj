from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from common.utils import generate_unique_slug, generate_unique_slug_translated, upload_product_img_to

# Create your models here.
class Slider(TranslatableModel):
    TYPES = [
        ('BRND', 'brand'),
        ('CTGR', 'category'),
        ('PROD', 'product'),
    ]

    translations = TranslatedFields(
        title = models.CharField(_('slider_title'), max_length=50, unique=True),
        text = models.CharField(_('slider_text'), max_length=100),
        button_text = models.CharField(_('slider_link_text'), max_length=30),
        link = models.CharField(_('slider_link'), max_length=128)
    )

    img = models.ImageField(_('slider_img'), upload_to='images/links/slider/%Y/%m/%d')

    type = models.CharField(max_length=4, choices=TYPES)
    type_id = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("slider")
        verbose_name_plural = _("sliders")


class PopularTab(TranslatableModel):
    TYPES = [
        ('BRND', 'brand'),
        ('CTGR', 'category')
    ]

    translations = TranslatedFields(
        title = models.CharField(_('tab_title'), max_length=50, unique=True),
        link = models.CharField(_('tab_link'), max_length=128)
    )

    img = models.ImageField(_('tab_img'), upload_to='images/links/tab/%Y/%m/%d')
    background = models.ImageField(_('tab_background'), upload_to='images/links/tab/%Y/%m/%d/background')

    type = models.CharField(max_length=4, choices=TYPES)
    type_id = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("popular_tab")
        verbose_name_plural = _("popular_tabs")


class Module(TranslatableModel):
    TYPES = [
        ('BRND', 'brand'),
        ('CTGR', 'category')
    ]

    translations = TranslatedFields(
        title = models.CharField(_('module_title'), max_length=50, unique=True),
        text = models.CharField(_('module_text'), max_length=100),
        button_text = models.CharField(_('module_link_text'), max_length=30),
        link = models.CharField(_('module_link'), max_length=128)
    )

    img = models.ImageField(_('module_img'), upload_to='images/links/module/%Y/%m/%d')
    background = models.ImageField(_('module_background'), upload_to='images/links/module/%Y/%m/%d/background')

    type = models.CharField(max_length=4, choices=TYPES)
    type_id = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("module")
        verbose_name_plural = _("modules")