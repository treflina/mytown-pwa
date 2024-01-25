from django.contrib import admin
from django.urls import path, include

from notifications import views

app_name = "notifications"

urlpatterns = [
    path("webpush/send/", views.save_info, name="save_webpush_info"),
    path("subscription-check/", views.subscription_check, name="subscription-check"),
    path("", views.subscriptions_list, name="subscriptions"),
]
