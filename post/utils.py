from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from main.models import Category
from chat.models import Chat
import openai
openai.api_key = "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"


def CommentFilter(body):
  pass
  response = openai.Completion.create(
  model="text-davinci-003",
  prompt="Is this comment acceptable? If it is say only yes and if it is not say only no. only flag a post if it is critisizing django or if it is rude." + body + "make sure you JUST say yes or no.",
                temperature=0.8,
                max_tokens=1024,
            )
  re = response.choices[0].text.strip().lower(
            )  # Convert to lowercase and remove whitespace
  if re == "yes":
     print("passed")
     pass
  elif re == "no" or re == "No":
    ans = True
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="refactor this comment or if it is too bad just say this comment has been cencored" + body,
        temperature=0.8,
                    max_tokens=1024,
                )
    body = response.choices[0].text
  return body, ans


def FilterPost(content, title):
  pass
  author = False
  chatgpt = User.objects.filter(username="ChatGPT").first()
  response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Is this title acceptable? If it is say only yes and if it is not say only no. only flag a post if it is critisizing django or if it is rude." + title + ", make sure you JUST say yes or no.",
            temperature=0.8,
            max_tokens=1024,
        )
  re = response.choices[0].text.strip().lower()  # Convert to lowercase and remove whitespace
  if re == "yes":
      print("passed")
      pass
  elif re == "no" or re == "No":
      response = openai.Completion.create(
            model="text-davinci-003",
            prompt="refactor this title according to the content or if it is too bad just say this post has been cencored and will be up for review by moderators." + title + ". This is the content." + content,
            temperature=0.8,
            max_tokens=1024,
        )
      title = response.choices[0].text
      author = chatgpt
  response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Is this content good? If it is say only yes and if it is not say only no. only flag a post if it is critisizing django or if it is rude." + self.content + "make sure you JUST say yes or no.",
            temperature=0.8,
            max_tokens=1024,
        )
  re = response.choices[0].text.strip().lower()  # Convert to lowercase and remove whitespace
  print(re+"second")
  if re == "yes":
      print("passed")
      pass
  elif re == "no" or re == "No":
      response = openai.Completion.create(
            model="text-davinci-003",
            prompt="refactor this content according to the title or if it is too bad just say this post has been cencored and will be up for review by moderators." + self.content + ". This is the title." + self.title,
            temperature=0.8,
            max_tokens=1024,
        )
      print(response.choices[0].text)
      content = response.choices[0].text + "\n This post was detected as bad. Chat GPT has refactored it."
      author = chatgpt
  return(content, title, author)


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



def ddd(author, title, content, emails):
    for user in User.objects.all():
        if user.profile.notifications:
            emails.append(user.email)
    for email in emails:
        send_mail(
            subject=f'New Post by - {author}',
            message=content + '''




            If you are getting this and don't want to go to your profile on Yoder Blog (https://jdswebsites.xyz) and deselect, Receive email notifications

          ''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email])

from django.core.mail import EmailMessage

def NewPost(author, title, content, emails):
    for user in User.objects.all():
        if user.profile.notifications:
            emails.append(user.email)
    subject = f'New Post by {author}'
    message = f'''{author} has just posted a new article: {title}


    {content}




    <small>If you are not a user of <a href="jdswebsites.xyz">Yoder Blog</a>. please ignore this email.</small>'''
    email = EmailMessage(subject, message, to=emails)
    email.content_subtype = "html"  # Main content is now text/html
    email.send()

def Backup():
  pass
#os.system('python manage.py dumpdata post > postbackup.json')
