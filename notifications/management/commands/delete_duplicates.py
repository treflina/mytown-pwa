import logging
from django.db.models import Count, Min

from django.core.management.base import BaseCommand
from webpush.models import SubscriptionInfo


logging.root.handlers = []
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("notifications.log")],
)


class Command(BaseCommand):
    help = "Delete duplicated subscriptions after user agent update"

    def handle(self, *args, **options):
        duplicates = (
            SubscriptionInfo.objects
            .values('auth', 'p256dh')
            .annotate(min_id=Min('id'), count_id=Count('id'))
            .filter(count_id__gt=1)
        )

        min_ids_to_delete = [entry['min_id'] for entry in duplicates]

        if min_ids_to_delete:
            SubscriptionInfo.objects.filter(id__in=min_ids_to_delete).delete()
            logging.info(f"Subscriptions with ids: {min_ids_to_delete} have been deleted.")
