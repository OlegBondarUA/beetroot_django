from django.contrib import admin

from . models import Category, Color, Product, Image, Size


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Size)
