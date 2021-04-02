from flask import Flask, render_template, jsonify
from movie_finder import MovieFinder

app = Flask(__name__)

movie_find = MovieFinder()


# main page
@app.route('/')
def index():
    trending_all_week = movie_find.get_trending()
    return render_template('home.html', trending_all_week=trending_all_week)


if __name__ == '__main__':
    app.run(threaded=True)
