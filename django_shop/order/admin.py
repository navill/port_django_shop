from django.contrib import admin

from order.models import Order, OrderWithItem


# Register your models here.
class OrderWithItemInline(admin.TabularInline):
    model = OrderWithItem
    raw_id_fields = ['item']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'address', 'post_code', 'created']
    list_filter = ['first_name', 'created']
    inlines = [OrderWithItemInline]
