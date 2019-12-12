from django.urls import path
from django.views.decorators.cache import cache_page

from shop import views

app_name = 'shop'

urlpatterns = [
    path('shop/<slug:category_slug>/', views.product_list, name='products_by_category'),
    path('shop/product/<int:p_id>/', views.product_detail, name='product_detail'),
    # path('', cache_page(60 * 15)(views.product_list), name='product_list'),
    path('', views.product_list, name='product_list'),
]