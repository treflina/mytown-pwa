import json
import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError

from webpush import send_group_notification
from webpush.models import Group
from garbage.models import GarbageCollection, Region


logging.root.handlers = []
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("notifications.log")],
)


def get_tomorrow():
    return (timezone.now() + timedelta(days=1)).date()


class Command(BaseCommand):
    help = "Send notifications about a garbage collection if it's planned for the next day."

    def handle(self, *args, **options):
        regions = Region.objects.all()
        tomorrow = get_tomorrow()
        for region in regions:
            num = region.number
            gar_col = GarbageCollection.objects.filter(region=region, date=tomorrow)

            for col in gar_col:
                body = f"{region.name} (Rejon {region.number})"
                payload = {
                    "head": f"Jutro {col.date.strftime('%d-%m-%Y')} wywóz: {col.garbage_type.name}",
                    "body": body,
                    "badge": "static/img/trash2.png",
                    "url": f"/odpady/regions/{region.id}",
                }
                if Group.objects.filter(name=region.id):
                    try:
                        send_group_notification(
                            group_name=region.id, payload=payload, ttl=1000
                        )
                        logging.info(f"{region.name}: {col.garbage_type.name}")
                    except Exception as e:
                        send_mail(
                            "eTurawa",
                            f"{e}",
                            settings.EMAIL_HOST_USER,
                            [settings.EMAIL_HOST_USER],
                            fail_silently=False,
                        )
                        logging.error(f"Błąd przy próbie wysłania powiadomień: {e}")
