
from django.db import models
from django.contrib.auth.models import User


class Artist(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='artists/', blank=True, null=True)

    def str(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='songs')
    audio_file = models.FileField(upload_to='songs/')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    release_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='liked_songs',blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.artist.name}"


class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def str(self):
        return f"{self.user.username} - {self.song.title}"