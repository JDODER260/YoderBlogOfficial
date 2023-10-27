from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Category
from chat.models import Chat
from post.models import Post
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from .forms import ChatForm, CategoryForm
from .utils import NotificationMixin
import random
from users.models import Profile


def AboutView(request):
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(request, 'blog/about.html', {'title': 'About'})
        else:
            return render(request, 'themetwo/about.html', {'title': 'About'})
    else:
        return render(request, 'blog/about.html', {'title': 'About'})


def NavigationView(request):
    context = {}
    if request.user.is_authenticated:
        cat_menu = Category.objects.all()
        chat_menu = User.objects.all()
        sidebar = []
        notifications = Chat.objects.filter(
            person_to=request.user).order_by('-date_posted')
        unique_authors = notifications.values('author').distinct()
        for author in unique_authors:
            latest_message = notifications.filter(
                author=author['author']).first()
            sidebar.append(latest_message)
        context["cat_menu"] = cat_menu
        if sidebar: context['sidebar'] = sidebar
        context["chat_menu"] = chat_menu
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(request, 'blog/navigation.html', context)
        else:
            return render(request, 'themetwo/navigation.html', context)
    else:
        return render(request, 'blog/navigation.html', context)


def CategoryView(request, cats):
    category_posts = Post.objects.filter(category=cats).order_by('-id')
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(request, 'blog/categories.html', {
                'posts': category_posts,
                'cats': cats
            })
        else:
            return render(request, 'themetwo/categories.html', {
                'posts': category_posts,
                'cats': cats
            })
    else:
        return render(request, 'blog/categories.html', {
            'posts': category_posts,
            'cats': cats
        })


class CreateCategory(NotificationMixin, CreateView):
    model = Category
    form_class = CategoryForm

    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/add_category.html']
        else:
            return ['blog/add_category.html']

    def get_success_url(self):
        return reverse('close')


class SearchView(NotificationMixin, ListView):
    model = Post

    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/search_results.html']
        else:
            return ['blog/search_results.html']

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Post.objects.filter(
            title__icontains=query) | Post.objects.filter(
                content__icontains=query) | Post.objects.filter(
                    category__icontains=query) | Post.objects.filter(
                        date_posted__icontains=query) | Post.objects.filter(
                            author__username__icontains=query)
        return object_list

    def get_context_data(self, *args, **kwargs):
        query = self.request.GET.get("q")
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context["query"] = query
        return (context)


class Nofilterview(NotificationMixin, ListView):
    paginate_by = 9
    ordering = ['-date_posted']
    model = Post

    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/filter_off.html']
        else:
            return ['blog/home.html']

    context_object_name = 'posts'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        posts = Post.objects.all()

        # Get the total number of comments for each post
        lists_comm = []
        for i in posts:
            comm = 0
            for x in i.comments.all():
                comm += 1
            lists_comm.append({"post": i.title, "total_comms": comm})

        # Get the top 5 posts with the most likes
        hero_section = sorted(posts,
                              key=lambda x: x.likes.count(),
                              reverse=True)[:5]

        # Get the most recent 7 posts
        post_grid_section = posts.order_by('-date_posted')[:6]
        pg1 = post_grid_section[:3]
        pg2 = post_grid_section[3:6]
        # Get all the posts with the category "Chess"
        chess_category_section = posts.filter(category='Chess')
        ranone = random.choice(posts)

        # Get the 6 most commented posts
        trending_posts = sorted(posts,
                                key=lambda post: post.comments.count(),
                                reverse=True)[:6]

        # Get the 6 most recent posts
        latest_posts = posts.order_by('-date_posted')[:6]
        context["popular_posts"] = hero_section
        context["trending_posts"] = trending_posts
        context["latest_posts"] = latest_posts
        context["hero_section"] = hero_section
        context["pg1"] = pg1
        context["pg2"] = pg2
        context["ranone"] = ranone
        context["post_grid_section"] = post_grid_section
        context["chess_category_section"] = chess_category_section
        context["comment_post_list"] = lists_comm
        context["hello"] = True
        return (context)
