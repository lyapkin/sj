from django.db.models import Q

from .models import Product, Category, SuperCategory, SubCategory


def get_categories():
    categories = Category.objects.translated()
    return categories


def get_products(category, sub, sub2, query_params):
    products = Product.objects.translated()
    if sub2:
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
    
    return products
