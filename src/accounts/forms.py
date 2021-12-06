from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import password_validation

from model_utils import Choices

from accounts.models import User


class RegisterForm(UserCreationForm):
    """Form used to create new user accounts."""

    ORGANIZATION_TYPE = Choices(
        ('farmer', 'Agriculteur'),
        ('association', 'Association'),
        ('special', "Collectivité d'outre-mer à statuts particuliers"),
        ('commune', 'Commune'),
        ('department', 'Département'),
        ('private_sector', 'Entreprise privée'),
        ('public_cies', "Entreprise publique locale (Sem, Spl, SemOp)"),
        ('epci', 'EPCI à fiscalité propre'),
        ('public_org', "Établissement public (école, bibliothèque…) / Service de l'État"),
        ('private_person', 'Particulier'),
        ('region', 'Région'),
        ('researcher', 'Recherche'),
    )

    first_name = forms.CharField(
        label='Votre prénom',
        required=True)
    last_name = forms.CharField(
        label='Votre nom',
        required=True)
    email = forms.EmailField(
        label='Votre adresse e-mail',
        required=True,
        help_text="Nous enverrons un e-mail de confirmation à cette adresse avant de valider le compte.")  # noqa
    beneficiary_role = forms.CharField(
        label='Votre rôle',
        max_length=128,
        required=False)
    beneficiary_function = forms.ChoiceField(
        label="Votre fonction",
        required=False,
        choices=User.FUNCTION_TYPE)
    is_contributor = forms.BooleanField(
        label='Publier des aides',
        required=False)
    is_beneficiary = forms.BooleanField(
        label='Trouver des aides',
        required=False)
    organization_type = forms.ChoiceField(
        label="Vous êtes un/une",
        required=True,
        choices=ORGANIZATION_TYPE)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'password1', 'password2',
            'beneficiary_role', 'beneficiary_function', 'is_contributor',
            'is_beneficiary', 'organization_type'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': True})
        self.fields['email'].widget.attrs.update({
            'placeholder': "Merci de bien vérifier l'adresse saisie."})

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()

    def clean(self):
        """Validation routine (frontend form only)."""

        data = super().clean()

        if not any((data.get('is_contributor'), data.get('is_beneficiary'))):
            msg = "Merci de cocher au moins une des options."
            self.add_error('is_beneficiary', msg)
            self.add_error('is_contributor', msg)

        if not data.get('organization_type'):
            msg = "Merci de sélectionner une option."
            self.add_error('organization_type', msg)

        return data


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Saisissez une adresse e-mail et un mot de passe valides.',
        'inactive': "Ce compte n'est actuellement pas actif.",
    }

    username = forms.EmailField(
        label='Votre adresse e-mail',
        required=True)
    password = forms.CharField(
        label='Votre mot de passe',
        required=True,
        strip=False,
        widget=forms.PasswordInput)

    def clean_username(self):
        """Don't prevent users to login when they user uppercase emails."""

        username = self.cleaned_data['username']
        return username.lower()


class PasswordResetForm(forms.Form):
    """Password reset request form."""

    username = forms.EmailField(
        label='Votre adresse e-mail',
        required=True)


class ContributorProfileForm(forms.ModelForm):
    """Edit contributor profile related user data."""

    is_contributor = forms.BooleanField(
        label='Publier des aides',
        required=False)
    is_beneficiary = forms.BooleanField(
        label='Trouver des aides',
        required=False)

    new_password = forms.CharField(
        label='Choisissez un nouveau mot de passe',
        required=False,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Laissez vide pour conserver votre mot de passe actuel'}))

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'is_contributor', 'is_beneficiary',
            'beneficiary_function', 'beneficiary_role', 'new_password']
        labels = {
            'first_name': 'Votre prénom',
            'last_name': 'Votre nom',
            'email': 'Votre adresse email',
            'beneficiary_function': 'Vous êtes',
            'beneficiary_role': 'Votre fonction',
        }

    def clean(self):
        """Validation routine (frontend form only)."""

        data = super().clean()

        if not any((data.get('is_contributor'), data.get('is_beneficiary'))):
            msg = "Merci de cocher au moins l'une des options."
            self.add_error('is_beneficiary', msg)
            self.add_error('is_contributor', msg)

        return data

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data by super().
        password = self.cleaned_data.get('new_password')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('new_password', error)

    def save(self, commit=True):
        user = super().save(commit=False)

        new_password = self.cleaned_data['new_password']
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()
        return user


class InviteCollaboratorForm(forms.ModelForm):
    """Form used to allow user to invite new collaborator."""

    first_name = forms.CharField(
        label='Son prénom',
        required=True)
    last_name = forms.CharField(
        label='Son nom',
        required=True)
    email = forms.EmailField(
        label='Son adresse e-mail',
        required=True,
        error_messages={'unique': 'Cette adresse email correspond à un utilisateur déjà enregistré sur Aides Territoires.'})  # noqa

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email'
        ]

    def __init__(self, *args, **kwargs):
        super(InviteCollaboratorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'fr-input'

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()


class CompleteProfileForm(forms.ModelForm):
    """Edit user profile."""

    first_name = forms.CharField(
        label='Votre prénom',
        required=True)
    last_name = forms.CharField(
        label='Votre nom',
        required=True)
    is_contributor = forms.BooleanField(
        label='Publier des aides',
        required=False)
    is_beneficiary = forms.BooleanField(
        label='Trouver des aides',
        required=False)

    new_password = forms.CharField(
        label='Choisissez un mot de passe',
        required=True,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        widget=forms.PasswordInput())

    new_password2 = forms.CharField(
        label='Saisissez à nouveau votre mot de passe',
        required=True,
        strip=False,
        widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'is_contributor', 'is_beneficiary',
            'beneficiary_function', 'beneficiary_role',
            'new_password', 'new_password2'
        ]
        labels = {
            'beneficiary_function': 'Vous êtes',
            'beneficiary_role': 'Votre fonction',
        }

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data by super().
        password = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('new_password2')
        if password and password == password2:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('new_password', error)
        elif password != password2:
            self.add_error('new_password', 'Les mots de passe ne sont pas identiques')

    def save(self, commit=True):
        user = super().save(commit=False)

        new_password = self.cleaned_data['new_password']
        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()
        return user
