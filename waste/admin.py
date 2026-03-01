from django.contrib import admin
from .models import Collection

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('worker', 'ward', 'house_code', 'date')
    list_filter = ('ward', 'date')
    search_fields = ('house_code', 'worker__username')