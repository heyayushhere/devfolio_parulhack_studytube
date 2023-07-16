

# Create your models here.
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_id = models.CharField(max_length=50)
    completion_time = models.DateTimeField(default=timezone.now)
    progress = models.ManyToManyField(User, through='UserProgress')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    thumbnail_url = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"



class Playlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video)

    def __str__(self):
        return self.user.username + "'s Playlist"

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


from django.db import models

class FavoriteChannel(models.Model):
    channel_id = models.CharField(max_length=50,default='a')
    name = models.CharField(max_length=100,default='non')

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class UserFavoriteVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_id = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')

    def __str__(self):
        return self.title










