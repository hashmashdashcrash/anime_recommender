from django.urls import path
from . import views

urlpatterns = [
    path('', views.anime_list, name='anime_list'),
    path('anime/<int:anime_id>/', views.anime_detail, name='anime_detail'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add/<int:anime_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove/<int:anime_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('recommendations/', views.recommendations, name='recommendations'),
]