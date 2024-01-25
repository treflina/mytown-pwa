from django.db import models
from wagtail.models import Page
from wagtail.documents.models import AbstractDocument, Document
from .utils import convert_bytes, extract_extension


class HomePage(Page):
    template = "index.html"

    content_panels = Page.content_panels


class CustomDocument(AbstractDocument):
    @property
    def get_extension(self):
        return extract_extension(self.file)

    @property
    def get_size(self):
        return convert_bytes(self.file_size)

    admin_form_fields = Document.admin_form_fields
