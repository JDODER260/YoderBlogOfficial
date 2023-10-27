from django.contrib import admin
from .models import Chat, Room, Message



admin.site.register(Chat)
admin.site.register(Room)
admin.site.register(Message)