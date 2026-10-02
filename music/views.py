

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Song, Artist
from .forms import SongForm,SearchForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.edit import FormMixin


class SongListView(ListView):
    model = Song
    template_name = 'music/song_list.html'
    context_object_name = 'songs'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'همه‌ی آهنگ‌ها'
        return context





class SongDetailView(FormMixin, DetailView):
    model = Song
    template_name = 'music/song_detail.html'
    context_object_name = 'song'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('music:song_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = self.object.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.song = self.object
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)


class ArtistListView(ListView):
    model = Artist
    template_name = 'music/artist_list.html'
    context_object_name = 'artists'


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'music/artist_detail.html'
    context_object_name = 'artist'





class SongCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Song
    form_class = SongForm
    template_name = 'music/song_form.html'
    success_url = reverse_lazy('music:song_list')

    def test_func(self):
        return self.request.user.is_staff


class SongUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Song
    form_class = SongForm
    template_name = 'music/song_form.html'
    success_url = reverse_lazy('music:song_list')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'ویرایش آهنگ'
        context['submit_label'] = 'ذخیره تغییرات'
        return context



class SongDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Song
    template_name = 'music/song_confirm_delete.html'
    success_url = reverse_lazy('music:song_list')

    def test_func(self):
        return self.request.user.is_staff





class MyLikedSongsView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'music/my_liked_songs.html'
    context_object_name = 'songs'

    def get_queryset(self):
        return self.request.user.liked_songs.all()




@login_required
def toggle_like(request, pk):
    song = get_object_or_404(Song, pk=pk)

    if request.user in song.likes.all():
        song.likes.remove(request.user)
    else:
        song.likes.add(request.user)

    return redirect('music:song_detail', pk=song.pk)




class SearchView(FormView):
    template_name = 'music/search.html'
    form_class = SearchForm
    success_url = reverse_lazy('music:search')

    def form_valid(self, form):
        query = form.cleaned_data['query']
        songs = Song.objects.filter(title__icontains=query)

        return self.render_to_response(
            self.get_context_data(form=form, songs=songs, query=query)
        )