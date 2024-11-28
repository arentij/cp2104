from django.contrib import admin
from django.contrib import admin
from .models import Shard

# Register your models here.

@admin.register(Shard)
class ShardAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'password')
    search_fields = ('text',)