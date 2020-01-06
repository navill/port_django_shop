from django.db import models

# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, db_index=True)
    items = models.IntegerField(default=0)
    slug = models.SlugField(max_length=200, db_index=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:products_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)

    quantity = models.IntegerField(default=0)
    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id])


@receiver([post_save, post_delete], sender=Product)
def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    category = product.category
    category.items = Product.objects.filter(category=category).count()
    category.save()
