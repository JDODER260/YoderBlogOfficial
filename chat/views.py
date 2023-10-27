from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .models import Chat, Room, Message
from users.models import Profile
from main.models import Category
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from .forms import ChatForm, RoomForm
from django.http import HttpResponseRedirect, JsonResponse
import operator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .utils import NotificationMixin
import openai

openai.api_key = "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"

@login_required
def chat(request, pk):
    chats = Chat.objects.all()
    all_chats = []
    for i in chats:
        if i.person_to.id == pk and i.author.id == request.user.id or i.person_to.id == request.user.id and i.author.id == pk:
            all_chats.append(i)
    if request.method == 'POST':
        form = ChatForm(request.POST, instance=None)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.author = request.user
            chat.person_to_id = pk
            chat.save()
            return redirect('chat', pk=pk)
    else:
        form = ChatForm()
    person_to = User.objects.filter(pk=pk).first()
    context = {'chats': all_chats, 'pk': pk, 'form': form, 'person_to': person_to}
    if request.user.is_authenticated:
        cat_menu = Category.objects.all()
        chat_menu = User.objects.all()
        sidebar = []
        notifications = Chat.objects.filter(person_to=request.user).order_by('-date_posted')
        unique_authors = notifications.values('author').distinct()
        for author in unique_authors:
            latest_message = notifications.filter(author=author['author']).first()
            sidebar.append(latest_message)
        context["cat_menu"] = cat_menu
        if sidebar: context['sidebar'] = sidebar
        context["chat_menu"] = chat_menu
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(request, 'chat/chat.html', context)
        else:
            return render(request, 'themetwo/chat/chat.html', context)
    else:
        return render(request, 'chat/chat.html', context)




@login_required
def ChatView(request, pk):
    chats = Chat.objects.filter(author_id=pk)
    user_chats = Chat.objects.filter(author=request.user)
    if request.method == 'POST':
        form = ChatForm(request.POST, instance=request.user)
        def form_valid(self, form):
            form.instance.author = self.request.user
            form.instance.person_to_id = self.kwargs.get('pk')
            return super().form_valid(form)
    else:
        form = ChatForm(request.POST)
    all_chats = []
    for chat in chats:
      if chat.person_to == request.user:
        all_chats.append(chat)
    for chat in user_chats:
      if chat.person_to.id == pk:
        all_chats.append(chat)
    all_chats.sort(key = operator.attrgetter('date_posted'), reverse = True)
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(request,  'chat/chat.html', {'chats': all_chats, 'pk': pk, 'form': form})
        else:
            return render(request,  'themetwo/chat/chat.html', {'chats': all_chats, 'pk': pk, 'form': form})
    else:
        return render(request,  'chat/chat.html', {'chats': all_chats, 'pk': pk, 'form': form})




class CreateChat(NotificationMixin, CreateView):
    model = Chat
    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            if profile.layout:
                return ['themetwo/chat/create_chat.html']
            else:
                return ['chat/create_chat.html']
    form_class = ChatForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.person_to_id = self.kwargs.get('pk')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('close')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["pk"] = self.kwargs['pk']
        return(context)

def close(request):
    return HttpResponse('<script type="text/javascript">window.close()</script>')





class Home(NotificationMixin, ListView):
    model = Room
    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            print("True")
            return ['themetwo/chat/home.html']
        else:
            return ['chat/home.html']
    context_object_name = 'rooms'
    paginate_by = 7

    def get_queryset(self):
        query = []
        details = Room.objects.all()
        allowed = False
        
        for i in details:
            allowed_users = i.allowed_users.all()
            allowed = False
            if i.allow_all_users:
                allowed = True
            for x in allowed_users:
                if x.username == self.request.user.username:
                    allowed = True
                    break
            if i.user == self.request.user or self.request.user.is_staff:
                allowed = True
            if allowed:
                query.append(i)
        return query


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            cat_menu = Category.objects.all()
            chat_menu = User.objects.all()
            context["cat_menu"] = cat_menu
            context["chat_menu"] = chat_menu
            context["sidebar"]
        return context


def room(request, room):
    username = request.user.username
    room_details = Room.objects.get(name=room)
    allowed_users = room_details.allowed_users.all()
    if room_details.allow_all_users:
      allowed = True
    else:
      allowed = False
      for i in allowed_users:
          if i.username == request.user.username:
              allowed = True
      if room_details.user.username == request.user.username or request.user.is_staff:
          allowed = True
    if not allowed:
        HttpResponse(status=403)
    context = {
        'username': username,
        'room': room,
        'room_details': room_details,
        'allowed_users': allowed_users,
        'allowed': allowed,

    }
    if request.user.is_authenticated:
        cat_menu = Category.objects.all()
        chat_menu = User.objects.all()
        sidebar = []
        notifications = Chat.objects.filter(person_to=request.user).order_by('-date_posted')
        unique_authors = notifications.values('author').distinct()
        for author in unique_authors:
            latest_message = notifications.filter(author=author['author']).first()
            sidebar.append(latest_message)
        context["cat_menu"] = cat_menu
        if sidebar: context['sidebar'] = sidebar
        context["chat_menu"] = chat_menu
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(request, 'chat/room.html', context)
        else:
            return render(request, 'themetwo/chat/room.html', context)
    else:
        return render(request, 'chat/room.html', context)

def checkview(request):
    room = request.POST['room_name']

    if Room.objects.filter(name=room).exists():
        return HttpResponseRedirect(reverse('room', args=[str(room)]))
    else:
        return HttpResponseRedirect(reverse('create_room'))

def send(request):
    message = request.POST['message']
    room_id = request.POST['room_id']
    room = Room.objects.filter(id = room_id).first()
    chatgpt_user = User.objects.filter(username = "ChatGPT").first()
    new_message = Message.objects.create(value=message, user=request.user, room_id=room_id)
    new_message.save()
    print(room.name)
    if room.name == "ChatGPT":
        response = openai.Completion.create(
    model="text-davinci-003",
    prompt=message,
    temperature=0.8,
    max_tokens=1024,
)

        new_message = Message.objects.create(value=response.choices[0].text, user=chatgpt_user, room_id=room_id)
        new_message.save()
    return HttpResponse('Message sent successfully')
#This veiw returns the user_id instead of the user Username
#def getMessages(request, room):
    #room_details = Room.objects.get(name=room)

    #messages = Message.objects.filter(room=room_details.id)
    #return JsonResponse({"messages":list(messages.values())})

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    messages_list = []
    for message in messages:
        message_data = {
            "value": message.value,
            "date": message.date,
            "user": message.user.username,
        }
        messages_list.append(message_data)
    return JsonResponse({"messages": messages_list})


class RoomListView(NotificationMixin, ListView):
    model = Room
    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
                return ['themetwo/chat/vew_rooms.html']
        else:
            return ['chat/view_rooms.html']
    context_object_name = 'rooms'
    paginate_by = 7





class RoomDeleteView(NotificationMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Room
    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
                return ['themetwo/chat/delete_room.html']
        else:
            return ['chat/delete_room.html']
    success_url = reverse_lazy('chat-home')

    def test_func(self):
        room = self.get_object()
        return self.request.user == room.user or self.request.user.is_superuser





class UpdateRoomView(NotificationMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Room
    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
                return ['themetwo/chat/update_room.html']
        else:
            return ['chat/update_room.html']
    form_class = RoomForm
    success_url = reverse_lazy('chat-home')

    def test_func(self):
        room = self.get_object()
        return self.request.user == room.user or self.request.user.is_superuser


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
                return ['themetwo/chat/create_room.html']
        else:
            return ['chat/create_room.html']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('room', kwargs={'room': self.object.name})

