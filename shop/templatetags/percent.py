from decimal import Decimal

from django import template


register = template.Library()


@register.simple_tag
def discount_rate(retail_price, sale_price):
    return round(((Decimal(retail_price) - Decimal(sale_price)) / Decimal(retail_price)) * 100)


@register.filter(name='add_dollar')
def add_dollar(value, arg):
    if value:
        return f'{arg}{value}'
