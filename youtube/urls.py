from django.contrib import admin
from django.urls import path, include
from youtube_search import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from youtube_search.views import add_to_playlist,my_playlist,task_list, create_task, update_task,login_view,add_video,watch_video,search_videos,ip,add_favorite_channel,favorite_videos

from youtube_search.views import watch_video,video,add_favorite_channel,search_channels,channel_videos,index,focus,aboutus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('side/', views.ip,name='side'),
    path('', views.index,name='index'),
    path('aboutus/', views.aboutus,name='aboutus'),
    path('focus/', views.focus,name='focus'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('search/', views.search_videos, name='search_videos'),                                       
    path('add-to-playlist/<str:video_id>/', views.add_to_playlist, name='add_to_playlist'),

    path('my-playlist/', my_playlist, name='my_playlist'), 
    path('tasks/', task_list, name='task_list'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/update/<int:pk>/', update_task, name='update_task'),
    path('test/',views.test,name='test'),
    path('login/', views.login_view, name='login'),
    path('add-video/', add_video, name='add_video'),
    path('video/<int:video_id>/', watch_video, name='watch_video'),
    path('create_video/', views.create_video, name='create_video'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('video/<str:video_id>/', video, name='video'),
    path('favorite-channels/', views.add_favorite_channel, name='favorite_channels'),
    path('favorite-videos/', views.favorite_videos, name='favorite_videos'),
    path('search-channels/', views.search_channels, name='search_channels'),
    path('channel-videos/<slug:channel_id>/', channel_videos, name='channel_videos'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
