from garbage.models import GarbageType, Region, GarbageCollection
from rest_framework import serializers


class GarbageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarbageType
        fields = ["name", "short_name", "color"]


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["name", "garbage_collection"]


class GarbageCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GarbageCollection
        fields = ["id", "garbage_type", "date"]
