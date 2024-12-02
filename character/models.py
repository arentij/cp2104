from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

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

    def __str__(self):
        return self.name

class Lore(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='lores')
    title = models.CharField(max_length=200)
    content = models.TextField()
    game_phase = models.ForeignKey(GamePhase, on_delete=models.CASCADE)
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