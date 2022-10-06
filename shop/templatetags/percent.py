from decimal import Decimal

from django import template


register = template.Library()


@register.simple_tag
def discount_rate(retail_price, sale_price, base=Decimal(1)):
    return base * round(
        ((Decimal(retail_price) - Decimal(sale_price))
         / Decimal(retail_price)) * 100 / base)
