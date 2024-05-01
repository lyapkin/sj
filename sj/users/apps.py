from django.apps import AppConfig
from django.db.models.signals import post_delete


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from .signals import delete_profile
        from .models import Profile
        post_delete.connect(
            delete_profile.clean_profile_deletion,
            sender=Profile,
            weak=False,
            dispatch_uid='delete_email'
        )