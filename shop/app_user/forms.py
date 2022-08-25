from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator


class RegisterUserForm(UserCreationForm):
    telephone = forms.CharField(validators=[RegexValidator('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')])
    avatar = forms.ImageField(required=False,  label='аватарка')