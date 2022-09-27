from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=35)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    base_url = models.URLField()

    def __str__(self):
        return self.image.url


class Product(models.Model):
    base_url = models.URLField()
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.CharField(max_length=5000, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default='')
    discount = models.CharField(max_length=80, default='')

    image = models.OneToOneField(Image, null=True, on_delete=models.SET_NULL)
    categories = models.ManyToManyField(Category, related_name='products')
    sizes = models.ManyToManyField(Size, related_name='products')
    colors = models.ManyToManyField(Color, related_name='products')

    def __str__(self):
        return self.title
