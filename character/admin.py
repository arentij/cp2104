from django.contrib import admin
from .models import Character, Lore, GamePhase, CurrentGamePhase, CharacterNote


@admin.register(GamePhase)
class GamePhaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(CurrentGamePhase)
class CurrentGamePhaseAdmin(admin.ModelAdmin):
    list_display = ('current_phase',)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')
    search_fields = ('name', 'short_name')
    filter_horizontal = ('users',)  # Allow selection of users in the admin interface

@admin.register(Lore)
class LoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'character')
    list_filter = ('game_phases', 'visible_to_groups')
    filter_horizontal = ('game_phases', 'visible_to_groups',)

# Register CharacterNote with custom admin
class CharacterNoteAdmin(admin.ModelAdmin):
    list_display = ('character', 'user', 'content', 'created_at')  # Display these fields in the list view
    list_filter = ('character', 'user', 'created_at')  # Filters in the sidebar
    search_fields = ('content', 'character__name', 'user__username')  # Add search functionality
    ordering = ('-created_at',)  # Order by creation date, newest first

admin.site.register(CharacterNote, CharacterNoteAdmin)