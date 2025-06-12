from django.db import models
from django.utils.translation import gettext as _


class Trainer(models.Model):
    name = models.CharField(_("name"), max_length=255)
    location = models.CharField(_("location"), max_length=255)
    email = models.EmailField(
        _("email"),
    )
    subjects = models.JSONField(
        verbose_name=_("subject"),
        max_length=255,
        help_text=_("Type each subjects separated with a comma"),
    )

    class Meta:
        verbose_name = _("Trainer")
        verbose_name_plural = _("Trainers")
        ordering = ["name", "subjects"]

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(_("name"), max_length=255)
    location = models.CharField(_("location"), max_length=255)
    participants = models.PositiveIntegerField(_("participants"), default=1)
    date_scheduled = models.DateField(_("date"))
    notes = models.TextField(_("notes"), blank=True)
    trainer = models.ForeignKey(
        Trainer,
        verbose_name=_("trainer"),
        related_name="courses",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    price = models.PositiveBigIntegerField(_("price"), default=0)
    trainer_price = models.PositiveBigIntegerField(_("trainer price"), default=0)
    subject = models.CharField(verbose_name=_("subject"), max_length=255)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ["name", "subject"]

    def save(self, **kwargs):
        self.location = self.location.capitalize()
        return super().save(**kwargs)

    def __str__(self):
        return self.name
