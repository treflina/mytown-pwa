import json
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView

from webpush.forms import SubscriptionForm, WebPushForm
from webpush.views import process_subscription_data
from webpush.models import PushInformation, SubscriptionInfo

from garbage.models import Region
from notifications.models import NotificationGroup
from .forms import CustomWebPushForm


def subscriptions_list(request):
    regions = Region.objects.all()
    groups = NotificationGroup.objects.all()
    context = {"regions": regions, "groups": groups}

    webpush_settings = getattr(settings, "WEBPUSH_SETTINGS", {})
    context["vapid_key"] = webpush_settings.get("VAPID_PUBLIC_KEY")

    return render(
        request,
        "notifications/notifications_settings.html",
        context=context,
    )


@require_POST
def subscription_check(request):
    try:
        post_data = json.loads(request.body.decode("utf-8"))
        subscription_endpoint = post_data["subscription"]["endpoint"]
        group = post_data["group"]
    except (ValueError, KeyError):
        return HttpResponse(status=400)

    if PushInformation.objects.filter(
        subscription__endpoint=subscription_endpoint, group__name=group
    ).exists():
        return HttpResponse(status=200)
    return HttpResponse(status=240)


@require_POST
def save_info(request):
    try:
        post_data = json.loads(request.body.decode("utf-8"))
    except ValueError:
        return HttpResponse(status=400)

    subscription_data = process_subscription_data(post_data)
    subscription_form = SubscriptionForm(subscription_data)
    web_push_form = CustomWebPushForm(post_data)

    if subscription_form.is_valid() and web_push_form.is_valid():
        web_push_data = web_push_form.cleaned_data
        status_type = web_push_data.pop("status_type")
        group_name = web_push_data.pop("group")

        if request.user.is_authenticated or group_name:
            subscription = subscription_form.get_or_save()

            web_push_form.save_or_delete(
                subscription=subscription,
                user=request.user,
                status_type=status_type,
                group_name=group_name,
            )
            push_info = PushInformation.objects.filter(
                subscription_id=subscription.id
            ).count()

            if status_type == "subscribe":
                return HttpResponse(status=201)
            elif push_info > 0 and status_type == "unsubscribe":
                return HttpResponse(status=242)
            elif status_type == "unsubscribe":
                return HttpResponse(status=202)
    return HttpResponse(status=400)
