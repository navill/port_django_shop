from django.db import models

from shop.models import Product


# Create your models here.

# 주문서
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    post_code = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.first_name


# 주문서 + 제품
class OrderWithItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_item', on_delete=models.CASCADE)
    item = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)

    total_price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "OrderWithItem"
        verbose_name_plural = "OrderWithItems"

    def __str__(self):
        return self.order
