from django import forms

from dsfr.forms import DsfrBaseForm

from accounts.models import User
from bookmarks.models import Bookmark


class BaseBookmarkForm(DsfrBaseForm):
    """Commont fields for both bookmark forms."""

    title = forms.CharField(
        label="Donnez un nom à votre alerte", required=True, max_length=250
    )
    alert_frequency = forms.ChoiceField(
        label="Fréquence de l’alerte",
        choices=Bookmark.FREQUENCIES,
        help_text="À quelle fréquence souhaitez-vous recevoir les nouveaux résultats ?",
    )
    querystring = forms.CharField(widget=forms.HiddenInput)


class UserBookmarkForm(BaseBookmarkForm):
    """Form used to configure a new search bookmark (user connected only)."""

    send_email_alert = forms.BooleanField(
        label="Recevoir les nouveaux résultats par e-mail", required=False
    )


class AnonymousBookmarkForm(BaseBookmarkForm):
    """Configure new search bookmarks (anonymous users only)."""

    email = forms.EmailField(
        label="Votre adresse e-mail",
        help_text="Nous enverrons un e-mail pour confirmer votre adresse",
        required=True,
    )

    def clean_email(self):
        """Make sure the email is not linked to an existing account.

        If it's linked to an account, make sure it's a new account,
        meaning it was never use to log in.
        """

        email = self.cleaned_data["email"]
        user_exists = (
            User.objects.filter(email=email).filter(last_login__isnull=False).exists()
        )
        if user_exists:
            msg = "Un compte avec cette adresse existe déjà. Avez-vous oublié de vous connecter ?"
            raise forms.ValidationError(msg, code="unique")
        return email


class BookmarkAlertForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ["send_email_alert", "alert_frequency"]
