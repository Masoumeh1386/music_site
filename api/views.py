from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from music.models import Song, Artist, Comment
from .serializers import SongSerializer, ArtistSerializer, CommentSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['artist']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        song = self.get_object()
        user = request.user

        if user in song.likes.all():
            song.likes.remove(user)
            return Response({'status': 'unliked', 'likes_count': song.likes.count()})
        else:
            song.likes.add(user)
            return Response({'status': 'liked', 'likes_count': song.likes.count()})


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['song']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)