# Anime Watchlist and Recommendation System

This is my final year project. It is a small Django website for keeping track of anime and getting recommendations.

Users can register, log in, search for anime, and add shows to their own watchlist. They can also give anime a personal rating from 1 to 5. The recommendations page then uses the anime in the user’s watchlist to suggest other shows they might like.

The recommendation part is simple. It looks at the genres from the user’s watchlist and checks for other anime with similar genres. If the user rated something highly, the genres from that anime count a bit more. The normal anime rating is also used so that better rated shows are pushed up slightly.

# Features

* Register and log in
* Search for anime
* Filter by genre
* View anime details
* Add anime to a watchlist
* Remove anime from the watchlist
* Rate anime from 1 to 5
* Get recommendations based on the watchlist and ratings

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

Install the needed packages:

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

The app uses sample anime data.
