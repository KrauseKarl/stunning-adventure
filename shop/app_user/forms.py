from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# validators=[RegexValidator('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')]

class AuthForm(forms.Form):
    """
    Форма для аутентификации пользователя
    (model User)
    """
    default_errors = {
        'required': 'Поле обязательно для заполнения',
        'invalid': 'Введите допустимое значение'
    }
    username = forms.CharField(error_messages=default_errors)
    password = forms.CharField(widget=forms.PasswordInput, error_messages=default_errors)


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='имя пользователя',
                               widget=forms.Textarea(attrs={'rows': 1, 'cols': 20})
                               )
    password1 = forms.CharField(label="пароль", strip=False,
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
                                )
    password2 = forms.CharField(label="пароль подтвердить", strip=False, help_text='',
                                widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

    telephone = forms.CharField(label='телефон')

    email = forms.EmailField(required=False, label='E-mail')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'telephone','email')

    # def clean_password_confirm(self):
    #     # Check that the two password entries match
    #     password = self.cleaned_data.get("password")
    #     password_confirm = self.cleaned_data.get("password_confirm")
    #     if password and password_confirm and password != password_confirm:
    #         raise forms.ValidationError("Пароли не совпадают")
    #     return password
    #
    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user


class UpdateUserForm(UserChangeForm):
    first_name = forms.CharField(
        max_length=30,
        label='Имя',
        widget=forms.Textarea(attrs={'rows': 1, 'cols': 20})
    )
    last_name = forms.CharField(
        max_length=30,
        label='Фамилия',
        widget=forms.Textarea(attrs={'rows': 1, 'cols': 20})
    )
    password1 = forms.CharField(
        label="пароль",
        strip=False,
        help_text='Your password must contain at least: '
                  ' 1 uppercase letter,  '
                  ' 1 lowercase letter,'
                  ' 1 special character (#?!@$%^&*-), '
                  ' 1 number and  8 characters.',

        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label="пароль подтвердить",
        strip=False,
        help_text='',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    telephone = forms.CharField(validators=[RegexValidator('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')],
                                label='телефон')
    avatar = forms.ImageField(required=False, label='аватарка')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'telephone')



# class UpdateUserForm(forms.ModelForm):
#     """
#     Форма для обновления полей 'First name' и 'Last name'
#     профиля пользователя (model User)
#     """
#     default_errors = {
#         'required': _('This field is required'),
#         'invalid': _('Please enter a valid value')
#     }
#     first_name = forms.CharField(
#         max_length=30,
#         label=_('First name'),
#         widget=forms.Textarea(attrs={'rows': 1, 'cols': 20}),
#         error_messages=default_errors
#     )
#     last_name = forms.CharField(
#         max_length=30,
#         label=_('Last name'),
#         error_messages=default_errors,
#         widget=forms.Textarea(attrs={'rows': 1, 'cols': 20})
#     )
#
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name')
#
#
# class UpdateProfileForm(forms.ModelForm):
#     """
#     Форма для обновления полей
#     'avatar' профиля пользователя
#     (model Profile)
#     """
#     my_default_errors = {
#         'required': _('This field is required'),
#         'invalid': _('Please enter a valid value')
#     }
#     avatar = forms.ImageField(
#         required=False,
#         label=_('avatar')
#     )
#
#     class Meta:
#         model = Profile
#         fields = ['avatar']
