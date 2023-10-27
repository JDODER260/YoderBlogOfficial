from django import forms
from .models import Chat, Room


class ChatForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder': 'Type your message here...',
            'class': 'form-control',
            'aria-label': 'Type your message here...',
            'aria-describedby': 'send-button',
            'rows': 1,
            'data-emojiable': True
        }))

    class Meta:
        model = Chat
        fields = ('content', 'person_to', 'author')
        widgets = {
            'person_to':
            forms.HiddenInput(attrs={
                'id': 'person_to',
                'class': 'smallthings'
            }),
            'author':
            forms.HiddenInput(attrs={
                'id': 'author',
                'class': 'smallthings'
            }),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'allow_all_users', 'allowed_users']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['allowed_users'].widget.attrs.update(
            {'class': 'form-control'})

