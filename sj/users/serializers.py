from datetime import datetime, timedelta
import random
from django.conf import settings
from rest_framework import serializers

from .models import User, Email, Otp
from .utils import create_otp, send_otp


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ('email',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email'
        )


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ('email',)

    def create(self, validated_data):
        ModelClass = self.Meta.model
        otp, otp_expiration = create_otp()
        instance = ModelClass.objects.create(**validated_data, otp=otp, otp_expiration=otp_expiration)
        # request_save_handlers.order_ready.send(ModelClass, instance=instance, created=True)
        send_otp(self.context.get('request'), instance.email, instance.otp)

        return instance

