from django.urls import path
from .views import ChatView, CreateChat, close, Home, room, checkview, send, getMessages,RoomListView, RoomDeleteView, UpdateRoomView, chat, RoomCreateView


urlpatterns = [
    path('chat/room/create/', RoomCreateView.as_view(), name='create_room'),
    path('chat/<int:pk>/', chat, name='chat'),
    path('chat/new/<int:pk>/', CreateChat.as_view(), name='create_chat'),
    path('close', close, name='close'),
    path('chat/', Home.as_view(), name='chat-home'),
    path('chat/room/<str:room>/', room, name='room'),
    path('chat/checkview', checkview, name='checkview'),
    path('send', send, name='send'),
    path('getMessages/<str:room>/', getMessages, name='getMessages'),
    path('chat/rooms/', RoomListView.as_view(), name='room_list'),
    path('chat/room/delete/<int:pk>/', RoomDeleteView.as_view(), name='room-delete'),
    path('chat/room/update/<int:pk>/', UpdateRoomView.as_view(), name='room-update'),
]
