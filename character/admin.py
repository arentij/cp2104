from django.contrib import admin
from .models import GamePhase, CurrentGamePhase, Character, Lore

@admin.register(GamePhase)
class GamePhaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(CurrentGamePhase)
class CurrentGamePhaseAdmin(admin.ModelAdmin):
    list_display = ('current_phase',)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Lore)
class LoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'character')
    list_filter = ('game_phases', 'visible_to_groups')
    filter_horizontal = ('game_phases', 'visible_to_groups',)
