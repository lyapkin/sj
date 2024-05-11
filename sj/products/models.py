from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from common.utils import generate_unique_slug, generate_unique_slug_translated, upload_product_img_to


class Charachteristic(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_('char_name'), max_length=40, unique=True),
        slug = models.SlugField('url', max_length=50, unique=True)
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("product_char")
        verbose_name_plural = _("product_chars")

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(Charachteristic, self.name)
        return super().save(*args, **kwargs)


class CharachteristicValue(TranslatableModel):
    translations = TranslatedFields(
        value = models.CharField(_('char_value_name'), max_length=40, unique=True),
        slug = models.SlugField('url', max_length=50, unique=True)
    )
    charachteristic_key = models.ForeignKey(Charachteristic, models.CASCADE, related_name='values', verbose_name=_('char_name'))

    def __str__(self):
        return f'{str(self.charachteristic_key)} / {self.value}'
    
    class Meta:
        verbose_name = _("product_char_value")
        verbose_name_plural = _("product_char_values")

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(CharachteristicValue, self.value)
        return super().save(*args, **kwargs)


class SuperCategory(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_('category_name'), max_length=40, unique=True),
        slug = models.SlugField('url', max_length=50, unique=True)
    )
    charachteristic = models.ManyToManyField(Charachteristic, blank=True)

    order = models.PositiveSmallIntegerField(_('order'), default=32000)

    top = models.BooleanField(default=True)
    second = models.BooleanField(default=False)

    def __str__(self):
        try:
            return str(self.subcategory)
        except SuperCategory.subcategory.RelatedObjectDoesNotExist:
            return str(self.category)


class Category(SuperCategory):

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def save(self, *args, **kwargs):
        self.top = True
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(Category, self.name)
        return super().save(*args, **kwargs)


class SubCategory(SuperCategory):
    parent = models.ForeignKey(SuperCategory, on_delete=models.CASCADE, related_name='children', verbose_name=_('parent_category'))

    def __str__(self):
        return f'{self.parent} / {self.name}'

    class Meta:
        verbose_name = _("subcategory")
        verbose_name_plural = _("subcategories")

    def save(self, *args, **kwargs):
        self.top = False
        if self.parent.top:
            self.second = True
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(SubCategory, self.name)
        return super().save(*args, **kwargs)
    

class BrandCountry(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_('country'), max_length=40, unique=True),
    )
    slug = models.SlugField('url', max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("brand_country")
        verbose_name_plural = _("brand_countries")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug.strip())
        return super().save(*args, **kwargs)
    

class Brand(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_('brand'), max_length=80, unique=True),
    )
    slug = models.SlugField('url', max_length=90, unique=True)
    country = models.ForeignKey(BrandCountry, on_delete=models.SET_NULL, related_name='brands', null=True, verbose_name=_('country'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug.strip())
        return super().save(*args, **kwargs)


class ProductType(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("product_type"), max_length=100, unique=True),
        slug = models.SlugField("url", max_length=130, unique=True, blank=True),
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(ProductType, self.name)
        obj = super().save(*args, **kwargs)
        return obj
 

class Product(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("product_name"), max_length=100, unique=True),
        slug = models.SlugField("url", max_length=130, unique=True, blank=True),
        description = models.TextField(_('description'))
    )
    is_present = models.BooleanField(_('presence'), default=False)
    is_prioritized = models.BooleanField(_('is_prioritized'), default=False)
    actual_price = models.PositiveIntegerField(_('actual_price'), null=True, blank=True)
    current_price = models.PositiveIntegerField(_('current_price'), null=True, blank=True)
    order = models.PositiveSmallIntegerField(_('order'), default=32000)
    code = models.CharField(_("part_number"), max_length=20, unique=True, null=True, blank=True)

    category = models.ForeignKey(SuperCategory, on_delete=models.SET_NULL, related_name='products', null=True)

    type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, related_name='products', null=True, verbose_name=_('product_type'))
    brand = models.ForeignKey(Brand, models.SET_NULL, related_name='products', null=True, verbose_name=_('product_brand'))

    charachteristics = models.ManyToManyField(CharachteristicValue, blank=True)

    # brand
    # brand_country
    # product_type

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug.strip():
            self.slug = generate_unique_slug_translated(Product, self.name)
        obj = super().save(*args, **kwargs)
        return obj


class ProductImg(models.Model):
    img_url = models.ImageField(_("product_img"), upload_to=upload_product_img_to)
    product = models.ForeignKey(Product, models.CASCADE, related_name='img_urls', verbose_name=_('product'))

    def __str__(self):
        return str(self.img_url)
    
    class Meta:
        verbose_name = _("product_img")
        verbose_name_plural = _("product_imgs")