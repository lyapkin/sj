from django.contrib import admin

from .models import Otp, User, Profile, Email

# Register your models here.
admin.site.register([Otp, User, Profile, Email])