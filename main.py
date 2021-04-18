from flask import Flask, render_template, jsonify, request, redirect, url_for, abort
from media_finder import MediaFinder
import os

app = Flask(__name__)

from data_storage import DataStorage

data_manager = DataStorage()
media_finder = MediaFinder()


# Main page
@app.route("/")
def index():
    home_info = data_manager.load_info("main_home")
    return render_template("home.html", home_info=home_info)


# Movie home page
@app.route("/movie-home")
def movie_home():
    movie_info = data_manager.load_info("movie_home")
    return render_template("movie-home.html", movie_info=movie_info)


# Tv home page
@app.route("/tv-home")
def tv_home():
    tv_info = data_manager.load_info("tv_home")
    return render_template("tv-home.html", tv_info=tv_info)


# Details of a Movie
@app.route("/movie")
def get_movie_detail():
    movie_detail = media_finder.get_media_detailed_info("movie", request.args.get("id"))
    return render_template("movie-detail.html", details=movie_detail)


# Details of a TV Show
@app.route("/tv-show")
def get_tv_detail():
    show_detail = media_finder.get_media_detailed_info("tv", request.args.get("id"))
    return render_template("tv-show-detail.html", details=show_detail)


# Details of a person
@app.route("/person")
def get_person_detail():
    person_detail = media_finder.get_person_detailed_info(request.args.get("id"))
    return render_template("person-detail.html", details=person_detail)


# Credits page
@app.route("/credits")
def credit():
    return render_template("credits.html")


# DB updater
@app.route("/update-db/<code>")
def update_db(code):
    if data_manager.update_all_info(code):
        return redirect(url_for("index"))
    else:
        abort(403)


# Search
@app.route("/search/<search_type>", methods=["GET", "POST"])
def search(search_type):
    if request.method == "POST":
        search_results = media_finder.get_search_results(
            request.form.get("query"), search_type
        )
        return render_template(
            "search-results.html",
            search_results=search_results,
            query=request.form.get("query"),
            search_type=search_type,
        )


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
