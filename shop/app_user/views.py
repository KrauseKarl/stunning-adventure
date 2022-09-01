import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from app_user.forms import RegisterUserForm, UpdateUserForm, AuthForm
from app_user.models import Profile


class UserLoginView(LoginView):
    REDIRECT_FIELD_NAME = 'item/list'
    template_name = 'users/login.html'
    redirect_field_name = None
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('app_user:account',
                       kwargs={'pk': self.request.user.pk})


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'


class CreateProfile(SuccessMessageMixin, CreateView):
    model = User
    second_model = Profile
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('app_item:item_list')
    success_message = "%(calculated_field)s was created successfully"

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            calculated_field=self.object.calculated_field,
        )

    def form_valid(self, form):
        user = form.save()
        verified_user = Group.objects.get(name='Пользователь')
        user.groups.add(verified_user)
        telephone = str(form.cleaned_data.get('telephone'))
        telephone = telephone.split('7')[1].replace('(', '').replace(')', '').replace(' ', '')
        Profile.objects.create(
            user=user,
            telephone=telephone,
            group=verified_user,
        )
        # logger = logging.getLogger('register_user')
        # logger.info('[{user}] has been successfully registered'.format(user=user.profile.__str__()))
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(self.request,
                            username=username,
                            password=raw_password)
        login(self.request, user)
        return redirect(self.success_url)
        # else:
        #     from django.contrib import messages
        #
        #     messages.success(self.request, "Такой пользователь уже зарегистрирован")
        #     return redirect('app_user:register')

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""

        messages = 'Такой пользователь уже зарегистрирован'
        return self.render_to_response(self.get_context_data(form=form, messages=messages))


class DetailAccount(DetailView):
    model = User
    template_name = 'users/account.html'
    context_object_name = 'user'


class DetailProfile(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'


class DetailHistoryView(DetailView):
    model = User
    template_name = 'users/history_view.html'
    context_object_name = 'user'


class UpdateProfile(UpdateView):
    model = User
    second_model = Profile
    template_name = 'users/profile_edit.html'
    form_class = UpdateUserForm

    def get_success_url(self):
        return reverse('app_user:account',
                       kwargs={'pk': self.request.user.pk})
