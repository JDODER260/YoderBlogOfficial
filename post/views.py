from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Post, Comment
from main.models import Category
from chat.models import Chat
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .utils import NewPost, Backup, NotificationMixin, FilterPost, CommentFilter
from .forms import AddCommentForm, PostForm
import operator
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from users.forms import Profile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random
import openai

openai.api_key = "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"

# views.py
from django_filters.views import FilterView
from .forms import PostFilterSet


class PostListView(NotificationMixin, FilterView):
    paginate_by = 6
    ordering = ['-date_posted']
    model = Post
    context_object_name = 'posts'
    filterset_class = PostFilterSet

    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/home.html']
        else:
            return ['blog/home.html']

    @method_decorator(csrf_exempt)
    def get_queryset(self):
        queryset = Post.objects.filter(category='Complaints') | \
                   Post.objects.filter(category='Feature-Requests') | \
                   Post.objects.filter(category='Conversation') | \
                   Post.objects.filter(category='Coding') | \
                   Post.objects.filter(category='Implemented-requests') | \
                   Post.objects.filter(category='Questions')
        queryset = queryset.order_by('-date_posted')
        return queryset

    @method_decorator(csrf_exempt)
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
                                reverse=True)[:4]

        # Get the 6 most recent posts
        latest_posts = posts.order_by('-date_posted')[:4]
        if self.request.user.is_authenticated:
            context["popular_posts"] = hero_section[:4]
            context["trending_posts"] = trending_posts
            context["latest_posts"] = latest_posts
            context["hero_section"] = hero_section
            context["pg1"] = pg1
            context["pg2"] = pg2
            context["ranone"] = ranone
            context["post_grid_section"] = post_grid_section
            context["chess_category_section"] = chess_category_section
            context["comment_post_list"] = lists_comm
            context["hello"] = self.request.user.is_authenticated
        return context


@login_required
def viewpost(request, pk):
    chatgpt = User.objects.filter(username="ChatGPT").first()
    post = Post.objects.get(id=pk)
    total_comments = 0
    for c in post.comments.all():
        total_comments += 1
    stuff = get_object_or_404(Post, id=pk)
    total_likes = stuff.total_likes()
    liked = False
    if stuff.likes.filter(id=request.user.id).exists():
        liked = True
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            ans = False
            form.instance.post_id = pk
            form.instance.author_id = request.user.id
            body = form.instance.body
            #body, ans = CommentFilter(body)
            form.instance.body = body
            if ans:
              form.instance.author = chatgpt
            form.save()
            return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))
        form = AddCommentForm()
    else:
        form = AddCommentForm()
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(
                request, 'blog/details.html', {
                    'post': post,
                    'liked': liked,
                    'total_likes': total_likes,
                    'pk': pk,
                    'form': form,
                    'total_comments': total_comments
                })
        else:
            return render(
                request, 'themetwo/details.html', {
                    'post': post,
                    'liked': liked,
                    'total_likes': total_likes,
                    'pk': pk,
                    'form': form,
                    'total_comments': total_comments
                })
    else:
        return render(
            request, 'blog/details.html', {
                'post': post,
                'liked': liked,
                'total_likes': total_likes,
                'pk': pk,
                'form': form,
                'total_comments': total_comments
            })


class PostCreateView(NotificationMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/post_create.html']
        else:
            return ['blog/post_create.html']

    def form_valid(self, form):
        author = False
        form.instance.author = self.request.user
        self.title = form.instance.title
        self.content = form.instance.content
      #This is if openai chatgpt is not working
        #self.content, self.title, author = FilterPost(self.content, self.title)
        
        if author:
            form.instance.author = author
            form.instance.title = self.title
            form.instance.content = self.content
        NewPost(self.request.user.username,
                form.instance.title,
                form.instance.content,
                emails=[self.request.user.email])

        return super().form_valid(form)


class PostUpdateView(NotificationMixin, LoginRequiredMixin,
                     UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm

    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/post_update.html']
        else:
            return ['blog/post_update.html']

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False


class PostDeleteView(NotificationMixin, LoginRequiredMixin,
                     UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = 'post'

    def get_template_names(self):
        profile = Profile.objects.all().first()
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/post_delete.html']
        else:
            return ['blog/post_delete.html']

    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False


class UserPostListView(NotificationMixin, LoginRequiredMixin, ListView):
    paginate_by = 7
    model = Post

    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/user_posts.html']
        else:
            return ['blog/user_posts.html']

    context_object_name = 'posts'

    def get_queryset(self):
        user = User.objects.filter(username = self.kwargs.get('username')).first()
        return Post.objects.filter(author=user).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        quser = Profile.objects.filter(user__username=self.kwargs.get('username')).first()
        total_likes = quser.total_likes()
        liked = False
        if quser.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = super().get_context_data(*args, **kwargs)
        user = User.objects.filter(username = self.kwargs.get('username')).first()
        context["total_likes"] = total_likes
        context["liked"] = liked
        context["postuser"] = user
        return (context)


@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


@login_required
def UserLikeView(request, pk):
    post = get_object_or_404(Profile, user_id=request.POST.get('postuser_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(
        reverse('user-posts', args=[str(post.user.username)]))


class CreateComment(NotificationMixin, CreateView):
    model = Comment
    form_class = AddCommentForm

    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/create_new_comment.html']
        else:
            return ['blog/create-new_comment.html']

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.name = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('close')


class DeleteComment(NotificationMixin, DeleteView):
    model = Comment

    def get_template_names(self):
        profile = Profile.objects.all().first()
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/delete_comment.html']
        else:
            return ['blog/delete_comment.html']
    def get_context_data(self, *args, **kwargs):
        qp = Post.objects.filter(comments=self.kwargs['pk']).first()
        linkpk = qp.id
        context = super().get_context_data(*args, **kwargs)
        context["pklink"] = linkpk
        return context

    def get_success_url(self):
        qp = Post.objects.filter(comments=self.kwargs['pk']).first()
        return reverse('post-detail', kwargs={'pk': qp.id})
