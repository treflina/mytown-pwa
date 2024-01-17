import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import TemplateView

from webpush.forms import SubscriptionForm, WebPushForm
from webpush.views import process_subscription_data
from webpush.models import PushInformation, SubscriptionInfo
from .forms import CustomWebPushForm


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

            if status_type == "subscribe":
                return HttpResponse(status=201)
            elif "unsubscribe":
                return HttpResponse(status=202)
    return HttpResponse(status=400)
