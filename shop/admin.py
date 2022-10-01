from django.contrib import admin
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

from . models import Brand, Category, Color, Product, Image, Size


class ImageInlineAdmin(admin.TabularInline):
    model = Image
    fields = ('picture', 'image')
    readonly_fields = fields
    extra = 0

    @staticmethod
    def picture(obj):
        return format_html(
            '<img src="{}" style="max-width: 50px">', obj.image.url
        )


class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    inlines = (ImageInlineAdmin,)
    list_display = ('title', 'price', 'old_price', 'availability')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    list_filter = ('brand', 'color')
    list_editable = ('availability',)

    fieldsets = (
        (None, {
            'fields': (
                'base_url',
                ('title', 'slug'),
                ('description',),
                ('price', 'old_price', 'availability'),
                ('categories', 'sizes'),
                ('color', 'brand'),
            )
        }),
    )


class ImageAdmin(admin.ModelAdmin):
    list_display = ('picture',)

    @staticmethod
    def picture(obj):
        return format_html(
            '<img src="{}" style="max-width: 50px">', obj.image.url
        )


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?brand__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products</a>')


class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?color__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products</a>')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?categories__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products</a>')


class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_products')
    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    @staticmethod
    def total_products(obj):
        count = obj.products.count()
        link = f'/admin/shop/product/?sizes__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} products</a>')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Brand, BrandAdmin)
