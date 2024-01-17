import json
from django.utils import timezone
from datetime import timedelta
from django.core.management.base import BaseCommand, CommandError
from webpush import send_group_notification
from webpush.models import Group
from garbage.models import GarbageCollection, Region


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
                body = f"{col.garbage_type.name} & {region.id}"
                payload = {"head": "Jutro wywóz:", "body": body}
                if Group.objects.filter(name=region.id):
                    send_group_notification(
                        group_name=region.id, payload=payload, ttl=1000
                    )
