from flask import Flask, render_template, jsonify, request, redirect, url_for, abort
from media_finder import MediaFinder
import os

app = Flask(__name__)

from data_storage import DataStorage

data_manager = DataStorage()
media_finder = MediaFinder()


# main page
@app.route("/")
def index():
    home_info = data_manager.load_info("main_home")
    return render_template("home.html", home_info=home_info)


# movie homepage
@app.route("/movie-home")
def movie_home():
    movie_info = data_manager.load_info("movie_home")
    return render_template("movie-home.html", movie_info=movie_info)


# tv homepage
@app.route("/tv-home")
def tv_home():
    tv_info = data_manager.load_info("tv_home")
    return render_template("tv-home.html", tv_info=tv_info)


# movie details page
@app.route("/movie-details")
def get_movie_detail():
    movie_detail = media_finder.get_media_detailed_info("movie", request.args.get("id"))
    return render_template("movie-detail.html", details=movie_detail)


# tv show details page
@app.route("/tv-show-details")
def get_tv_detail():
    show_detail = media_finder.get_media_detailed_info("tv", request.args.get("id"))
    return render_template("tv-show-detail.html", details=show_detail)


# credits page
@app.route("/credits")
def credit():
    return render_template("credits.html")


# db updater
@app.route("/update-db/<code>")
def update_db(code):
    if data_manager.update_all_info(code):
        return redirect(url_for("index"))
    else:
        abort(403)


# 404
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# 403
@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403


if __name__ == "__main__":
    app.run(debug=True)
