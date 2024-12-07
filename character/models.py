from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import random
import string

class GamePhase(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class CurrentGamePhase(models.Model):
    current_phase = models.OneToOneField(GamePhase, on_delete=models.CASCADE)

    def __str__(self):
        return f"Current Phase: {self.current_phase.name}"

class Character(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    short_name = models.CharField(max_length=4, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.generate_short_name()
        super().save(*args, **kwargs)    

    @staticmethod
    def generate_short_name():
        while True:
            short_name = ''.join(random.choices(string.ascii_letters, k=4))
            if not Character.objects.filter(short_name=short_name).exists():
                return short_name

    def __str__(self):
        return self.name

class Lore(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='lores')
    title = models.CharField(max_length=200)
    content = models.TextField()
    game_phases = models.ManyToManyField(GamePhase)
    visible_to_groups = models.ManyToManyField(Group)

    def __str__(self):
        return f"{self.title} ({self.character.name})"

# Ensure the 'Common' group exists and all players are members of it
@receiver(post_migrate)
def create_common_group(sender, **kwargs):
    if sender.name == 'character':
        common_group, created = Group.objects.get_or_create(name='Common')
        if created:
            print("'Common' group created.")

class CharacterNote(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.user.username} on {self.character.name}"