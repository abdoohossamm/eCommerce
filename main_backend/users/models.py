from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    created_at = models.DateTimeField(_("joined date"), auto_now_add=True)
    is_seller = models.BooleanField(_("seller status"), default=False)
