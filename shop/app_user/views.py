from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_field_name = '/'  # reverse('app_shop:main')


class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'


class CreateProfile(CreateView):
    pass


class DetailAccount(DetailView):
    pass


class DetailProfile(DetailView):
    pass


class UpdateProfile(UpdateView):
    pass
