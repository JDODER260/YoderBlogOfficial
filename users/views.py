from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView, ListView
from django.views.decorators.csrf import csrf_exempt
from main.models import Category
from chat.models import Chat
import operator
import json
from django.urls import reverse
from .utils import NotificationMixin
from django.db.models import Max
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from .models import Profile
from django.utils import timezone


def location_view(request, username):
    profile = Profile.objects.filter(user__username=username).first()
    if not profile:
        return render(request, 'error/404.html', {'error': 'User not found'})
    if not profile.gps_coords:
        return render(request, 'error/404.html', {'error': 'GPS coordinates not found'})
    gps_coords = profile.gps_coords.split(',')
    print(gps_coords)
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(request, 'users/location.html', {'lat': gps_coords[0], 'long': gps_coords[1]})
        else:
            return render(request, 'themetwo/users/location.html', {'lat': gps_coords[0], 'long': gps_coords[1]})
    else:
        return render(request, 'users/location.html', {'lat': gps_coords[0], 'long': gps_coords[1]})


@user_passes_test(lambda u: u.is_superuser)
def admin_location_view(request):
    gps_coords = request.user.profile.gps_coords
    if not gps_coords:
        return render(request, '404.html', {'error': 'GPS coordinates not found'})
    gps_coords = gps_coords.split(',')
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(request, 'users/location.html', {'lat': gps_coords[0], 'long': gps_coords[1]})
        else:
            return render(request, 'themetwo/users/location.html', {'lat': gps_coords[0], 'long': gps_coords[1]})
    else:
        return render(request, 'users/location.html', {'lat': gps_coords[0], 'long': gps_coords[1]})


@login_required
@csrf_exempt
def update_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lat = data['lat']
        lng = data['lng']
        request.user.profile.gps_coords = f"{lat},{lng}"
        request.user.profile.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if username != "Admin" or username != "admin" or username != "Administrator" or username != "administrator" or username != "Admin " or username != "admin " or username != "Administrator " or username != "administrator ":
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(
                    request, f'You have successfully created a new account with the username {username}')
            else:
                messages.warning(
                    request, 'You are not allowed a username like that!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            print("Not")
            return render(request, 'users/register.html', {'form': form})
        else:
            print("IS")
            return render(request, 'themetwo/users/register.html', {'form': form})
    else:
        return render(request, 'users/register.html', {'form': form})



@login_required
def profile(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            profile = p_form.save(commit=False)
            profile.ip = ip
            profile.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(request, 'users/profile.html', context)
        else:
            return render(request, 'themetwo/users/profile.html', context)
    else:
        return render(request, 'users/profile.html', context)


class DeleteUser(NotificationMixin, DeleteView):
    model = User
    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/users/delete.html']
        else:
            return ['users/delete.html']

    def get_success_url(self):
        return reverse('blog-home')


class ShowUsers(NotificationMixin, ListView):
    model = User
    def get_template_names(self):
        profile = Profile.objects.all().first()
        profile.layout = False
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
        if profile.layout:
            return ['themetwo/users/users.html']
        else:
            return ['users/users.html']
    context_object_name = 'users'

    def get_queryset(self):
        queryset = User.objects.all()
        for i in queryset:
            if i.profile.last_active:
                i.profile.are_active = (timezone.now() - i.profile.last_active).total_seconds() <= 420
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        num_registered_users = User.objects.count()

    # Get the number of active users (last_active within the last 7 minutes)
        active_threshold = timezone.now() - timezone.timedelta(minutes=7)
        active_users = User.objects.filter(profile__last_active__gte=active_threshold)
        context['active_users'] = active_users
        context['number_of_users'] = num_registered_users
        return context


def terms(request):
    if request.user.is_authenticated:
        if not request.user.profile.layout:
            return render(request, 'error/terms.html')
        else:
            return render(request, 'themetwo/error/terms.html')
    else:
        return render(request, 'error/terms.html')

