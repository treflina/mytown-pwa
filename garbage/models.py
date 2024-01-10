from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField

from .validators import FileValidator

CONTENT_TYPES = ("application/pdf",)


def get_today():
    return date.today()


class Region(models.Model):
    validate_file = FileValidator(max_size=1024 * 1000, content_types=CONTENT_TYPES)

    name = models.CharField(_("Region"), max_length=255)
    number = models.PositiveSmallIntegerField(_("Region's number"), unique=True)
    schedule = models.FileField(upload_to="schedules/", null=True, blank=True)

    class Meta:  # noqa
        ordering = ["number"]
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return self.name


class GarbageType(models.Model):
    name = models.CharField(_("Garbage Type"), max_length=255)
    # TODO REMOVE BLANK
    number = models.PositiveIntegerField(
        _("Number (ordering)"), unique=True, null=True, blank=True
    )
    color = ColorField(default="#000000")
    # image = models.ImageField(_("Image"), blank=True, null=True)

    def __str__(self):
        return self.name


class GarbageCollection(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    garbage_type = models.ForeignKey(GarbageType, on_delete=models.CASCADE)
    date = models.DateField()

    @property
    def get_days_count(self):
        return (self.date - get_today()).days

    def __str__(self):
        return f"{self.date} - {self.region} - {self.garbage_type}"
