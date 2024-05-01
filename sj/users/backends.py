from .models import User, Email, Profile, Otp
from django.db.models import Q
from django.contrib.auth.backends import BaseBackend, ModelBackend
import datetime


class AuthBackend(BaseBackend):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, email=None, code=None, password=None):

        try:
            otp = Otp.objects.get(email=email)
        except Otp.DoesNotExist:
            return None

        if otp.otp != code:
            return None

        email, _ = Email.objects.get_or_create(email=email)

        try:
            user = email.profile.user
        except Profile.DoesNotExist:
            user = User.objects.create(email=email.email)
            profile = Profile.objects.create(user=user, email=email)

        if not user.is_active:
            return None

        return user
