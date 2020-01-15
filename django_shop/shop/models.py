from django.db import models

# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


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

    # def get_image_url(self):
    #     img = self.product_image.first()
    #     if img:
    #         # directory path
    #         return img.image.url
    #     return img


@receiver([post_save, post_delete], sender=Product)
def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    product = instance
    category = product.category
    category.items = Product.objects.filter(category=category).count()
    category.save()


def image_upload_to(instance, filename):
    name = instance.product.name
    # 첫 이미지 등록 시 instance.id를 불러오지 못하는 이유
    # ProductImage 모델이 저장되기 전에 instance.id를 호출 -> None 반환
    # -> post_save: 저장 시점에 이미 image_upload_to가 실행되버림
    # instance.id==None
    # Product를 먼저 생성하고 ProductImage를 생성하면서 Product.id를 이용
    slug = slugify(name)
    basename, file_extension = filename.split(".")
    new_filename = f"{slug}-{instance.product.id}.{file_extension}"
    return f"products/{slug}/{new_filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_image', on_delete=models.CASCADE)
    # image_upload_to: 함수 호출'()'이 아닌 함수명을 할당
    image = models.ImageField(upload_to=image_upload_to, blank=True, null=True)

    def __str__(self):
        return self.product.name
