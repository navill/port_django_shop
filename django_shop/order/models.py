from django.db import models

from shop.models import Product


# Create your models here.

# 주문서
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    post_code = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name


# 주문서 + 제품
class OrderWithItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_item', on_delete=models.CASCADE)
    item = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)

    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.order)
