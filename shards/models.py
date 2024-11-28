from django.db import models

# Create your models here.

class Shard(models.Model):
    text = models.TextField()  # Field to store shard information (text)
    password = models.CharField(max_length=255, blank=True, null=True)  # Optional password field

    def __str__(self):
        return f"Shard {self.id}"