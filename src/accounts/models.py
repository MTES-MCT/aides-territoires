from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Custom manager for our custom User model."""

    def _create_user(self, email, full_name, password, **extra_fields):
        """Create and save the user object."""

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, full_name, password=None, **extra_fields):
        """Creates a simple user."""

        extra_fields['is_superuser'] = False
        return self._create_user(email, full_name, password, **extra_fields)

    def create_superuser(self, email, full_name, password, **extra_fields):
        """Creates a superuser."""

        extra_fields['is_superuser'] = True
        return self._create_user(email, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Represents a single user account (one physical person)."""

    objects = UserManager()

    email = models.EmailField(
        _('Email address'),
        unique=True)
    full_name = models.CharField(
        _('Full name'),
        max_length=256)
    date_joined = models.DateTimeField(
        _('Date joined'),
        default=timezone.now)

    ##
    # Contributors related data
    ##
    organization = models.CharField(
        _('Organization'),
        max_length=128,
        blank=True)
    role = models.CharField(
        _('Role'),
        max_length=128,
        blank=True)
    contact_phone = models.CharField(
        _('Contact phone number'),
        max_length=20,
        blank=True)
    is_certified = models.BooleanField(
        _('Is certified'),
        default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return '{} ({})'.format(self.full_name, self.email)

    @property
    def is_staff(self):
        """Only the admin user can access the admin site."""
        return self.is_superuser

    @property
    def is_contributor(self):
        """Contributors need to specify more personal data."""
        return self.organization and self.role and self.contact_phone
