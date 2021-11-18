from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User


# Register your models here.

admin.site.register(User)