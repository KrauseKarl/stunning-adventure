from django.urls import path
from app_user.views import *
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', CreateProfile.as_view(), name='register'),
    path('account/<int:pk>/', DetailAccount.as_view(), name='account'),
    path('profile/<int:pk>/', DetailProfile.as_view(), name='profile'),
    path('profile/<int:pk>/edit/', UpdateProfile.as_view(), name='profile_edit'),
    path('history_view/<int:pk>/', DetailHistoryView.as_view(), name='history_view'),
    path('profile_edit/<int:pk>/', UpdateProfile.as_view(), name='profile_edit'),
]
