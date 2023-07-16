from .models import Task
from django import forms

from django import forms
from .models import Video
from .models import FavoriteChannel

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_id', 'category', 'sub_category']

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
from django import forms

class FavoriteChannelForm(forms.ModelForm):
    class Meta:
        model = FavoriteChannel
        fields = ['channel_id']
