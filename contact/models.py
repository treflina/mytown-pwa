from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.forms import FormBuilder



from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from wagtailcaptcha.forms import WagtailCaptchaFormBuilder
from wagtailcaptcha.models import WagtailCaptchaEmailForm


class CustomFormBuilder(WagtailCaptchaFormBuilder):
    @property
    def formfields(self):
        fields = super(WagtailCaptchaFormBuilder, self).formfields
        fields[self.CAPTCHA_FIELD_NAME] = ReCaptchaField(label="", widget=ReCaptchaV3())
        return fields




class FormField(AbstractFormField):
    page = ParentalKey(
        "ContactPage", on_delete=models.CASCADE, related_name="form_fields"
    )


class ContactPage(WagtailCaptchaEmailForm):
    form_builder = CustomFormBuilder

    intro = RichTextField(verbose_name=_("Page introduction"), blank=True)
    form_intro = RichTextField(verbose_name=_("Form introduction"), blank=True)
    thank_you_text = RichTextField(verbose_name=_("Thank you text"), blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        FieldPanel("form_intro"),
        InlinePanel("form_fields", label=_("Form fields")),
        FieldPanel("thank_you_text"),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Email",
        ),
    ]
