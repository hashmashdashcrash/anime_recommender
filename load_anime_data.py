import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime_project.settings')
django.setup()

from anime.models import Anime

anime_data = [
    ("Attack on Titan", "Action, Drama, Fantasy", 9.1, 87, "Humanity fights for survival against giant humanoid creatures."),
    ("Death Note", "Mystery, Psychological, Supernatural", 9.0, 37, "A student finds a notebook that can kill people and is chased by a detective."),
    ("Fullmetal Alchemist Brotherhood", "Action, Adventure, Fantasy", 9.1, 64, "Two brothers search for a way to restore their bodies after a failed experiment."),
    ("Demon Slayer", "Action, Fantasy, Adventure", 8.6, 55, "A young swordsman fights demons while trying to save his sister."),
    ("Jujutsu Kaisen", "Action, Supernatural, Fantasy", 8.7, 47, "A student joins sorcerers to fight curses after swallowing a cursed object."),
    ("Naruto", "Action, Adventure, Shounen", 8.4, 220, "A young ninja tries to gain recognition and become village leader."),
    ("One Piece", "Adventure, Action, Comedy", 8.9, 1000, "A pirate crew searches for the legendary treasure known as One Piece."),
    ("Hunter x Hunter", "Adventure, Action, Fantasy", 9.0, 148, "A boy becomes a hunter and searches for his father."),
    ("Steins Gate", "Sci-Fi, Thriller, Drama", 9.0, 24, "A group of friends accidentally discover a way to send messages through time."),
    ("Code Geass", "Action, Mecha, Drama", 8.8, 50, "A prince gains a mysterious power and leads a rebellion."),
    ("Your Lie in April", "Romance, Drama, Music", 8.7, 22, "A former piano prodigy rediscovers music after meeting a violinist."),
    ("Toradora", "Romance, Comedy, Slice of Life", 8.1, 25, "Two students help each other pursue their crushes."),
    ("Kaguya-sama Love is War", "Romance, Comedy, School", 8.6, 37, "Two student council members try to make each other confess first."),
    ("Violet Evergarden", "Drama, Slice of Life, Fantasy", 8.7, 13, "A former soldier learns about emotions while writing letters."),
    ("Cowboy Bebop", "Action, Sci-Fi, Adventure", 8.8, 26, "Bounty hunters travel through space while confronting their pasts."),
    ("Mob Psycho 100", "Action, Comedy, Supernatural", 8.6, 37, "A quiet boy with psychic powers tries to live normally."),
    ("Vinland Saga", "Action, Historical, Drama", 8.8, 48, "A young warrior becomes caught in revenge, war, and meaning."),
    ("Spy x Family", "Comedy, Action, Slice of Life", 8.5, 37, "A spy forms a fake family for a mission."),
    ("Haikyuu", "Sports, Comedy, Drama", 8.7, 85, "A short volleyball player works to become a strong competitor."),
    ("Blue Lock", "Sports, Action, Drama", 8.2, 24, "Football players compete to become Japan's best striker."),
]

for title, genres, rating, episodes, synopsis in anime_data:
    Anime.objects.get_or_create(
        title=title,
        defaults={
            "genres": genres,
            "rating": rating,
            "episodes": episodes,
            "synopsis": synopsis,
        }
    )

print("Anime data loaded successfully.")