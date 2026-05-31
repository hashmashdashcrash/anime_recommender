from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Anime, WatchlistItem


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('anime_list')
    else:
        form = UserCreationForm()

    return render(request, 'anime/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('anime_list')
    else:
        form = AuthenticationForm()

    return render(request, 'anime/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('anime_list')


def anime_list(request):
    search = request.GET.get('search', '')
    genre = request.GET.get('genre', '')

    anime_list = Anime.objects.all().order_by('title')

    if search:
        anime_list = anime_list.filter(title__icontains=search)

    if genre:
        anime_list = anime_list.filter(genres__icontains=genre)

    return render(request, 'anime/anime_list.html', {
        'anime_list': anime_list,
        'search': search,
        'genre': genre
    })


def anime_detail(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    in_watchlist = False

    if request.user.is_authenticated:
        in_watchlist = WatchlistItem.objects.filter(user=request.user, anime=anime).exists()

    return render(request, 'anime/anime_detail.html', {
        'anime': anime,
        'in_watchlist': in_watchlist
    })


@login_required
def watchlist(request):
    items = WatchlistItem.objects.filter(user=request.user).select_related('anime')
    return render(request, 'anime/watchlist.html', {
        'items': items
    })


@login_required
def add_to_watchlist(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    WatchlistItem.objects.get_or_create(user=request.user, anime=anime)
    return redirect('anime_detail', anime_id=anime.id)


@login_required
def remove_from_watchlist(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)
    WatchlistItem.objects.filter(user=request.user, anime=anime).delete()
    return redirect('watchlist')


@login_required
def recommendations(request):
    watchlist_items = WatchlistItem.objects.filter(user=request.user).select_related('anime')
    watched_anime = [item.anime for item in watchlist_items]

    if not watched_anime:
        recommended = Anime.objects.all().order_by('-rating')[:10]
        reason = "These recommendations are based on the highest rated anime because your watchlist is currently empty."
    else:
        user_genres = set()

        for anime in watched_anime:
            for genre in anime.genres.split(','):
                user_genres.add(genre.strip().lower())

        scores = []

        for anime in Anime.objects.exclude(id__in=[a.id for a in watched_anime]):
            anime_genres = set(g.strip().lower() for g in anime.genres.split(','))
            shared_genres = user_genres.intersection(anime_genres)

            if shared_genres:
                score = len(shared_genres) + (anime.rating / 10)
                scores.append((anime, score, ', '.join(shared_genres)))

        scores.sort(key=lambda x: x[1], reverse=True)
        recommended = scores[:10]
        reason = "These recommendations are based on anime that share genres with your watchlist."

    return render(request, 'anime/recommendations.html', {
        'recommended': recommended,
        'reason': reason,
        'has_watchlist': bool(watched_anime)
    })