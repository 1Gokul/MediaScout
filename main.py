from flask import Flask, render_template, jsonify
from movie_finder import MovieFinder

app = Flask(__name__)

movie_find = MovieFinder()


# main page
@app.route('/')
def index():
    trending_movie_week = movie_find.get_trending_movies()
    trending_tv_week = movie_find.get_trending_shows()
    spotlight = movie_find.get_spotlight()
    return render_template('home.html',
                           trending_movies=trending_movie_week,
                           trending_shows=trending_tv_week,
                           spotlight=spotlight)


@app.route('/movie-home')
def movie_home():
    now_playing_movies = movie_find.get_now_playing_movies()
    upcoming_movies = movie_find.get_upcoming_movies()
    popular_movies = movie_find.get_popular_movies()
    top_rated_movies = movie_find.get_top_rated_movies()

    return render_template('movie_home.html',
                           now_playing_movies=now_playing_movies,
                           upcoming_movies=upcoming_movies,
                           popular_movies=popular_movies,
                           top_rated_movies=top_rated_movies)

@app.route('/movie-details/id=<id>')
def get_movie_detail(id):
    return render_template("movie-detail.html")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
