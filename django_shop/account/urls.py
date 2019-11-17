from django.contrib.auth import views as auth_views
from django.urls import path

from account import views


urlpatterns = [
    # login & logout
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.change_password_done, name='password_change_done'),

    # edit info
    path('edit/', views.edit_user, name='edit'),
    path('register/', views.register_user, name='register'),

    # history
    path('history/', views.get_history, name='history'),
]
