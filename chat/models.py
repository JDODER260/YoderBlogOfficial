from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime


class Chat(models.Model):
    person_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='person_to')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s - %s' % (self.author, self.person_to, self.content)

    def get_absolute_url(self):
        return reverse('chat', kwargs={'pk': self.pk})


class Room(models.Model):
    name = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    allowed_users = models.ManyToManyField(User, related_name='allowed_users', blank=True)
    allow_all_users = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.user})"



class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username}, {self.room.name}, {self.date}"
