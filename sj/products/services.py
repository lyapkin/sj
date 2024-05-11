from itertools import chain
from django.db.models import Q
from django.utils.translation import get_language, gettext_lazy as _
from django.db.models import F

from .models import Product, Category, SuperCategory, SubCategory, Brand, Charachteristic, BrandCountry, ProductType
from .serializers import *
from .constants import *


def get_categories(category):
    if category:
        categories = SuperCategory.objects.translated().filter(translations__slug=category)
        categories = categories.first()
        # .children.translated() if categories.exists() else []
    else:
        categories = Category.objects.translated()
    return categories


def sort_products(products, query_params):
    sort = query_params.pop('sort', [RELEVANCE_SORT])

    if sort[0] == RELEVANCE_SORT:
        return products.order_by('-id')
    if sort[0] == POPULARITY_SORT:
        return products #!!!!!!!!!!!!!! implement
    if sort[0] == PRICE_DOWN_SORT:
        return products.order_by('-current_price')
    if sort[0] == PRICE_UP_SORT:
        return products.order_by('current_price')
    
    return products


def filter_products(products, query_params):
    
    is_present = query_params.pop(IS_PRESENT_FILTER, None)
    if is_present is not None and is_present[0] == 1:
        products = products.filter(is_present=True)
    elif is_present is not None and is_present[0] == 0:
        product = product.filter(is_present=False)

    discount = query_params.pop(DISCOUNT_FILTER, None)
    if discount is not None and discount[0] == 1:
        products = products.filter(current_price__lt=F('actual_price'))

    brands = query_params.pop(BRAND_REQUEST_KEY, None)
    if brands is not None and len(brands) > 0:
        products = products.filter(brand__slug__in=brands)

    brand_countries = query_params.pop(BRAND_COUNTRY_REQUEST_KEY, None)
    if brand_countries is not None and len(brand_countries) > 0:
        products = products.filter(brand__country__slug__in=brand_countries)

    product_types = query_params.pop(PRODUCT_TYPE_REQUEST_KEY, None)
    if product_types is not None and len(product_types) > 0:
        products = products.filter(type__translations__slug__in=product_types)

    price_min = query_params.pop(PRICE_MIN_FILTER, None)
    if price_min is not None and len(price_min) > 0:
        products = products.filter(current_price__gte=price_min[0])

    price_max = query_params.pop(PRICE_MAX_FILTER, None)
    if price_max is not None and len(price_max) > 0:
        products = products.filter(current_price__lte=price_max[0])
    
    for param in query_params:
        params_list = query_params.getlist(param)
        products = products.filter(charachteristics__translations__slug__in=params_list)

    return products

    


def get_products(category, sub, sub2, brandname, query_params):
    query_params = query_params.copy()
    # sort = query_params.pop('sort', None)
    query_params.pop('page', None)
    
    products = Product.objects.translated().all()

    products = sort_products(products, query_params)
    section = None

    if brandname:
        products = products.filter(brand__slug=brandname)
    elif sub2:
        category = Category.objects.translated().filter(translations__slug=category)
        subcategories = SubCategory.objects.translated().filter(translations__slug=sub, parent__in=category)
        end_subcategories = SubCategory.objects.translated().filter(translations__slug=sub2, parent__in=subcategories)
        products = products.filter(category__in=end_subcategories)
    elif sub:
        category = Category.objects.filter(translations__slug=category)
        subcategories = SubCategory.objects.filter(translations__slug=sub, parent__in=category)
        children = SubCategory.objects.filter(parent__in=subcategories)
        if children.exists():
            products = products.filter(category__in=children)
        else:
            products = Product.objects.translated().filter(category__in=subcategories)
    elif category:
        categories = SubCategory.objects.filter(parent__translations__slug=category)
        end_categories = categories.filter(children__isnull=True)
        parent_categories = categories.filter(children__isnull=False)
        end_categories2 = SubCategory.objects.filter(parent__in=parent_categories)
        products = products.filter(Q(category__in=end_categories) | Q(category__in=end_categories2))

    products = filter_products(products, query_params)
    
    return products


def get_section(category=None, sub=None, sub2=None, brandname=None):
    section = None
    if brandname:
        brand = Brand.objects.translated().filter(slug=brandname)
        if brand.exists():
            section = BrandSerializer(brand.first()).data
    elif sub2:
        sub_obj = SuperCategory.objects.translated().filter(translations__slug=sub2)
        if sub_obj.exists():
            section = SuperCategorySerializer(sub_obj.first()).data
    elif sub:
        sub_obj = SuperCategory.objects.translated().filter(translations__slug=sub)
        if sub_obj.exists():
            section = SuperCategorySerializer(sub_obj.first()).data
    elif category:
        sub_obj = SuperCategory.objects.translated().filter(translations__slug=category)
        if sub_obj.exists():
            section = SuperCategorySerializer(sub_obj.first()).data
    return section



def get_brands():
    brands = Brand.objects.translated().all()
    return brands


def get_brand_countries():
    countries = BrandCountry.objects.translated().all()
    return countries


def get_types():
    types = ProductType.objects.translated()
    return types


def get_charachteristics():
    charachteristics = Charachteristic.objects.translated()
    return charachteristics


def serialize_filters(types, brands, countries, charachterisctics):
    brands_serializer = BrandFilterSerializer(brands, many=True)
    types_serializer = TypeFilterSerializer(types, many=True)
    charachterisctics_serializer = CharachteristicsFilterSerializer(charachterisctics, many=True)
    brand_countries_serializer = BrandCountryFilterSerializer(countries, many=True)
    return {'filters': [
                {'title': _('product_type'), 'request_key': PRODUCT_TYPE_REQUEST_KEY, 'id': -3, 'values': types_serializer.data},
                {'title': _('brand'), 'request_key': BRAND_REQUEST_KEY, 'id': -2, 'values': brands_serializer.data},
                {'title': _('brand_country'), 'request_key': BRAND_COUNTRY_REQUEST_KEY, 'id': -1, 'values': brand_countries_serializer.data},
                *charachterisctics_serializer.data
            ],
            'other_filter_keys': [PRICE_MAX_FILTER, PRICE_MIN_FILTER, IS_PRESENT_FILTER, DISCOUNT_FILTER],
            'sort': [
                {'id': 1, 'slug': RELEVANCE_SORT, 'value': _('relevance')},
                {'id': 2, 'slug': POPULARITY_SORT, 'value': _('popularity')},
                {'id': 3, 'slug': PRICE_UP_SORT, 'value': _('price_up')},
                {'id': 1, 'slug': PRICE_DOWN_SORT, 'value': _('price_down')}
            ]}


def alphabet_brands(data):
    res = {}
    for brand in data:
        first_letter = brand['name'][:1].upper()
        if first_letter in res:
            res[first_letter].append(brand)
        else:
            res[first_letter] = [brand]

    return dict(sorted(res.items()))


def search_products(line):
    products = Product.objects.translated().filter(Q(translations__name__icontains=line) | Q(code__icontains=line), translations__language_code=get_language())
    return products


def search_brands(line):
    brands = Brand.objects.translated().filter(translations__name__icontains=line, translations__language_code=get_language())
    return brands


def serach_categories(line):
    categories = SuperCategory.objects.translated().filter(translations__name__icontains=line, translations__language_code=get_language())
    return categories


def serialize_search(products, brands, categories):
    return {
        'products': SearchProductSerializer(products, many=True).data,
        'categories': SerachCategorySerializer(categories, many=True).data,
        'brands': BrandSerializer(brands, many=True).data
    }

