from django.urls import include, path
from rest_framework import routers

from garbage import views

router = routers.DefaultRouter()
router.register(r"Region", views.RegionViewSet)
router.register(r"GarbageType", views.GarbageTypeViewSet)
router.register(r"garbagecollection", views.GarbageCollectionViewSet)

# Wire up our API using automatic URL routing.
# Additionally, login URLs for the browsable API.

app_name = "garbage"

urlpatterns = [
    # path("", views.HomeView.as_view(), name="home"),
    path("regions/", views.RegionListView.as_view(), name="regions"),
    path("regions/<int:pk>/", views.RegionDetailView.as_view(), name="region-details"),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

urlpatterns += router.urls
