from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm1(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['ip', 'theme', 'notifications', 'bio', 'profile_pic', 'terms', 'layout']
        widgets = {
            'ip': forms.TextInput(attrs={'type': 'hidden'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['theme', 'notifications', 'bio', 'profile_pic', 'terms', 'layout']
        widgets = {
            'ip': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        

        # Add custom Bootstrap-themed styling to checkboxes
        self.fields['terms'].label = 'Do you accept our \"Terms and Conditions\"?'
        self.fields['layout'].label = 'Custom Layout'
        self.fields['notifications'].label = 'Do you want to recieve Notifications?'