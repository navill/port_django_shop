from django.urls import path
from django.views.decorators.cache import cache_page

from shop import views

app_name = 'shop'

urlpatterns = [
    path('shop/<slug:category_slug>/', views.product_list, name='products_by_category'),
    path('shop/list/', views.product_list, name='product_list'),

    path('shop/product/<int:p_id>/', views.product_detail, name='product_detail'),
    path('home/', views.home, name='home'),
]
