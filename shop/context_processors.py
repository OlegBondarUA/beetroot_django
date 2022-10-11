from .selectors import categories_selector, random_products_selector


def categories_menu(request):
    return {
        'search_categories': categories_selector()
    }


def featured_products(request):
    return {
        'featured_products': random_products_selector()
    }
