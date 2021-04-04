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


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
