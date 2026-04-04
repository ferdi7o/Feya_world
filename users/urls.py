from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, ProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html', success_url='/profile/'), name='password_change'),
]