from datetime import datetime, timedelta
import string
import random as random
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

from .models import Otp


def create_otp():
    chars = string.digits
    rand = ''.join(random.choice(chars) for _ in range(4))
    expiration = datetime.now() + timedelta(minutes=10)
    return rand, expiration


def send_otp(request, mail, otp):
    link = ''
    subject = ''
    # message = (_(f'{otp}\n\n') +
    #            _(f'{link}'))
    message = render_to_string('users/template_otp.html', {
        'domain': settings.SITE_DOMAIN,
        'email': urlsafe_base64_encode(force_bytes(mail)),
        'code': urlsafe_base64_encode(force_bytes(otp)),
        'protocol': 'https' if request.is_secure() else 'http',
        'otp': otp,
    })
    send_mail(
        subject,
        message,
        'admin@admin.admin',
        [mail]
    )


def clean_otp_db():
    num = random.randint(0, 99)
    if num > 90:
        Otp.objects.filter(otp_expiration__lt=datetime.now() - timedelta(minutes=60)).delete()
