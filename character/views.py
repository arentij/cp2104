from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Character, CurrentGamePhase, Lore
from .forms import CharacterNoteForm
from django.contrib import messages

@login_required
def character_page(request, short_name):
    character = get_object_or_404(Character, short_name=short_name)
    user_groups = request.user.groups.all()
    current_phase_instance = CurrentGamePhase.objects.first()
    current_phase = current_phase_instance.current_phase if current_phase_instance else None

    # Ensure the user is in the 'Common' group
    common_group, _ = Group.objects.get_or_create(name='common')
    if common_group not in user_groups:
        request.user.groups.add(common_group)
        user_groups = request.user.groups.all()

    if current_phase:
        visible_lore = Lore.objects.filter(
            character=character,
            game_phases=current_phase,
            visible_to_groups__in=user_groups
        ).distinct()
    else:
        visible_lore = Lore.objects.none()

    # Determine if notes should be shown
    show_notes = request.user in character.users.all()

    context = {
        'character': character,
        'visible_lore': visible_lore,
        'show_notes': show_notes
    }

    return render(request, 'character_page.html', context)

    return render(request, 'character_page.html', context)

def character_list(request):
    characters = Character.objects.all()  # Retrieve all characters
    context = {
        'characters': characters
    }
    return render(request, 'character_list.html', context)

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('character_page', short_name='main')  # Redirect to a default character page
    else:
        form = AuthenticationForm()

    context = {'form': form}
    if request.user.is_authenticated:
        context['username'] = request.user.username
    return render(request, 'login.html', context)

@login_required
def custom_logout(request):
    logout(request)
    return render(request, 'logout.html')

def toc(request):
    return render(request, 'index.html')