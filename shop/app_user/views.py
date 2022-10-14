import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.models import User, Group
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from app_cart.models import Cart, CartItem
from app_item.models import Item
from app_order.models import Order
from app_user.forms import RegisterUserForm, UpdateUserForm
from app_user.models import Profile
from app_user.services.registration_service import send_mail_to_verify_account, account_activation_token


class UserLoginView(LoginView):
    REDIRECT_FIELD_NAME = 'item/list'
    template_name = 'users/login.html'
    redirect_field_name = None
    redirect_authenticated_user = True

    # def dispatch(self, request, *args, **kwargs):
    #
    #     return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('app_user:account', kwargs={'pk': self.request.user.pk})


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = reverse_lazy('app_item:item_list')


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
        unverified_user = Group.objects.get(name='unverified')
        telephone = str(form.cleaned_data.get('telephone'))
        telephone = telephone.split('7')[1].replace('(', '').replace(')', '').replace(' ', '')
        email = form.cleaned_data.get('email')
        Profile.objects.create(
            user=user,
            telephone=telephone,
            group=unverified_user,
            email=email,
        )
        # logger = logging.getLogger('register_user')
        # logger.info('[{user}] has been successfully registered'.format(user=user.profile.__str__()))
        # send_mail_to_verify_account(user)
        # token = account_activation_token.make_token(user)
        # current_site = get_current_site(self.request)
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        #
        # subject = 'Activate your Account'
        # message = render_to_string(
        #     'users/account_activation_email.html', {
        #         'user': user,
        #         'domain': current_site.domain,
        #         'uid': uid,
        #         'token': token,
        #     })
        # to = user.email

        send_mail_to_verify_account(self.request, user)

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
        messages = 'Такой пользователь уже зарегистрирован'
        return self.render_to_response(self.get_context_data(form=form, messages=messages))


class DetailAccount(DetailView):
    model = User
    template_name = 'users/account.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.filter(user=self.get_object()).last()
        return context


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
        return reverse('app_user:account', kwargs={'pk': self.request.user.pk})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        verified_user_group = Group.objects.get(name='Пользователь')

        user.profile.group = verified_user_group
        user.profile.save()
        user.groups.add(verified_user_group)
        user.save()

    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('app_user:activated_success')
    else:
        return redirect('app_user:invalid_activation')


class ActivatedAccount(TemplateView):
    model = User
    template_name = 'users/activated_successfully.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user'] = self.request.user
        return self.render_to_response(context)


class InvalidActivatedAccount(TemplateView):
    model = User
    template_name = 'users/activation_invalid.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['user'] = self.request.user
        return self.render_to_response(context)
