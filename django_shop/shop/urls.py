from django.conf import settings
from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf.urls.static import static
from shop import views

app_name = 'shop'

urlpatterns = [
    path('shop/list/', views.product_list, name='product_list'),
    path('shop/<slug:category_slug>/', views.product_list, name='products_by_category'),
    path('shop/product/<int:p_id>/', views.product_detail, name='product_detail'),
    path('', views.home, name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)