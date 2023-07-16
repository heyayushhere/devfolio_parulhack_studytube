from django.shortcuts import render, HttpResponse
from googleapiclient.discovery import build
from django.conf import settings
from .models import Video, UserFavoriteVideo,Playlist

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .models import Task
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'youtube_search/registration/register.html', {'form': form})

def profile(request):
    return render(request, 'youtube_search/registration/profile.html')

def logout_view(request):
    logout(request)
    return redirect('login')
def test(request):
    return render(request,'youtube_search/test/home-v3.html')

# Rest of the code for search_videos and favorite_video views...
# views.py

# Import the AuthenticationForm class
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'youtube_search/registration/login.html', {'form': form})


def search_videos(request):
    videos = []
    recommendations = []

    categories = Category.objects.all()  # Fetch all categories

    if 'q' in request.GET:
        query = request.GET['q']
        category_id = request.GET.get('category')  # Get selected category ID
        
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        
        search_params = {
            'q': query,
            'part': 'snippet',
            'maxResults': 15,
            'type': 'video',
        }
        
        if category_id:
            search_params['videoCategoryId'] = category_id  # Apply category filter
        
        response = youtube.search().list(**search_params).execute()

        for item in response['items']:
            video_id = item['id'].get('videoId')
            if video_id:
                title = item['snippet']['title']
                description = item['snippet']['description']
                video = Video(title=title, description=description, video_id=video_id)
                
                # Fetch the thumbnail image URL
                thumbnails = item['snippet']['thumbnails']
                thumbnail_url = thumbnails['high']['url']  # Change 'high' to the desired size
        
                video.thumbnail_url = thumbnail_url
                videos.append(video)

        # Save videos to the database
        Video.objects.bulk_create(videos)

        # Get video recommendations based on the search query
        recommendations_response = youtube.search().list(
                q=query,
                part='snippet',
                maxResults=10,
                type='video'
            ).execute()

        for item in recommendations_response['items']:
            video_id = item['id'].get('videoId')
            if video_id:
                title = item['snippet']['title']
                description = item['snippet']['description']
                thumbnail_url = item['snippet']['thumbnails']['high']['url']
                recommendation = Video(title=title, description=description, video_id=video_id, thumbnail_url=thumbnail_url)
                recommendations.append(recommendation)

    return render(request, 'youtube_search/search.html', {'videos': videos, 'categories': categories, 'recommendations': recommendations})


def add_to_playlist(request, video_id):
    playlist, created = Playlist.objects.get_or_create(user=request.user)
    video = Video.objects.filter(video_id=video_id).first()
    playlist.videos.add(video)
    return redirect('my_playlist')
def index(request):
    return render(request,'youtube_search/index.html')
def focus(request):
    return render(request,'youtube_search/focus.html')






def my_playlist(request):
    playlist = Playlist.objects.filter(user=request.user).first()  # Retrieve the user's playlist
    context = {'playlist': playlist}
    return render(request, 'youtube_search/my_playlist.html', context)

from django.shortcuts import render, redirect
from .forms import TaskForm


def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'youtube_search/task_list.html', {'tasks': tasks})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'youtube_search/create_task.html', {'form': form})

def update_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'youtube_search/update_task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('youtube_search/task_list')


# views.py

from googleapiclient.discovery import build
from django.conf import settings
from .models import Video


   
# views.py

from django.shortcuts import render, redirect
from googleapiclient.discovery import build
from django.conf import settings
from .models import Video

def add_video(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        search_query = request.POST['search_query']
        completion_time = request.POST['completion_time']

        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        response = youtube.search().list(
            q=search_query,
            part='snippet',
            maxResults=1
        ).execute()

        video_id = None

        if 'items' in response and len(response['items']) > 0:
            video_id = response['items'][0]['id'].get('videoId')

        if video_id:
            video = Video(title=title, description=description, video_id=video_id, completion_time=completion_time)
            video.save()
            return redirect('profile')

    return render(request, 'youtube_search/add_video.html')



from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Video, UserProgress
from django.utils import timezone

@login_required
def watch_video(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    user = request.user

    # Check if the user has already started watching the video
    user_progress, created = UserProgress.objects.get_or_create(user=user, video=video)

    if created:
        # User just started watching the video
        user_progress.started_at = timezone.now()
        user_progress.save()

    if request.method == 'POST':
        if 'complete' in request.POST:
            # User completed watching the video
            user_progress.completed_at = timezone.now()
            user_progress.save()

    # Render the template with the video and user's progress
    return render(request, 'youtube_search/watch-video.html', {'video': video, 'user_progress': user_progress})




# testing

from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import Category, SubCategory

def create_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST)
        if form.is_valid():
            video = form.save()
            return redirect('video_detail', video_id=video.id)
    else:
        form = VideoForm()
    
    return render(request, 'youtube_search/create_video.html', {'form': form})

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    return render(request, 'youtube_search/subcategory_options.html', {'subcategories': subcategories})




def video(request, video_id):
    videos = Video.objects.filter(video_id=video_id)
    
    if videos.exists():
        video = videos.first()
    else:
        raise Http404("Video not found")

    recommendations = []

    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

    # Get video recommendations based on the selected video
    recommendations_response = youtube.search().list(
        relatedToVideoId=video_id,
        part='snippet',
        maxResults=10,
        type='video'
    ).execute()

    for item in recommendations_response['items']:
        video_id = item['id'].get('videoId')
        if video_id:
            title = item['snippet']['title']
            description = item['snippet']['description'][:200]  # Limit description to 200 characters
            thumbnail_url = item['snippet']['thumbnails']['high']['url']  # Change 'high' to the desired size

            recommendation = Video(title=title, description=description, video_id=video_id, thumbnail_url=thumbnail_url)
            recommendations.append(recommendation)

    return render(request, 'youtube_search/video.html', {'video': video, 'video_id': video_id, 'recommendations': recommendations})
    
def ip(request):
    return render(request,'youtube_search\sidebar.html' )
from django.shortcuts import render, get_object_or_404
from youtube_search.models import Video

def video_details(request, video_id):
    
    recommendations = Video.objects.exclude(video_id=video_id).order_by('?')[:10]

    return render(request, 'youtube_search/video.html', {'video': video, 'recommendations': recommendations})




from django.shortcuts import render, redirect
from .forms import FavoriteChannelForm

def add_favorite_channel(request):
    if request.method == 'POST':
        form = FavoriteChannelForm(request.POST)
        if form.is_valid():
            favorite_channel = form.save(commit=False)
            favorite_channel.user = request.user
            favorite_channel.save()
            return redirect('favorite_videos')
    else:
        form = FavoriteChannelForm()
    return render(request, 'youtube_search/add_favorite_channel.html', {'form': form})

from django.shortcuts import render
from .models import FavoriteChannel, Video

def favorite_videos(request):
    videos = FavoriteVideo.objects.filter(user=request.user)
    favorite_channels = FavoriteChannel.objects.filter(user=request.user)
    videos = []
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

    for favorite_channel in favorite_channels:
        channel_id = favorite_channel.channel_id

        playlist_response = youtube.channels().list(
            id=channel_id,
            part='contentDetails'
        ).execute()

        playlist_id = playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        playlist_items_response = youtube.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=15
        ).execute()

        for item in playlist_items_response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            thumbnail_url = item['snippet']['thumbnails']['high']['url']
            video = Video(title=title, description=description, video_id=video_id, thumbnail_url=thumbnail_url)
            videos.append(video)

    return render(request, 'youtube_search/favorite_videos.html', {'videos': videos})


# views.py


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from django.shortcuts import render

def search_channels(request):
    query = request.GET.get('query')
    channels = []

    if query:
        try:
            youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
            search_response = youtube.search().list(
                q=query,
                part='snippet',
                type='channel',
                maxResults=10
            ).execute()

            for item in search_response['items']:
                channel_id = item['id']['channelId']
                title = item['snippet']['title']
                description = item['snippet']['description']
                thumbnail_url = item['snippet']['thumbnails']['high']['url']
                channels.append({
                    'channel_id': channel_id,
                    'title': title,
                    'description': description,
                    'thumbnail_url': thumbnail_url
                })

        except HttpError as e:
            # Handle any errors that occur during the API request
            error_message = str(e)
            # Handle the error as per your requirements

    return render(request, 'youtube_search/search_channels.html', {'channels': channels, 'query': query})

def channel_videos(request, channel_id):
    videos = []
    try:
        youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
        videos_response = youtube.search().list(
            channelId=channel_id,
            part='snippet',
            type='video',
            maxResults=10
        ).execute()

        for item in videos_response['items']:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            thumbnail_url = item['snippet']['thumbnails']['high']['url']
            videos.append({
                'video_id': video_id,
                'title': title,
                'description': description,
                'thumbnail_url': thumbnail_url
            })

    except HttpError as e:
        # Handle any errors that occur during the API request
        error_message = str(e)
        # Handle the error as per your requirements

    return render(request, 'youtube_search/channel_videos.html', {'videos': videos, 'channel_id': channel_id})
