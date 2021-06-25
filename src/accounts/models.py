from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserQueryset(models.QuerySet):
    """Custom queryset with additional filtering methods for users."""

    def is_administrator_of_search_pages(self):
        """Only return users who are search page administrators."""

        return self.filter(search_pages__isnull=False)

    def with_api_token(self):
        """Only return users with an API Token."""

        return self.filter(auth_token__isnull=False)


class UserManager(BaseUserManager):
    """Custom manager for our custom User model."""

    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)

    def _create_user(self, email, first_name, last_name, password,
                     **extra_fields):
        """Create and save the user object."""

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None,
                    **extra_fields):
        """Creates a simple user."""

        extra_fields['is_superuser'] = False
        return self._create_user(email, first_name, last_name, password,
                                 **extra_fields)

    def create_superuser(self, email, first_name, last_name, password,
                         **extra_fields):
        """Creates a superuser."""

        extra_fields['is_superuser'] = True
        return self._create_user(email, first_name, last_name, password,
                                 **extra_fields)

    def is_administrator_of_search_pages(self):
        """Only return users who are search page administrators."""

        return self.get_queryset().is_administrator_of_search_pages()

    def with_api_token(self):
        """Only return users with an API Token."""

        return self.get_queryset().with_api_token()


class User(AbstractBaseUser, PermissionsMixin):
    """Represents a single user account (one physical person)."""

    objects = UserManager()

    email = models.EmailField(
        _('Email address'),
        unique=True)
    first_name = models.CharField(
        _('First name'),
        max_length=256)
    last_name = models.CharField(
        _('Last name'),
        max_length=256)
    date_joined = models.DateTimeField(
        _('Date joined'),
        default=timezone.now)

    ##
    # Account settings fields
    ##
    ml_consent = models.BooleanField(
        _('Gave consent to receive communications'),
        default=False)
    similar_aids_alert = models.BooleanField(
        _('Wants to receive alerts when similar aids are published'),
        default=False)

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
        max_length=35,
        blank=True)
    is_contributor = models.BooleanField(
        _('Is contributor'),
        help_text=_('Can access a dashboard to create aids'),
        default=True)
    is_certified = models.BooleanField(
        _('Is certified'),
        help_text=_('Display a badge next to this user\'s aids'),
        default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return '{} ({})'.format(self.full_name, self.email)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_staff(self):
        """Only the admin users can access the admin site."""
        return self.is_superuser or self.is_administrator_of_search_pages

    @property
    def is_contributor_or_staff(self):
        """Only the contributors or the admin users can access
        certain pages of the app."""
        return self.is_contributor or self.is_superuser

    @property
    def profile_complete(self):
        """Contributors need to specify more personal data."""
        return self.organization and self.role and self.contact_phone

    @property
    def is_administrator_of_search_pages(self):
        """Only the minisite administrators can access
        certain pages of the app."""
        return self.search_pages.exists()
