from django.contrib import admin

from garbage.models import GarbageType, GarbageCollection, Region

admin.site.register(GarbageCollection)
admin.site.register(GarbageType)
admin.site.register(Region)
