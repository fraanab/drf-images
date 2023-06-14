import uuid

from django.contrib.auth.models import User
from django.db import models


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teamname = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.teamname

class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    def __str__(self):
        return f'{self.team.teamname}, member: {self.member.username}'

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    thumbnail = models.ImageField(upload_to='images/', default='images/note_ml5jgv.jpg', blank=True)
    content = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tasks", blank=True, null=True)

    def __str__(self):
        return f'"{self.content}" by {self.by}. {self.team}'

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    by = models.ForeignKey(User, on_delete=models.CASCADE)
