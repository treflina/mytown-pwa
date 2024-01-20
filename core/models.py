from django.db import models
from wagtail.models import Page

class HomePage(Page):
    template = "index.html"

    content_panels = Page.content_panels