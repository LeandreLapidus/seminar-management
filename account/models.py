from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
# Create your models here.
class Account(AbstractUser):
    name = models.CharField(_("nom complet"), max_length=255)
    first_name = None
    last_name = None

    REQUIRED_FIELDS = ["name", "email"]

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
    
    def __str__(self):
        return self.full_name or self.username
        