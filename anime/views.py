from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Anime, WatchlistItem, AnimeRating


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
    user_rating = None

    if request.user.is_authenticated:
        in_watchlist = WatchlistItem.objects.filter(user=request.user, anime=anime).exists()
        user_rating = AnimeRating.objects.filter(user=request.user, anime=anime).first()

    return render(request, 'anime/anime_detail.html', {
        'anime': anime,
        'in_watchlist': in_watchlist,
        'user_rating': user_rating
    })


@login_required
def rate_anime(request, anime_id):
    anime = get_object_or_404(Anime, id=anime_id)

    if request.method == 'POST':
        score = int(request.POST.get('score', 3))

        if score < 1:
            score = 1
        elif score > 5:
            score = 5

        rating, created = AnimeRating.objects.get_or_create(
            user=request.user,
            anime=anime,
            defaults={'score': score}
        )

        if not created:
            rating.score = score
            rating.save()

    return redirect('anime_detail', anime_id=anime.id)


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

        return render(request, 'anime/recommendations.html', {
            'recommended': recommended,
            'reason': reason,
            'has_watchlist': False
        })

    genre_scores = {}

    for anime in watched_anime:
        user_rating = AnimeRating.objects.filter(user=request.user, anime=anime).first()

        if user_rating:
            weight = user_rating.score
        else:
            weight = 3

        for genre in anime.genres.split(','):
            genre = genre.strip().lower()

            if genre:
                genre_scores[genre] = genre_scores.get(genre, 0) + weight

    scores = []

    for anime in Anime.objects.exclude(id__in=[a.id for a in watched_anime]):
        anime_genres = set(g.strip().lower() for g in anime.genres.split(','))
        shared_genres = anime_genres.intersection(genre_scores.keys())

        if shared_genres:
            genre_score = sum(genre_scores[genre] for genre in shared_genres)
            final_score = genre_score + (anime.rating / 10)
            scores.append((anime, final_score, ', '.join(shared_genres)))

    scores.sort(key=lambda x: x[1], reverse=True)
    recommended = scores[:10]

    reason = "These recommendations are based on your watchlist, your personal ratings, shared genres, and the anime's general rating."

    return render(request, 'anime/recommendations.html', {
        'recommended': recommended,
        'reason': reason,
        'has_watchlist': True
    })