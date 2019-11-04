from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('<slug:category_slug>/', views.product_list, name='products_by_category'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('', views.product_list, name='product_list'),
]