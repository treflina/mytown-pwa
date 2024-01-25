from datetime import timedelta

from django import forms
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    MultipleChooserPanel,
    MultiFieldPanel,
)
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page

from . import blocks


class NewsIndexPage(Page):
    """News listing page model."""

    template = "news/news_index.html"
    subpage_types = ["news.NewsDetailPage"]
    parent_page_types = ["core.HomePage"]
    max_count = 1

    @property
    def get_child_pages(self):
        return self.get_children().public().live()

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)

        news = (
            NewsDetailPage.objects.live()
            .public()
            .specific()
            .order_by("-first_published_at")
        )
        if request.GET.get("tag", None):
            tags = request.GET.get("tag")
            news = news.filter(tags__slug__in=[tags])
            tag = Tag.objects.filter(slug__in=[tags]).first()

            context["tag_filter"] = True
            context["tag"] = tag

        context["posts"] = news
        return context

    class Meta:  # noqa
        verbose_name = _("news")
        verbose_name_plural = _("news")


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "news.NewsDetailPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class NewsDetailPage(Page):
    """Detail page for news content."""

    page_description = _("New post in news.")
    subpage_types = []
    parent_page_types = ["news.NewsIndexPage"]

    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)
    notification_groups = ParentalManyToManyField(
        "notifications.NotificationGroup", blank=True
    )

    event_date = models.DateField(
        blank=True,
        null=True,
        default=now,
        verbose_name=_("Event date"),
    )

    publish_end_date = models.DateField(
        blank=True,
        null=True,
        default=(now() + timedelta(days=30)).date(),
        verbose_name=_("Publishing end date"),
    )

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        verbose_name=_("Banner image"),
    )

    included_in_content = models.BooleanField(
        verbose_name=_("Included in the article's content"),
        default=False,
        help_text="""Include the image in the article's detail content.""",
    )

    alt_attr = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        verbose_name=_("Alternative text"),
        help_text=_(
            """Image description for visually impaired users & search engines."""
        ),
    )

    main_text = RichTextField(
        blank=False,
        null=True,
        verbose_name=_("Main text"),
        features=[
            "bold",
            "italic",
            "ol",
            "ul",
            "hr",
            "link",
            "document-link",
        ],
    )

    body = StreamField(blocks.BodyBlock(), null=True, blank=True, use_json_field=True)

    promote_panels = Page.promote_panels + []

    content_panels = Page.content_panels + [
        FieldRowPanel(
            [
                FieldPanel("event_date"),
                FieldPanel("publish_end_date"),
            ],
            heading=_("Dates"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("banner_image"),
                FieldPanel("alt_attr"),
                FieldPanel("included_in_content"),
            ],
            heading=_("Banner image"),
        ),
        FieldPanel("main_text"),
        FieldPanel("body"),
        MultiFieldPanel(
            [
                MultipleChooserPanel(
                    "gallery_images",
                    label=_("Images"),
                    chooser_field_name="image",
                    help_text=_(
                        "Images will be placed in the mini gallery at the end of the article."
                    ),
                ),
            ],
            heading=_("Mini gallery"),
        ),
        MultiFieldPanel(
            [
                FieldPanel("tags"),
                FieldPanel("notification_groups", widget=forms.CheckboxSelectMultiple),
            ],
            heading=_("Notifications and tags")
        ),
    ]

    class Meta:  # noqa
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")


class MiniGalleryImage(Orderable):
    page = ParentalKey(
        NewsDetailPage, on_delete=models.CASCADE, related_name="gallery_images"
    )

    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.CASCADE,
        related_name="+",
        verbose_name=_("Image"),
    )
    alt_attr = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_("Alternative text"),
    )

    panels = [FieldPanel("image"), FieldPanel("alt_attr")]
