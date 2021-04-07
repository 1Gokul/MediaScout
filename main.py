from flask import Flask, render_template, jsonify, request
from media_finder import MediaFinder

app = Flask(__name__)

media_find = MediaFinder()


# main page
@app.route("/")
def index():
    trending_movie_week = media_find.get_trending_movies()
    trending_tv_week = media_find.get_trending_shows()
    spotlight = media_find.get_spotlight()
    return render_template(
        "home.html",
        trending_movies=trending_movie_week,
        trending_shows=trending_tv_week,
        spotlight=spotlight,
    )


# movie homepage
@app.route("/movie-home")
def movie_home():
    now_playing_movies = media_find.get_now_playing_movies()
    upcoming_movies = media_find.get_upcoming_movies()
    popular_movies = media_find.get_popular_movies()
    top_rated_movies = media_find.get_top_rated_movies()
    documentary_movies = media_find.discover_by_genre("movie", "Documentary")
    print(documentary_movies)
    return render_template(
        "movie_home.html",
        now_playing_movies=now_playing_movies,
        upcoming_movies=upcoming_movies,
        popular_movies=popular_movies,
        top_rated_movies=top_rated_movies,
        documentary_movies=documentary_movies,
    )


# tv homepage
@app.route("/tv-home")
def tv_home():
    shows_on_the_air = media_find.get_shows_on_the_air()
    shows_airing_today = media_find.get_shows_airing_today()
    popular_shows = media_find.get_popular_shows()
    top_rated_shows = media_find.get_top_rated_shows()
    documentary_shows = media_find.discover_by_genre("tv", "Documentary")

    return render_template(
        "tv_home.html",
        shows_on_the_air=shows_on_the_air,
        shows_airing_today=shows_airing_today,
        popular_shows=popular_shows,
        top_rated_shows=top_rated_shows,
        documentary_shows=documentary_shows,
    )


# movie details page
@app.route("/movie-details")
def get_movie_detail():
    return render_template("movie-detail.html")


# tv show details page
@app.route("/tv-show-details")
def get_tv_show_detail():
    return render_template("tv-show-detail.html")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
