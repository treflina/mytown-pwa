import datetime
from django.conf import settings
from django.db.models import Q, F
from django.db.models.functions import ExtractDay
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, viewsets

from garbage.models import GarbageCollection, GarbageType, Region
from garbage.serializers import (
    GarbageCollectionSerializer,
    GarbageTypeSerializer,
    RegionSerializer,
)


class HomeView(TemplateView):
    template_name = "index.html"


class RegionListView(ListView):
    model = Region
    template_name = "garbage/regions-list.html"
    context_object_name = "regions"


class RegionDetailView(DetailView):
    model = Region
    template_name = "garbage/garbagecollection-detail.html"

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_garbage_types = GarbageType.objects.all().order_by("number")
        nearest_collection_objects = {}
        for garbage_type in all_garbage_types:
            nearest_collection_objects[garbage_type] = GarbageCollection.objects.filter(
                Q(region=self.object)
                & Q(garbage_type=garbage_type)
                & Q(date__gte=timezone.now())
            )[:2]
        context["nearest_collection_types"] = nearest_collection_objects

        # notifications
        obj = self.get_object()
        context["webpush"] = {"group": obj.id}
        webpush_settings = getattr(settings, "WEBPUSH_SETTINGS", {})
        context["vapid_key"] = webpush_settings.get("VAPID_PUBLIC_KEY")
        return context


class RegionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows garbage types to be viewed or edited.
    """

    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class GarbageTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows garbage types to be viewed or edited.
    """

    queryset = GarbageType.objects.all()
    serializer_class = GarbageTypeSerializer


class GarbageCollectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows garbage collection dates to be viewed or edited.
    """

    queryset = GarbageCollection.objects.all()
    serializer_class = GarbageCollectionSerializer
