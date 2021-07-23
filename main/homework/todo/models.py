from django.contrib.auth.models import User
from django.db import models

import uuid

# Create your models here.


class Todo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for Todo")
    performer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    todo_title = models.CharField(max_length=200)


class Pomodoro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    count = models.IntegerField()

