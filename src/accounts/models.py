from os.path import splitext

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone

from model_utils import Choices

from notifications.constants import NOTIFICATION_SETTINGS_FREQUENCIES_LIST
from notifications.models import Notification


class UserQueryset(models.QuerySet):
    """Custom queryset with additional filtering methods for users."""

    def contributors(self):
        """Only return users who are contributors."""

        return self.filter(is_contributor=True)

    def beneficiaries(self):
        """Only return users who are beneficiaries."""

        return self.filter(is_beneficiary=True)

    def search_page_admins(self):
        """Only return users who are search page administrators."""

        return self.filter(search_pages__isnull=False)

    def animators(self):
        """Only return users who are animators."""

        return self.filter(animator_perimeter__isnull=False)

    def with_api_token(self):
        """Only return users with an API Token."""

        return self.filter(auth_token__isnull=False)


class UserManager(BaseUserManager):
    """Custom manager for our custom User model."""

    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)

    def _create_user(self, email, first_name, last_name, password, **extra_fields):
        """Create and save the user object."""

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """Creates a simple user."""

        extra_fields["is_superuser"] = False
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """Creates a superuser."""

        extra_fields["is_superuser"] = True
        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def contributors(self):
        """Only return users who are contributors."""

        return self.get_queryset().contributors()

    def beneficiaries(self):
        """Only return users who are beneficiaries."""

        return self.get_queryset().beneficiaries()

    def search_page_admins(self):
        """Only return users who are search page administrators."""

        return self.get_queryset().search_page_admins()

    def animators(self):
        """Only return users who are animators."""

        return self.get_queryset().animators()

    def with_api_token(self):
        """Only return users with an API Token."""

        return self.get_queryset().with_api_token()


def logo_upload_to(instance, filename):
    """Rename uploaded files with the object's slug."""

    _, extension = splitext(filename)
    name = instance.pk
    filename = "accounts/{}_logo{}".format(name, extension)
    return filename


class User(AbstractBaseUser, PermissionsMixin):
    """Represents a single user account (one physical person)."""

    FUNCTION_TYPE = Choices(
        ("mayor", "Maire"),
        ("deputy_mayor", "Adjoint au maire"),
        ("municipal_councilor", "Conseiller municipal"),
        ("elected", "Élu"),
        ("town_clerk", "Secrétaire de mairie"),
        ("agent", "Agent territorial"),
        ("other", "Autre"),
    )

    ACQUISITION_CHANNEL_CHOICES = Choices(
        ("webinar", "Webinaire"),
        ("animator", "Animateur local"),
        ("trade_press", "Presse spécialisée"),
        ("word_of_mouth", "Bouche-à-oreille"),
        ("invited", "Invitation à collaborer"),
        ("other", "Autre"),
    )

    objects = UserManager()

    email = models.EmailField("Adresse e-mail", unique=True)
    first_name = models.CharField("Prénom", max_length=256)
    last_name = models.CharField("Nom", max_length=256)
    image = models.FileField(
        "Avatar de l’utilisateur",
        null=True,
        blank=True,
        upload_to=logo_upload_to,
        help_text="Assurez vous que l’image n’est pas trop lourde.",
    )

    # Account settings fields
    ml_consent = models.BooleanField(
        "A donné son consentement pour recevoir l’actualité", default=False
    )

    # Contributors related data
    contributor_organization = models.CharField(
        "Organisme (ancien champ)", max_length=128, blank=True
    )
    contributor_role = models.CharField(
        "Rôle (ancien champ)", max_length=128, blank=True
    )
    contributor_contact_phone = models.CharField(
        "Numéro de téléphone", max_length=35, blank=True
    )
    is_certified = models.BooleanField(
        "Certifié ?",
        help_text="Afficher un badge à côté des aides publiées par ce compte.",
        default=False,
    )

    # Beneficiaries related data
    beneficiary_organization = models.ForeignKey(
        "organizations.Organization",
        verbose_name="Structure du bénéficiaire",
        on_delete=models.PROTECT,
        help_text="A quelle structure appartient le bénéficiaire ?",
        null=True,
        blank=True,
    )
    beneficiary_function = models.CharField(
        "Fonction du bénéficiaire",
        max_length=32,
        choices=FUNCTION_TYPE,
        null=True,
        blank=True,
    )
    beneficiary_role = models.CharField(
        "Rôle du bénéficiaire", max_length=128, blank=True
    )

    proposed_organization = models.ForeignKey(
        "organizations.Organization",
        related_name="invited_user",
        verbose_name="Structure proposée",
        on_delete=models.SET_NULL,
        help_text="L’utilisateur a reçu une proposition pour rejoindre cette structure",
        null=True,
        blank=True,
    )
    invitation_author = models.ForeignKey(
        "accounts.User",
        related_name="invited_user",
        verbose_name="Auteur de l’invitation",
        on_delete=models.SET_NULL,
        help_text="utilisateur qui a invité cet utilisateur a rejoindre sa structure",
        null=True,
        blank=True,
    )
    invitation_date = models.DateTimeField(
        "Date de l’invitation", null=True, blank=True
    )
    join_organization_date = models.DateTimeField(
        "Date d’acceptation de l’invitation", null=True, blank=True
    )

    # Roles
    is_contributor = models.BooleanField(
        "Contributeur ?",
        help_text="Peut accéder à un espace pour créer et modifier ses aides.",
        default=True,
    )
    is_beneficiary = models.BooleanField(
        "Bénéficiaire ?",
        help_text="Peut accéder à un espace pour créer et modifier ses projets.",
        default=True,
    )
    animator_perimeter = models.ForeignKey(
        "geofr.Perimeter",
        verbose_name="Périmètre d’animation",
        on_delete=models.PROTECT,
        related_name="animators",
        help_text="Sur quel périmètre l’animateur local est-il responsable ?",
        null=True,
        blank=True,
    )
    acquisition_channel = models.CharField(
        "Canal d’acquisition",
        max_length=32,
        choices=ACQUISITION_CHANNEL_CHOICES,
        null=True,
        blank=True,
        help_text="Comment l’utilisateur a-t-il connu Aides-territoires?",
    )
    acquisition_channel_comment = models.CharField(
        "Commentaire Canal d’acquisition",
        max_length=1000,
        null=True,
        blank=True,
        help_text="Comment l’utilisateur a-t-il connu Aides-territoires (champ libre)?",
    )

    # Notification settings
    notification_counter = models.PositiveIntegerField(
        "Nombre de notifications reçues", default=0
    )
    notification_email_frequency = models.CharField(
        "Fréquence d’envoi des emails de notifications",
        max_length=32,
        choices=NOTIFICATION_SETTINGS_FREQUENCIES_LIST,
        default="daily",
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["id"]

    def __str__(self):
        return "{} ({})".format(self.full_name, self.email)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self):
        """Only the admin users can access the admin site."""
        return self.is_superuser or self.is_administrator_of_search_pages

    @property
    def is_contributor_or_staff_or_beneficiary(self):
        """Only the contributors or the admin users can access
        certain pages of the app."""
        return self.is_contributor or self.is_superuser or self.is_beneficiary

    @property
    def is_contributor_or_staff(self):
        """Only the contributors or the admin users can access
        certain pages of the app."""
        return self.is_contributor or self.is_superuser

    @property
    def is_contributor_or_beneficiary(self):
        """User has to choose if he is a contributor or/and
        beneficiary"""
        return self.is_contributor or self.is_beneficiary

    @property
    def unread_notifications(self):
        """Number of unread notifications for the user"""
        return Notification.objects.filter(
            recipient=self, date_read__isnull=True
        ).count()

    @property
    def bound_to_organization(self):
        """User need to specify more personal data."""
        return self.beneficiary_organization

    @property
    def profile_complete(self):
        """User need to specify more personal data."""
        return self.password and self.is_contributor_or_beneficiary

    @property
    def is_administrator_of_search_pages(self):
        """Only the minisite administrators can access
        certain pages of the app."""
        return self.search_pages.exists()

    def send_notification(self, title: str, message: str) -> None:
        """
        Send a notification to the user through the internal notification system
        """
        # Message should be valid html with content enclosed in one or several p tag(s)
        # Though if the message is very basic, we can add it here.
        if "<p>" not in message:
            message = f"<p>{message}</p>"

        Notification.objects.create(recipient=self, title=title, message=message)
        self.notification_counter += 1
        self.save()

    def get_search_preferences(self):
        """
        Returns the perimeter and organization type of the user to pre-fill the search forms
        """

        preferences_string = "?"
        preferences = {"targeted_audiences": None, "perimeter": None}
        organization = self.beneficiary_organization
        if organization is not None:
            preferences["targeted_audiences"] = organization.organization_type[0]
            preferences_string += (
                f'targeted_audiences={preferences["targeted_audiences"]}'
            )
            if organization.perimeter is not None:
                preferences["perimeter"] = organization.perimeter_id
                preferences_string += f'&perimeter={preferences["perimeter"]}'
        preferences["base_search_string"] = preferences_string
        return preferences


class UserLastConnexion(models.Model):
    user = models.ForeignKey(
        "accounts.User", verbose_name="Utilisateur", on_delete=models.CASCADE, null=True
    )
    last_connexion = models.DateTimeField(
        "Date de la dernière connexion", default=timezone.now
    )

    class Meta:
        verbose_name = "Dernière connexion de l’utilisateur"
        verbose_name_plural = "Dernières connexions des utilisateurs"
