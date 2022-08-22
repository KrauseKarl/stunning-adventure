from django.urls import path
from app_user.views import CreateView, DetailProfile, UpdateProfile, UserLoginView, UserLogoutView, DetailAccount
urlpatterns = [
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/register/', CreateView.as_view(), name='register'),
    path('accounts/account/<int:pk>/', DetailAccount.as_view(), name='account'),
    path('accounts/profile/<int:pk>/', DetailProfile.as_view(), name='profile'),
    path('accounts/profile_edit/<int:pk>/', UpdateProfile.as_view(), name='profile_edit'),

]
