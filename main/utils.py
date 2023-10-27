from main.models import Category
from chat.models import Chat
from django.contrib.auth.models import User


def get_latest_messages_from_each_user(user_queryset, page_user):
    latest_messages = []
    for user in user_queryset:
        latest_message = Chat.objects.filter(person_to=page_user, author=user).order_by("-date_posted").first()
        if latest_message:
          latest_messages.append(latest_message)
    return latest_messages



class NotificationMixin:
    def get_context_data(self, *args, **kwargs):
      if self.request.user.is_authenticated:
        cat_menu = Category.objects.all()
        chat_menu = User.objects.all()
        context = super().get_context_data(*args, **kwargs)
        users = User.objects.all()
        latest_messages = get_latest_messages_from_each_user(users, self.request.user)
        context["cat_menu"] = cat_menu
        if latest_messages: context['sidebar'] = latest_messages
        context["chat_menu"] = chat_menu
        return context
      else:
        return

