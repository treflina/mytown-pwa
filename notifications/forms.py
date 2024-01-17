from webpush.forms import WebPushForm
from webpush.models import Group, PushInformation


class CustomWebPushForm(WebPushForm):
    def save_or_delete(self, subscription, user, status_type, group_name):
        # Ensure get_or_create matches exactly
        data = {"user": None, "group": None}

        if user.is_authenticated:
            data["user"] = user

        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            data["group"] = group

        data["subscription"] = subscription
        endpoint = subscription.endpoint

        push_info, created = PushInformation.objects.get_or_create(**data)

        if status_type == "unsubscribe":
            push_info.delete()
            subscription_count = PushInformation.objects.filter(
                subscription__endpoint=endpoint
            ).count()
            if subscription_count <= 1:
                subscription.delete()
