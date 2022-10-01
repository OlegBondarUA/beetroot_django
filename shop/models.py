from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=35)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(
        'shop.Product', on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='images')
    base_url = models.URLField()

    def __str__(self):
        return self.image.url


class Product(models.Model):
    base_url = models.URLField(max_length=512)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=5000, default='')
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    old_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True
    )
    availability = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField(Category, related_name='products')
    sizes = models.ManyToManyField(Size, related_name='products')
    color = models.ForeignKey(
        Color, related_name='products', on_delete=models.SET_NULL,
        null=True, blank=True
    )
    brand = models.ForeignKey(
        Brand, related_name='products', on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return self.title
