from django.db import models
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class NotificationGroup(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=255)
    slug = models.SlugField(default="")

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Notification group")
        verbose_name_plural = _("Notification groups")
