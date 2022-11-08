from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import password_validation
from core.forms.baseform import AidesTerrBaseForm
from core.forms.fields import AutocompleteModelChoiceField

from model_utils import Choices

from accounts.models import User
from accounts.utils import check_current_password
from projects.models import Project
from geofr.models import Perimeter


class RegisterForm(UserCreationForm, AidesTerrBaseForm):
    """Form used to create new user accounts."""

    ORGANIZATION_TYPE = Choices(
        ("farmer", "Agriculteur"),
        ("association", "Association"),
        ("special", "Collectivité d’outre-mer à statuts particuliers"),
        ("commune", "Commune"),
        ("department", "Département"),
        ("private_sector", "Entreprise privée"),
        ("public_cies", "Entreprise publique locale (Sem, Spl, SemOp)"),
        ("epci", "Intercommunalité / Pays"),
        (
            "public_org",
            "Établissement public (école, bibliothèque…) / Service de l’État",
        ),
        ("private_person", "Particulier"),
        ("region", "Région"),
        ("researcher", "Recherche"),
    )

    first_name = forms.CharField(label="Votre prénom", required=True)
    last_name = forms.CharField(label="Votre nom", required=True)
    email = forms.EmailField(
        label="Votre adresse e-mail",
        required=True,
        help_text="""
            Par exemple : prenom.nom@domaine.fr<br />
            Nous enverrons un e-mail de confirmation à cette adresse avant de valider le compte.
            """,
        error_messages={
            "invalid": "Saisissez une adresse e-mail valide, par exemple prenom.nom@domaine.fr."
        },
    )
    beneficiary_role = forms.CharField(
        label="Votre rôle", max_length=128, required=False
    )
    beneficiary_function = forms.ChoiceField(
        label="Votre fonction", required=False, choices=User.FUNCTION_TYPE
    )
    is_contributor = forms.BooleanField(label="Publier des aides", required=False)
    is_beneficiary = forms.BooleanField(label="Trouver des aides", required=False)
    organization_name = forms.CharField(label="Nom de votre structure", required=True)
    organization_type = forms.ChoiceField(
        label="Vous êtes un/une", required=True, choices=ORGANIZATION_TYPE
    )
    perimeter = AutocompleteModelChoiceField(
        label="Votre territoire", queryset=Perimeter.objects.all(), required=True
    )

    acquisition_channel = forms.ChoiceField(
        required=True, choices=sorted(User.ACQUISITION_CHANNEL, key=lambda x: x[1])
    )

    acquisition_channel_comment = forms.CharField(
        label="Précisez comment vous avez connu Aides-territoires", required=False
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "beneficiary_role",
            "beneficiary_function",
            "is_contributor",
            "is_beneficiary",
            "organization_name",
            "organization_type",
            "perimeter",
            "acquisition_channel",
            "acquisition_channel_comment",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"autocomplete": "given-name"})
        self.fields["last_name"].widget.attrs.update({"autocomplete": "family-name"})
        self.fields["email"].widget.attrs.update(
            {
                "placeholder": "Merci de bien vérifier l’adresse saisie.",
                "autofocus": False,
                "autocomplete": "email",
            }
        )
        self.fields["password1"].widget.attrs.update({"autocomplete": "new-password"})
        self.fields["password2"].widget.attrs.update({"autocomplete": "new-password"})

        if len(self.errors):
            self.set_autofocus_on_first_error()
        else:
            self.fields["first_name"].widget.attrs.update({"autofocus": True})

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email.lower()

    def clean(self):
        """Validation routine (frontend form only)."""

        data = super().clean()

        if not any((data.get("is_contributor"), data.get("is_beneficiary"))):
            msg = "Merci de cocher au moins une des options."
            self.add_error("is_beneficiary", msg)
            self.add_error("is_contributor", msg)

        if not data.get("organization_type"):
            msg = "Merci de sélectionner une option."
            self.add_error("organization_type", msg)

        if not data.get("acquisition_channel"):
            msg = "Merci de sélectionner une option."
            self.add_error("acquisition_channel", msg)

        return data


class RegisterCommuneForm(RegisterForm):
    email = forms.EmailField(
        label="Votre adresse e-mail",
        required=True,
        help_text="""
            Par exemple : prenom.nom@domaine.fr<br />
            Vous pouvez modifier l’email de contact s’il n’est pas exact
            ou si vous souhaitez en utiliser un autre, personnel par exemple.<br />
            Nous enverrons un e-mail de confirmation à cette adresse avant de valider le compte.
            """,
        error_messages={
            "invalid": "Saisissez une adresse e-mail valide, par exemple prenom.nom@domaine.fr."
        },
    )
    perimeter = AutocompleteModelChoiceField(
        label="Votre commune", queryset=Perimeter.objects.all(), required=True
    )


class LoginForm(AuthenticationForm, AidesTerrBaseForm):
    error_messages = {
        "invalid_login": "Saisissez une adresse e-mail et un mot de passe valides.",
        "inactive": "Ce compte n’est actuellement pas actif.",
    }

    username = forms.EmailField(
        label="Votre adresse e-mail",
        help_text="Par exemple : prenom.nom@domaine.fr",
        required=True,
        error_messages={
            "invalid": "Saisissez une adresse e-mail valide, par exemple prenom.nom@domaine.fr."
        },
    )
    password = forms.CharField(
        label="Votre mot de passe",
        required=True,
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean_username(self):
        """Don't prevent users to login when they enter uppercase emails."""

        username = self.cleaned_data["username"]
        return username.lower()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"autocomplete": "email"})
        self.fields["password"].widget.attrs.update(
            {"autocomplete": "current-password"}
        )


class PasswordResetForm(AidesTerrBaseForm):
    """Password reset request form."""

    username = forms.EmailField(
        label="Votre adresse e-mail",
        help_text="Par exemple : prenom.nom@domaine.fr",
        required=True,
        error_messages={
            "invalid": "Saisissez une adresse e-mail valide, par exemple prenom.nom@domaine.fr."
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({"autocomplete": "email"})


class PasswordResetConfirmForm(forms.ModelForm, AidesTerrBaseForm):
    """Change password after reset request form."""

    new_password = forms.CharField(
        label="Choisissez un nouveau mot de passe",
        required=True,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(),
    )

    new_password2 = forms.CharField(
        label="Saisissez à nouveau le nouveau mot de passe",
        required=True,
        strip=False,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = [
            "new_password",
            "new_password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["new_password"].widget.attrs.update(
            {"autocomplete": "new-password"}
        )
        self.fields["new_password2"].widget.attrs.update(
            {"autocomplete": "new-password"}
        )

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data by super().
        password = self.cleaned_data.get("new_password")
        password2 = self.cleaned_data.get("new_password2")

        if password and password == password2:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("new_password", error)
        elif password != password2:
            self.add_error("new_password", "Les mots de passe ne sont pas identiques")

    def save(self, commit=True):
        user = super().save(commit=False)

        new_password = self.cleaned_data["new_password"]
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()
        return user


class ContributorProfileForm(forms.ModelForm, AidesTerrBaseForm):
    """Edit contributor profile related user data."""

    is_contributor = forms.BooleanField(label="Publier des aides", required=False)
    is_beneficiary = forms.BooleanField(label="Trouver des aides", required=False)

    new_password = forms.CharField(
        label="Choisissez un nouveau mot de passe",
        required=False,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Laissez vide pour conserver votre mot de passe actuel"
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Saisissez à nouveau le nouveau mot de passe",
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Laissez vide pour conserver votre mot de passe actuel"
            }
        ),
    )

    current_password = forms.CharField(
        label="Entrez votre mot de passe actuel",
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "À remplir en cas de changement de mot de passe"}
        ),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "is_contributor",
            "is_beneficiary",
            "beneficiary_function",
            "beneficiary_role",
            "new_password",
            "new_password2",
            "current_password",
        ]
        labels = {
            "first_name": "Votre prénom",
            "last_name": "Votre nom",
            "email": "Votre adresse email",
            "beneficiary_function": "Vous êtes",
            "beneficiary_role": "Votre fonction",
        }

    def clean(self):
        """Validation routine (frontend form only)."""

        data = super().clean()

        if not any((data.get("is_contributor"), data.get("is_beneficiary"))):
            msg = "Merci de cocher au moins une des options."
            self.add_error("is_beneficiary", msg)
            self.add_error("is_contributor", msg)

        return data

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data by super().
        password = self.cleaned_data.get("new_password")
        password2 = self.cleaned_data.get("new_password2")

        if password and password == password2:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("new_password", error)

            # if new_password is set, we also need to check the current_password
            current_password = self.cleaned_data.get("current_password")
            try:
                self.current_password_checked = check_current_password(
                    current_password, self.instance.password
                )
            except forms.ValidationError as error:
                self.add_error("current_password", error)
                self.current_password_checked = False
        elif password != password2:
            self.add_error("new_password", "Les mots de passe ne sont pas identiques")

    def save(self, commit=True):
        user = super().save(commit=False)

        new_password = self.cleaned_data["new_password"]
        if new_password and self.current_password_checked:
            user.set_password(new_password)

        if commit:
            user.save()
        return user


class InviteCollaboratorForm(AidesTerrBaseForm):
    """Form used to allow user to invite new collaborator."""

    first_name = forms.CharField(label="Son prénom", required=True)
    last_name = forms.CharField(label="Son nom", required=True)
    email = forms.EmailField(
        label="Son adresse e-mail",
        help_text="Par exemple : prenom.nom@domaine.fr",
        required=True,
        error_messages={
            "invalid": "Saisissez une adresse e-mail valide, par exemple prenom.nom@domaine.fr."
        },
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(InviteCollaboratorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "fr-input"

    def clean_email(self):
        email = self.cleaned_data["email"]

        if self.data.get("email"):
            try:
                User.objects.get(email=self.data.get("email"))
                current_organization = User.objects.get(
                    email=self.data.get("email")
                ).beneficiary_organization
                proposed_organization = self.request.user.beneficiary_organization
                if (
                    User.objects.get(email=self.data.get("email")).proposed_organization
                    is not None
                ):
                    msg = "Cet utilisateur ne peut être invité car il a déjà une invitation en attente."  # noqa
                    self.add_error("email", msg)
                elif proposed_organization == current_organization:
                    msg = "Cet utilisateur est déjà un de vos collaborateurs."
                    self.add_error("email", msg)
            except Exception:
                return email.lower()

        return email.lower()


class JoinOrganizationForm(AidesTerrBaseForm):
    """Form used to allow user to join an other organization."""

    collaborators = forms.ModelMultipleChoiceField(
        label="Collaborateurs à inviter",
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    projects = forms.ModelMultipleChoiceField(
        label="Projets à transférer",
        queryset=Project.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(JoinOrganizationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "fr-input"

    def clean(self):
        """Validation routine (frontend form only)."""
        data = super().clean()
        return data


class CompleteProfileForm(forms.ModelForm, AidesTerrBaseForm):
    """Edit user profile."""

    first_name = forms.CharField(label="Votre prénom", required=True)
    last_name = forms.CharField(label="Votre nom", required=True)
    is_contributor = forms.BooleanField(label="Publier des aides", required=False)
    is_beneficiary = forms.BooleanField(label="Trouver des aides", required=False)

    new_password = forms.CharField(
        label="Choisissez un mot de passe",
        required=True,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(),
    )

    new_password2 = forms.CharField(
        label="Saisissez à nouveau votre mot de passe",
        required=True,
        strip=False,
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "is_contributor",
            "is_beneficiary",
            "beneficiary_function",
            "beneficiary_role",
            "new_password",
            "new_password2",
        ]
        labels = {
            "beneficiary_function": "Vous êtes",
            "beneficiary_role": "Votre fonction",
        }

    def __init__(self, *args, **kwargs):
        super(CompleteProfileForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            if field_name == "beneficiary_function":
                field = self.fields.get("beneficiary_function")
                field.choices[0] = ("", "Selectionnez une option")
                field.widget.choices = field.choices

    def clean(self):
        """Validation routine (frontend form only)."""

        data = super().clean()

        if not any((data.get("is_contributor"), data.get("is_beneficiary"))):
            msg = "Merci de cocher au moins une des options."
            self.add_error("is_beneficiary", msg)
            self.add_error("is_contributor", msg)

        return data

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data by super().
        password = self.cleaned_data.get("new_password")
        password2 = self.cleaned_data.get("new_password2")
        if password and password == password2:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("new_password", error)
        elif password != password2:
            self.add_error("new_password", "Les mots de passe ne sont pas identiques")

    def save(self, commit=True):
        user = super().save(commit=False)

        new_password = self.cleaned_data["new_password"]
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()
        return user
