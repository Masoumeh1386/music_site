from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'api'

router = DefaultRouter()
router.register('songs', views.SongViewSet, basename='song')
router.register('artists', views.ArtistViewSet, basename='artist')
router.register('comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]