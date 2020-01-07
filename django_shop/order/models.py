from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shop.models import Product

User = get_user_model()


# 주문서
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    post_code = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField(default=0)

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

# bulk를이용할 때 save signal 못씀...
# @receiver(post_save, sender=OrderWithItem)
# def order_item_post_saved_receiver(sender, instance, created, *args, **kwargs):
#     order_item = instance
#     print(order_item)
# Order.objects.filter(order_item.order)
# category.save()
