import logging

from webpush import send_group_notification
from webpush.models import Group, PushInformation

from wagtail import hooks
from news.models import NewsDetailPage, NewsIndexPage
from .models import NotificationGroup

logging.root.handlers = []
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("news_notifications.log")],
)


@hooks.register("after_publish_page")
def send_notifications(request, page):
    if isinstance(page, NewsDetailPage):
        if page.send_notifications:
            for group in page.notification_groups.all():
                body = f"{page.event_date}"
                if group.name in ["Ważne alerty", "Ogólne"]:
                    head = str(page.title)
                else:
                    head = f"{page.title} ({group.name})",

                payload = {
                    "head": head,
                    "body": body,
                    "url": f"/aktualnosci/{page.slug}",
                }
                if Group.objects.filter(name=group.slug):
                    send_group_notification(
                        group_name=group.slug, payload=payload, ttl=1000
                    )
                    logging.info(f"Sent: {group.name}: {page.title}")
        page.send_notifications = False
        page.save()


@hooks.register("after_publish_page")
def create_notification_categories(request, page):
    group_names = [
        "Ważne alerty",
        "Ogólne",
        "Bierdzany",
        "Kadłub Turawski",
        "Kotórz Mały",
        "Kotórz Wielki",
        "Ligota Turawska",
        "Osowiec",
        "Rzędów",
        "Turawa",
        "Węgry",
        "Zawada",
        "Zakrzów Turawski"
    ]
    if isinstance(page, NewsIndexPage):
        for name in group_names:
            group, created = NotificationGroup.objects.get_or_create(name=name)
