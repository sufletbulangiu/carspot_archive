from django.urls import path
from .views import UserRegisterView, UserEditView, PasswordsChangeView, ShowProfilePageView
from django.contrib.auth import views as auth_views
from . import views 

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('password/', PasswordsChangeView.as_view(), name='password'),
    path('password_success', views.password_success, name="pass_success"),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),


]