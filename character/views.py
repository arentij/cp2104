from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import Character, CurrentGamePhase, Lore

@login_required
def character_page(request, character_id):
    character = get_object_or_404(Character, id=character_id)
    user_groups = request.user.groups.all()
    current_phase_instance = CurrentGamePhase.objects.first()
    current_phase = current_phase_instance.current_phase if current_phase_instance else None

    # Ensure the user is in the 'Common' group
    common_group, _ = Group.objects.get_or_create(name='common')
    if common_group not in user_groups:
        request.user.groups.add(common_group)
        user_groups = request.user.groups.all()

    if current_phase:
        # Get the lore entries for the character visible to the user's groups and current game phase
        visible_lore = Lore.objects.filter(
            character=character,
            game_phases=current_phase,
            visible_to_groups__in=user_groups
        ).distinct()
    else:
        visible_lore = Lore.objects.none()

    context = {
        'character': character,
        'visible_lore': visible_lore
    }

    return render(request, 'character_page.html', context)