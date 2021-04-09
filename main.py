from flask import Flask, render_template, jsonify, request
from media_finder import MediaFinder

app = Flask(__name__)

media_find = MediaFinder()


# main page
@app.route("/")
def index():
    home_info = get_main_home_info()
    return render_template("home.html", home_info=home_info)


# movie homepage
@app.route("/movie-home")
def movie_home():
    movie_info = get_movie_home_info()
    return render_template("movie-home.html", movie_info=movie_info)


# tv homepage
@app.route("/tv-home")
def tv_home():
    tv_info = get_tv_home_info()
    return render_template("tv-home.html", tv_info=tv_info)


# movie details page
@app.route("/movie-details")
def get_movie_detail():
    return render_template("movie-detail.html")


# tv show details page
@app.route("/tv-show-details")
def get_tv_show_detail():
    return render_template("tv-show-detail.html")


def get_main_home_info():
    info_dict = {
        "trending_movie_week": media_find.info_by_category(
            category_before="trending", media_type="movie", category_after="week"
        ),
        "trending_shows_week": media_find.info_by_category(
            category_before="trending", media_type="tv", category_after="week"
        ),
        "spotlight": media_find.info_by_category(
            category_before="trending", media_type="all", category_after="day"
        ),
        "documentary_movies": media_find.discover_by_genre("movie", "Documentary"),
        "crime_shows": media_find.discover_by_genre("tv", "Crime"),
        "war_politics_shows": media_find.discover_by_genre("tv", "War & Politics"),
        "family_movies": media_find.discover_by_genre("movie", "Family"),
    }
    return info_dict


def get_tv_home_info():
    info_dict = {
        "shows_on_the_air": media_find.info_by_category(
            category_after="on_the_air", media_type="tv"
        ),
        "shows_airing_today": media_find.info_by_category(
            category_after="airing_today", media_type="tv"
        ),
        "popular_shows": media_find.info_by_category(
            category_after="popular", media_type="tv"
        ),
        "top_rated_shows": media_find.info_by_category(
            category_after="top_rated", media_type="tv"
        ),
        "documentary_shows": media_find.discover_by_genre("tv", "Documentary"),
        "animated_shows": media_find.discover_by_genre("tv", "Animation"),
        "action_adventure_shows": media_find.discover_by_genre(
            "tv", "Action & Adventure"
        ),
        "kids_shows": media_find.discover_by_genre("tv", "Kids"),
        "mystery_shows": media_find.discover_by_genre("tv", "Mystery"),
        "reality_shows": media_find.discover_by_genre("tv", "Reality"),
    }

    return info_dict


def get_movie_home_info():
    info_dict = {
        "now_playing_movies": media_find.info_by_category(
            category_after="now_playing", media_type="movie"
        ),
        "upcoming_movies": media_find.info_by_category(
            category_after="upcoming", media_type="movie"
        ),
        "top_rated_movies": media_find.info_by_category(
            category_after="top_rated", media_type="movie"
        ),
        "popular_movies": media_find.info_by_category(
            category_after="popular", media_type="movie"
        ),
        "documentary_movies": media_find.discover_by_genre("movie", "Documentary"),
        "comedy_movies": media_find.discover_by_genre("movie", "Comedy"),
        "mystery_movies": media_find.discover_by_genre("movie", "Mystery"),
        "western_movies": media_find.discover_by_genre("movie", "Western"),
        "drama_movies": media_find.discover_by_genre("movie", "Drama"),
        "crime_movies": media_find.discover_by_genre("movie", "Crime"),
    }

    return info_dict


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
