from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .managers import UserManager


# Create your models here.
class Email(models.Model):
    email = models.EmailField(_('email'), max_length=255, unique=True, primary_key=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('email')
        verbose_name_plural = _('emails')

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(Email, self).save(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), max_length=255, unique=True)
    username = models.CharField(_('username'), max_length=50, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(_('date_joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    last_login = models.DateTimeField(_('last_login'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(User, self).save(*args, **kwargs)


class Otp(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    otp = models.CharField(max_length=4)
    otp_expiration = models.DateTimeField()
    otp_tries = models.PositiveSmallIntegerField(default=settings.MAX_OTP_TRY)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(Otp, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, models.CASCADE, related_name='profile')
    email = models.OneToOneField(Email, models.CASCADE, related_name='profile')
    reserve_email = models.OneToOneField(Email, models.SET_NULL, null=True, blank=True, related_name='profile_reserve')

    SEX_CHOICES = {
        'W': _('profile_woman_sex'),
        'M': _('profile_man_sex')
    }

    # name = models.CharField(_('profile_name'), max_length=30, null=True)
    # lastname = models.CharField(_('profile_lastname'), max_length=30, null=True)
    # fathername = models.CharField(_('profile_fathername'), max_length=30, null=True, blank=True)
    # sex = models.CharField(_('profile_sex'), max_length=1, null=True, blank=True)
    # birthdate = models.DateField(_('profile_birth'), null=True)
    # city = models.CharField(_('profile_city'), max_length=100, null=True, blank='True')
    # phone_number = models.CharField(_('profile_phone_number'))

    def __str__(self):
        return self.email.email
