from flask import Flask, render_template, request, redirect, url_for, abort
from media_finder import MediaFinder
from datetime import datetime

app = Flask(__name__)

import data_storage

media_finder = MediaFinder()


# Main page
@app.route("/")
def index():
    home_info = data_storage.load_info("main_home")
    return render_template("home.html", home_info=home_info)


# Movie home page
@app.route("/movie-home")
def movie_home():
    movie_info = data_storage.load_info("movie_home")
    return render_template("movie-home.html", movie_info=movie_info)


# Tv home page
@app.route("/tv-home")
def tv_home():
    tv_info = data_storage.load_info("tv_home")
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


# Details of a TV season
@app.route("/<tv_id>/season/<season_number>")
def get_season_detail(tv_id, season_number):
    success, season_detail = media_finder.get_season_detailed_info(tv_id, season_number)
    if success:
        return render_template("tv-season-detail.html", details=season_detail)
    else:
        abort(404)


# Details of a person
@app.route("/person")
def get_person_detail():
    person_detail = media_finder.get_person_detailed_info(request.args.get("id"))
    return render_template("person-detail.html", details=person_detail)


# Credits page
@app.route("/credits")
def credit():
    return render_template("credits.html")


# Search
@app.route("/search/<search_type>", methods=["GET", "POST"])
def search(search_type):
    if search_type == "all":
        query = request.args.get("query")
        success, search_results = media_finder.get_search_query_results(query)

    elif search_type == "by-keywords":
        success, query, search_results = media_finder.search_by_keyword(
            request.args.get("query"), request.args.get("media_type")
        )

    else:
        abort(404)

    return render_template(
        "search-results.html",
        search_results=search_results,
        success=success,
        query=query,
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


# Update the DB
@app.route("/update-db/<code>")
def update_db(code):
    if data_storage.update_all_info(code):
        print(f"DB updated at {datetime.now()}")
        return redirect(url_for("index"))
    else:
        abort(403)


if __name__ == "__main__":
    app.run()
