from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.SongListView.as_view(), name='song_list'),
    path('song/<int:pk>/', views.SongDetailView.as_view(), name='song_detail'),
    path('artists/', views.ArtistListView.as_view(), name='artist_list'),
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('song/add/', views.SongCreateView.as_view(), name='song_add'),
    path('song/<int:pk>/edit/', views.SongUpdateView.as_view(), name='song_edit'),
    path('song/<int:pk>/delete/', views.SongDeleteView.as_view(), name='song_delete'),
    path('my-songs/', views.MyLikedSongsView.as_view(), name='my_liked_songs'),
    path('song/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('my-songs/', views.MyLikedSongsView.as_view(), name='my_liked_songs'),
    path('search/', views.SearchView.as_view(), name='search'),
    ]
