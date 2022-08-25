from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from app_user.forms import RegisterUserForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_field_name = '/'  # reverse('app_shop:main')


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'


class CreateProfile(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('app_user:account')


class DetailAccount(DetailView):
    pass


class DetailProfile(DetailView):
    pass


class UpdateProfile(UpdateView):
    pass
