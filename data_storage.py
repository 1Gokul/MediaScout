from pymongo import MongoClient
import os
from dotenv import load_dotenv

from media_finder import MediaFinder

# Load environment variables from either a .env file(dev) or from the environment(production)
load_dotenv()

# URL of the database
client = MongoClient(os.getenv("DATABASE_URL"))
db = client.test_media_data
collection = db.media_data

# MediaFinder Object
media_finder = MediaFinder()


def update_all_info(code):
    """Gets all required data from the TMDB API and updates the information in the database."""
    # If the code supplied is correct, update the database.
    if code == os.getenv("UPDATE_VERIFICATION_CODE"):

        # pymongo transaction
        with client.start_session() as session:
            # start the transaction
            with session.start_transaction():
                main_home = db.media_data.update_one(
                    {"page": "main_home"},
                    {"$set": {"content": get_main_home_info()}},
                    upsert=True,
                )
                movie_home = db.media_data.update_one(
                    {"page": "movie_home"},
                    {"$set": {"content": get_movie_home_info()}},
                    upsert=True,
                )
                tv_home = db.media_data.update_one(
                    {"page": "tv_home"},
                    {"$set": {"content": get_tv_home_info()}},
                    upsert=True,
                )

        return (
            main_home.matched_count + movie_home.matched_count + tv_home.matched_count
        )

    else:
        return None


def load_info(page_name):
    """Return required data from the DB."""
    result = db.media_data.find_one({"page": page_name})
    return result["content"]


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
