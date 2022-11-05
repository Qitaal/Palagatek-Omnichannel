from django.db import models

from src.marketplace.models import Marketplaces
from src.products.models import ProductsVariantsColors
from src.shared.enum import OrderStatus
from src.subdivisions.models import Provinces, Cities, Subdistricts


class Orders(models.Model):
    marketplace = models.ForeignKey(Marketplaces, models.SET_NULL, blank=True, null=True)
    serial_number = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    discounted_price = models.IntegerField(blank=True, null=True)
    shipping_fee = models.IntegerField(blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    order_status = models.CharField(choices=OrderStatus.choices, max_length=255)
    recipient_name = models.CharField(max_length=255, blank=True, null=True)
    recipient_phone = models.CharField(max_length=15, blank=True, null=True)
    recipient_province = models.ForeignKey(Provinces, on_delete=models.SET_NULL, blank=True, null=True)
    recipient_city = models.ForeignKey(Cities, on_delete=models.SET_NULL, blank=True, null=True)
    recipient_subdistrict = models.ForeignKey(Subdistricts, on_delete=models.SET_NULL, blank=True, null=True)
    recipient_address = models.CharField(max_length=255, blank=True, null=True)
    recipient_zipcode = models.CharField(max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return '{0} {1}'.format(self.marketplace, self.serial_number)

        
class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, blank=True, null=True)
    products_variants_colors = models.ForeignKey(ProductsVariantsColors, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return '{0} {1}'.format(self.order, self.products_variants_colors)