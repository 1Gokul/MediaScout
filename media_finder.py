import os
import requests
from flask import json, jsonify

MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
BACKDROP_SIZE = 1280
POSTER_SIZE = 300
OVERVIEW_MAX_CHARS = 250


class MediaFinder:
    def __init__(self):
        self.api_key = os.environ.get("MOVIEDB_API_KEY")

    def get_general_info(self, url: str, media_type=None):
        """ Gets info from the api and returns a simplified dict of the data. """
        response = requests.get(f"{url}?api_key={self.api_key}")
        return simplify_response(response.json()["results"], media_type)

    # For the homepage

    def get_trending_movies(self):
        return self.get_general_info("https://api.themoviedb.org/3/trending/movie/week")

    def get_trending_shows(self):
        return self.get_general_info("https://api.themoviedb.org/3/trending/tv/week")

    def get_spotlight(self):
        return self.get_general_info("https://api.themoviedb.org/3/trending/all/day")

    # For movies

    def get_now_playing_movies(self):
        return self.get_general_info(
            "https://api.themoviedb.org/3/movie/now_playing", media_type="movie"
        )

    def get_upcoming_movies(self):
        return self.get_general_info(
            "https://api.themoviedb.org/3/movie/upcoming", media_type="movie"
        )

    def get_popular_movies(self):
        return self.get_general_info(
            "https://api.themoviedb.org/3/movie/popular", media_type="movie"
        )

    def get_top_rated_movies(self):
        return self.get_general_info(
            "https://api.themoviedb.org/3/movie/top_rated", media_type="movie"
        )

    # For TV

    def get_shows_airing_today(self):
        return self.get_general_info(
            "https://api.themoviedb.org/3/tv/airing_today", media_type="tv"
        )

    def get_shows_on_the_air(self):
        return self.get_general_info(
            "https://api.themoviedb.org/3/tv/on_the_air", media_type="tv"
        )

    def get_popular_shows(self):
        return self.get_general_info(
            "https://api.themoviedb.org/3/tv/popular", media_type="tv"
        )

    def get_top_rated_shows(self):
        return self.get_general_info(
            "https://api.themoviedb.org/3/tv/top_rated", media_type="tv"
        )


def simplify_response(response_dict: dict, media_type):
    """ Returns a simplified version of the response with only the basic info of the movies and shows."""

    simplified_response = []
    media_title = ""
    media_date_name = ""

    for media_item in response_dict:

        media_item_data = {}

        # Set the dictionary's key names depending on the type of media
        if media_type == None:
            m_type = media_item["media_type"]

        else:
            m_type = media_type

        if m_type == "movie":
            media_title = "title"
            media_date_name = "release_date"
        else:
            media_title = "name"
            media_date_name = "first_air_date"

        # Add the movie's ID
        media_item_data["id"] = media_item["id"]

        # If the media is not in English, show the media's title in its original language first, followed by its English name in parantheses.
        if media_item["original_language"] != "en" and (
            media_item["original_" + media_title] != media_item[media_title]
        ):
            media_item_data[
                "full_title"
            ] = f"{media_item['original_' + media_title]} ({media_item[media_title]})"

        # else, just show the normal title.
        else:
            media_item_data["full_title"] = media_item[media_title]

        # Add the desctiption and trim it to 250 characters (if larger).
        description = media_item["overview"]
        media_item_data["description"] = (
            (description[:OVERVIEW_MAX_CHARS] + "...")
            if len(description) > (OVERVIEW_MAX_CHARS + 3)
            else description
        )

        # Add the release/air date
        date_list = media_item[media_date_name].split("-")
        media_item_data[
            "date"
        ] = f"{MONTHS[int(date_list[1]) - 1]} {date_list[2]}, {date_list[0]}"

        # Add the rating
        media_item_data["rating"] = (
            "N/A" if media_item["vote_average"] == 0 else media_item["vote_average"]
        )

        # Add a backdrop and a poster
        media_item_data[
            "backdrop"
        ] = f"https://image.tmdb.org/t/p/w{BACKDROP_SIZE}/{media_item['backdrop_path']}"
        media_item_data[
            "poster"
        ] = f"https://image.tmdb.org/t/p/w{POSTER_SIZE}/{media_item['poster_path']}"

        simplified_response.append(media_item_data)

    return simplified_response
