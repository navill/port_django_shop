from django.contrib import admin

# Register your models here.
from shop.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # key 값에 해당하는 필드를 value 값을 기준으로 자동 생성
    # -> slug field는 자동으로 name필드에 의해 생성
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'price', 'created', 'updated', 'available_stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    # admin에서 사용될 default filter
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available', 'price', 'available_stock']
