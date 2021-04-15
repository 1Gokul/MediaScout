from main import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from media_finder import MediaFinder
import os

# URL of the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace(
    "://", "ql://", 1
)

# Optional: But it silences the deprecation warning in the console.
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# The Data table
class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(50), unique=True, nullable=False)
    page_data = db.Column(JSON)


db.create_all()

# MediaFinder Object
media_finder = MediaFinder()


class DataStorage:
    def update_all_info(self, code):
        """ Gets all required data from the TMDB API and updates the information in the database. """

        # If the code supplied is correct, update the database.
        if code == os.environ.get("UPDATE_VERIFICATION_CODE"):

            # Clear all previous data from the data table
            db.session.query(Media).delete()

            # Add the data for the main homepage
            main_home = Media(page_name="main_home", page_data=get_main_home_info())
            db.session.add(main_home)

            # Add the data for the movie homepage
            movie_home = Media(page_name="movie_home", page_data=get_movie_home_info())
            db.session.add(movie_home)

            # Add the data for the tv homepage
            tv_home = Media(page_name="tv_home", page_data=get_tv_home_info())
            db.session.add(tv_home)

            db.session.commit()

            return True

        else:
            return False

    def load_info(self, page_name):
        """ Return required data from the DB. """
        result = Media.query.filter_by(page_name=page_name).first()
        return result.page_data


def get_main_home_info():
    info_dict = {
        "trending_movie_week": media_finder.info_by_category(
            category_before="trending", media_type="movie", category_after="week"
        ),
        "trending_shows_week": media_finder.info_by_category(
            category_before="trending", media_type="tv", category_after="week"
        ),
        "spotlight": media_finder.info_by_category(
            category_before="trending", media_type="all", category_after="day"
        ),
        "documentary_movies": media_finder.discover_by_genre("movie", "Documentary"),
        "crime_shows": media_finder.discover_by_genre("tv", "Crime"),
        "war_politics_shows": media_finder.discover_by_genre("tv", "War & Politics"),
        "family_movies": media_finder.discover_by_genre("movie", "Family"),
    }
    return info_dict


def get_tv_home_info():
    info_dict = {
        "shows_on_the_air": media_finder.info_by_category(
            category_after="on_the_air", media_type="tv"
        ),
        "shows_airing_today": media_finder.info_by_category(
            category_after="airing_today", media_type="tv"
        ),
        "popular_shows": media_finder.info_by_category(
            category_after="popular", media_type="tv"
        ),
        "top_rated_shows": media_finder.info_by_category(
            category_after="top_rated", media_type="tv"
        ),
        "documentary_shows": media_finder.discover_by_genre("tv", "Documentary"),
        "animated_shows": media_finder.discover_by_genre("tv", "Animation"),
        "action_adventure_shows": media_finder.discover_by_genre(
            "tv", "Action & Adventure"
        ),
        "kids_shows": media_finder.discover_by_genre("tv", "Kids"),
        "mystery_shows": media_finder.discover_by_genre("tv", "Mystery"),
        "reality_shows": media_finder.discover_by_genre("tv", "Reality"),
    }

    return info_dict


def get_movie_home_info():
    info_dict = {
        "now_playing_movies": media_finder.info_by_category(
            category_after="now_playing", media_type="movie"
        ),
        "upcoming_movies": media_finder.info_by_category(
            category_after="upcoming", media_type="movie"
        ),
        "top_rated_movies": media_finder.info_by_category(
            category_after="top_rated", media_type="movie"
        ),
        "popular_movies": media_finder.info_by_category(
            category_after="popular", media_type="movie"
        ),
        "documentary_movies": media_finder.discover_by_genre("movie", "Documentary"),
        "comedy_movies": media_finder.discover_by_genre("movie", "Comedy"),
        "mystery_movies": media_finder.discover_by_genre("movie", "Mystery"),
        "western_movies": media_finder.discover_by_genre("movie", "Western"),
        "drama_movies": media_finder.discover_by_genre("movie", "Drama"),
        "crime_movies": media_finder.discover_by_genre("movie", "Crime"),
    }

    return info_dict
