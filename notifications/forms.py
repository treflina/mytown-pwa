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

        push_info, created = PushInformation.objects.get_or_create(**data)
      
        if status_type == "unsubscribe":
            push_info.delete()
            subscription_info = PushInformation.objects.filter(
                subscription_id=subscription.id
            ).count()
            if subscription_info == 0:
                subscription.delete()
