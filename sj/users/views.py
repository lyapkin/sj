import random

from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone

from .models import Otp
from .serializers import OtpSerializer, UserSerializer
from .utils import create_otp, send_otp, clean_otp_db
from django.contrib.auth import authenticate, login, logout
from cart.serializers import CartSerializer
from cart.models import Cart


@api_view(['POST'])
def get_code(request, *args, **kwargs):
    clean_otp_db()
    otp = Otp.objects.filter(email=request.data['email'].lower()).first()
    if otp:
        otp.otp, otp.otp_expiration = create_otp()
        otp.save()
        send_otp(request, otp.email, otp.otp)
        return Response(OtpSerializer(otp).data, status=200)
    serializer = OtpSerializer(data={'email': request.data['email']}, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def confirm(request, *args, **kwargs):
    code = request.data['code']
    email = request.data['email'].lower()
    otp = Otp.objects.filter(email=email).first()

    if not otp:
        return Response({"error": _("code_not_exist"), "recode": True}, status=401)

    if otp.otp_expiration < timezone.now():
        otp.delete()
        return Response({"error": _("code_expiration"), "recode": True}, status=401)

    user = authenticate(request, email=email, code=code)
    if user is None:
        otp.otp_tries = otp.otp_tries - 1 if otp.otp_tries > 0 else 0
        if otp.otp_tries > 0:
            otp.save()
            return Response({"error": _("no_user"), "recode": False}, status=401)
        otp.delete()
        return Response({"error": _("tries_lack"), "recode": True}, status=401)

    login(request, user)
    otp.delete()
    return Response({**UserSerializer(request.user).data, 'cart': CartSerializer(Cart.objects.filter(user=request.user), many=True).data}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout_view(request, *args, **kwargs):
    logout(request)
    return Response({"success": _('logout_success')}, status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def check_auth(request, *args, **kwargs):
    # print(Cart.objects.filter(request.user))
    return Response({**UserSerializer(request.user).data, 'cart': CartSerializer(Cart.objects.filter(user=request.user), many=True).data}, status=200)
