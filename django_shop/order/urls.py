from django.urls import path

from order import views

app_name = 'order'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('<order_id>', views.user_order, name='order'),
]
