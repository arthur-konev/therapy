from django.contrib import admin
from .models import GeneralUser
from django.contrib.auth.admin import UserAdmin

admin.site.register(GeneralUser, UserAdmin)