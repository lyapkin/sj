from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email.lower())

        user = self.model(email=email, username=username)
        if password:
            user.set_password(password)

        user.is_staff = False
        user.is_superuser = False
        user.is_active = True

        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not email:
            raise ValueError('Superuser must have a password')

        user = self.model(email=self.normalize_email(email.lower()), username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        user.save()
        return user
