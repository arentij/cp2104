from django.contrib import admin
from .models import Author, Message

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'content')
    search_fields = ('author', 'content')
