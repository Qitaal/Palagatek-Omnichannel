from django.db import models

from src.categories.models import Categories
from src.shared.enum import ShopeeStatus


class Products(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Categories, models.SET_NULL, blank=True, null=True)
    shopee_status = models.CharField(choices=ShopeeStatus.choices, max_length=255)
    shopee_id = models.BigIntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(Products, models.CASCADE)
    image = models.ImageField(upload_to='product_images')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_images'

    def __str__(self):
        return 'Image product {0}'.format(self.product)


class Variants(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_variants'

    def __str__(self):
        return self.name


class Colors(models.Model):
    name = models.CharField(max_length=225)
    hex = models.CharField(max_length=225)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_colors'

    def __str__(self):
        return self.name


class ProductsVariantsColors(models.Model):
    product = models.ForeignKey(Products, models.CASCADE)
    variant = models.ForeignKey(Variants, models.SET_NULL, blank=True, null=True)
    color = models.ForeignKey(Colors, models.SET_NULL, blank=True, null=True)
    sku = models.CharField(max_length=225, blank=True, null=True)
    origin_price = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    volume_length = models.FloatField(blank=True, null=True)
    volume_width = models.FloatField(blank=True, null=True)
    volume_height = models.FloatField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to='thumbnail_image', blank=True, null=True)
    shopee_id = models.BigIntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products_variants_colors'

    def __str__(self):
        return '{0} {1} {2}'.format(self.product, self.variant, self.color)
