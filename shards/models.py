from django.db import models
import uuid

# Create your models here.

class Shard(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique UUID for each shard
    name = models.CharField(max_length=255)  # Name of the shard
    text = models.TextField()  # Field to store shard information (text)
    password = models.CharField(max_length=255, blank=True, null=True)  # Optional password field

    def __str__(self):
        return f"Shard {self.uuid}"