from django.contrib import admin
from django.contrib.auth.models import Group
from app_user.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'avatar', 'telephone']

admin.site.register(Profile, ProfileAdmin)
