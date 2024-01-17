from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, JSONField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ctim.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Cyber Threat Intelligence Management.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore
    # CTIM specific user fields
    business_role = CharField(_("Business Role"), max_length=255, blank=True, null=True)
    company = CharField(_("Company"), max_length=255, blank=True, null=True)
    industry = CharField(_("Industry"), max_length=255, blank=True, null=True)
    interests = JSONField(_("Interests"), default=dict, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
