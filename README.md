# Anime Watchlist and Recommendation System

This is my final year project. It is a small Django website for keeping track of anime and getting basic recommendations.

The user can make an account, log in, search through the anime list, and add shows to their watchlist. There is also a recommendations page which suggests anime based on the genres of the shows already in the user’s watchlist.

The recommendation system is fairly simple. It checks what genres the user seems to like, then finds other anime with similar genres. The rating is also used so that higher rated anime are pushed up a bit more. It is not meant to be as advanced as something like MyAnimeList or Netflix, but it shows the main idea of a recommendation system.

# Features

* Register and log in
* Search for anime
* Filter by genre
* View anime details
* Add anime to a watchlist
* Remove anime from the watchlist
* Get recommendations from the watchlist

# What I used

* Python
* Django
* SQLite
* HTML and CSS
* GitHub

# Running the project

Open the folder in VS Code and activate the virtual environment:

```bash
venv\Scripts\activate
```

Then install the needed packages:

```bash
pip install django pandas scikit-learn pillow
```

Run the database migrations:

```bash
python manage.py migrate
```

Load the anime data:

```bash
python load_anime_data.py
```

Start the server:

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

# Extra note

The app currently uses sample anime data. 