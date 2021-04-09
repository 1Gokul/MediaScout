import os
import requests
from flask import json, jsonify, url_for
import requests_cache

requests_cache.install_cache("mediascout_cache", backend="sqlite", expire_after=1800)

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

GENRES = {
    "Action & Adventure": 10759,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Kids": 10762,
    "Mystery": 9648,
    "News": 10763,
    "Reality": 10764,
    "Sci-Fi & Fantasy": 10765,
    "Soap": 10766,
    "Talk": 10767,
    "War & Politics": 10768,
    "Western": 37,
}

BACKDROP_SIZE = 1280
POSTER_SIZE = 300
OVERVIEW_MAX_CHARS = 250


class MediaFinder:
    def __init__(self):
        self.api_key = os.environ.get("MOVIEDB_API_KEY")

    def get_general_info(self, url: str, additional_args: str = "", media_type=None):
        """ Gets info from the api and returns a simplified dict of the data. """

        response = requests.get(f"{url}?api_key={self.api_key}{additional_args}")
        return simplify_response(response.json()["results"], media_type)

    def get_info_for_grid(self, url: str, additional_args: str = "", media_type=None):
        """ Gets the info required for showing in the poster grids (i.e. only the poster and movie ID)."""

        response = requests.get(
            f"{url}?api_key={self.api_key}{additional_args}"
        ).json()["results"]

        info_dict = []

        for media_item in response:

            item_data_to_add = {"id": media_item["id"]}

            if media_item["poster_path"] == None:
                item_data_to_add["poster"] = url_for(
                    "static", filename="img/no_poster.png"
                )
            else:
                item_data_to_add[
                    "poster"
                ] = f"https://image.tmdb.org/t/p/w{POSTER_SIZE}/{media_item['poster_path']}"

            info_dict.append(item_data_to_add)

        return info_dict

    def discover_by_genre(self, media_type, genre):
        """ Returns the info from TMDB's discover section. """

        return self.get_info_for_grid(
            f"https://api.themoviedb.org/3/discover/{media_type}",
            additional_args=f"&without_keywords=158436|6593|7344|18321|195997|445|11530|190115|206574|199723&with_genres={GENRES[genre]}&sort_by=popularity.desc&include_video=false",
            media_type=media_type,
        )

    def info_by_category(self, category_after, media_type, category_before=None):
        """ Returns the information on media of a particular category like 'trending' or 'popular'. """

        return self.get_general_info(
            f"https://api.themoviedb.org/3{ ('/' + category_before) if category_before else ''}/{media_type}/{category_after}",
            media_type=media_type,
        )


def simplify_response(response_dict: dict, media_type):
    """ Returns a simplified version of the response with only the basic info of the movies and shows. Used mainly for the large and small carousels. """

    simplified_response = []
    media_title = ""
    media_date_name = ""

    for media_item in response_dict:

        item_data_to_add = {}

        # Set the dictionary's key names depending on the type of media
        if media_type == None or media_type == "all":
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
        item_data_to_add["id"] = media_item["id"]

        # If the media is not in English, show the media's title in its original language first, followed by its English name in parantheses.
        if media_item["original_language"] != "en" and (
            media_item["original_" + media_title] != media_item[media_title]
        ):
            item_data_to_add[
                "full_title"
            ] = f"{media_item['original_' + media_title]} ({media_item[media_title]})"

        # else, just show the normal title.
        else:
            item_data_to_add["full_title"] = media_item[media_title]

        # Add the desctiption and trim it to 250 characters (if larger).
        description = media_item["overview"]
        item_data_to_add["description"] = (
            (description[:OVERVIEW_MAX_CHARS] + "...")
            if len(description) > (OVERVIEW_MAX_CHARS + 3)
            else description
        )

        # Add the release/air date
        try:
            date_list = media_item[media_date_name].split("-")
        except KeyError:
            item_data_to_add["date"] = "Unavailable"
        else:
            item_data_to_add[
                "date"
            ] = f"{MONTHS[int(date_list[1]) - 1]} {date_list[2]}, {date_list[0]}"

        # Add the rating
        item_data_to_add["rating"] = (
            "N/A" if media_item["vote_average"] == 0 else media_item["vote_average"]
        )

        # If there is no backdrop image, add the default one.
        if media_item["backdrop_path"] == None:
            item_data_to_add["backdrop"] = url_for(
                "static", filename="img/no_backdrop.png"
            )
        else:
            item_data_to_add[
                "backdrop"
            ] = f"https://image.tmdb.org/t/p/w{BACKDROP_SIZE}/{media_item['backdrop_path']}"

        # If there is no poster image, add the default one.
        if media_item["poster_path"] == None:
            item_data_to_add["poster"] = url_for("static", filename="img/no_poster.png")
        else:
            item_data_to_add[
                "poster"
            ] = f"https://image.tmdb.org/t/p/w{POSTER_SIZE}/{media_item['poster_path']}"

        simplified_response.append(item_data_to_add)

    return simplified_response
