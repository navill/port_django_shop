from django.urls import path

from order import views

app_name = 'order'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
]
