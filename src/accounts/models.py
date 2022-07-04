from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save


class MyAccountManager(BaseUserManager):

    def create_user(self, email,
                    username, password, first_name, last_name):
        validations = [
            (email, 'un correo electrónico'),
            (username, 'un nombre de usuario'),
            (first_name, 'uno o más nombres'),
            (last_name, 'uno o más apellidos'), ]

        # VALIDATE REQUIRE USER FIELDS
        for param, spec in validations:
            if not param:
                raise ValueError(f'Los usuarios deben tener {spec}.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,
                         username, password, first_name, last_name):

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def profile_pic_upload_location(instance, filename, *args, **kwargs):
    account_id = str(instance.id)
    return f'account/{account_id}/profile_{account_id}_{filename}'


class Account(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name="email",
                              max_length=100, unique=True, null=False)
    username = models.CharField(max_length=40, unique=True, null=False)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        verbose_name="profile picture",
        upload_to=profile_pic_upload_location,
        blank=True, null=True)
    first_name = models.CharField(verbose_name="first name", max_length=30)
    last_name = models.CharField(verbose_name="last name", max_length=30)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ['is_active', '-username']


@receiver(post_delete, sender=Account)
def submission_delete(sender, instance, **kwargs):
    instance.profile_picture.delete(False)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        if instance.is_superuser:
            instance.role = 'admin'
            instance.save()
