from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path("admin/", admin.site.urls),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
    path(
        "manifest.json",
        TemplateView.as_view(
            template_name="manifest.json", content_type="application/json"
        ),
        name="manifest.json",
    ),
    path("webpush/", include("webpush.urls")),
    path(
        "sw.js",
        (
            TemplateView.as_view(
                template_name="sw.js",
                content_type="application/javascript",
            )
        ),
        name="serviceworker",
    ),
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("odpady/", include("garbage.urls")),
    path("powiadomienia/", include("notifications.urls")),
    path("", include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
