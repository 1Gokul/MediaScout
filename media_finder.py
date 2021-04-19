import os
import requests
from flask import json, jsonify, url_for
from operator import itemgetter


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

# Genders in the TMDB API
TMDB_LISTED_GENDERS = ["N/A", "Female", "Male", "Non-Binary"]

BACKDROP_SIZE = 1280
POSTER_SIZE = 300
ACTOR_POSTER_SIZE = 185
OVERVIEW_MAX_CHARS = 250


class MediaFinder:
    def __init__(self):
        self.api_key = os.environ.get("MOVIEDB_API_KEY")

    def get_general_info(self, url: str, additional_args: str = "", media_type=None):
        """ Gets info from the api and returns a simplified dict of the data. """

        response = requests.get(f"{url}?api_key={self.api_key}{additional_args}")

        return simplify_response(response.json()["results"], media_type)

    def get_info_for_grid(
        self, url: str, additional_args: str = "", media_type="movie"
    ):
        """ Gets the info required for showing in the poster grids (i.e. only the poster, media ID and link)."""

        response = requests.get(
            f"{url}?api_key={self.api_key}{additional_args}"
        ).json()["results"]

        info_list = []

        for media_item in response:

            item_data_to_add = {
                "id": media_item["id"],
                "detail_link": url_for(f"get_{media_type}_detail", id=media_item["id"]),
            }

            # If there is no poster image, add the default one.
            if media_item["poster_path"] == None:
                item_data_to_add["poster"] = url_for(
                    "static", filename="img/no_poster.png"
                )
            else:
                item_data_to_add[
                    "poster"
                ] = f"https://image.tmdb.org/t/p/w{POSTER_SIZE}/{media_item['poster_path']}"

            info_list.append(item_data_to_add)

        return info_list

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

    def get_media_detailed_info(self, media_type, id):
        """ Get detailed information about a movie or show. """
        response = requests.get(
            f"https://api.themoviedb.org/3/{media_type}/{id}?api_key={self.api_key}&language=en-US&append_to_response=credits,similar,keywords,videos{',seasons' if media_type == 'tv' else ''}"
        ).json()

        # The simplify_response() function will help format and add the basic information of the media.
        simplified_response = simplify_response([response], media_type=media_type)[0]

        # Adding additional info
        simplified_response["tagline"] = response["tagline"]

        simplified_response["description"] = response["overview"]

        # Show a trailer
        for video in response["videos"]["results"]:
            if video["type"] == "Trailer":
                video_id = video["key"]
                break

        simplified_response["trailer"] = (
            f"https://www.youtube.com/watch?v={video_id}" if video_id else None
        )

        simplified_response["genres"] = ""

        # Add no more than 2 genres
        index = 0
        for genre in response["genres"]:

            simplified_response["genres"] += genre["name"]
            index += 1

            if genre == response["genres"][-1] or index >= 2:
                break
            else:
                simplified_response["genres"] += ", "

        # If a movie, show the duration
        if media_type == "movie":
            keyword_key = "keywords"
            simplified_response["runtime"] = f"{response['runtime'] or 0} minutes"

        # else if a series, show the number of seasons.
        else:
            keyword_key = "results"
            simplified_response[
                "n_seasons"
            ] = f"{response['number_of_seasons']} season{'s' if response['number_of_seasons'] > 1 else ''}"

            # Add the info of all the seasons

            seasons = []
            for season in response["seasons"]:
                season_info = {
                    "date": season["air_date"],
                    "name": season["name"],
                    "n_episodes": f"{season['episode_count']} episode{'s' if season['episode_count'] > 1 else ''}",
                    "description": season["overview"],
                    "link": url_for("get_tv_detail", id=season["id"]),
                }

                # If there is no poster image, add the default one.
                if season["poster_path"] == None:
                    season_info["poster"] = url_for("static", filename="img/no_poster.png")
                else:
                    season_info[
                        "poster"
                    ] = f"https://image.tmdb.org/t/p/w{POSTER_SIZE}/{season['poster_path']}"

                seasons.append(season_info)

            simplified_response["seasons"] = seasons

        # Spoken languages in the media
        simplified_response["media_status"] = response["status"]
        simplified_response["language"] = ", ".join(
            [language["english_name"] for language in response["spoken_languages"]]
        )

        # Companies involved
        simplified_response["production_companies"] = ", ".join(
            [company["name"] for company in response["production_companies"]]
        )

        # Credits

        # Crew
        directors = []

        for member in response["credits"]["crew"]:
            if member["job"] == "Director":
                directors.append(member["name"])

        simplified_response["directors"] = ", ".join(directors) or "N/A"

        cast = format_cast_dict(response["credits"]["cast"])

        simplified_response["cast"] = cast

        # Similar movies/series

        similar = []

        for item in response["similar"]["results"]:
            similar_item = {"id": item["id"]}

            if item["poster_path"] == None:
                similar_item["poster"] = url_for("static", filename="img/no_poster.png")
            else:
                similar_item[
                    "poster"
                ] = f"https://image.tmdb.org/t/p/w{POSTER_SIZE}/{item['poster_path']}"

            similar_item["detail_link"] = url_for(
                f"get_{media_type}_detail", id=item["id"]
            )

            similar.append(similar_item)

        simplified_response["similar"] = similar

        # Keywords
        simplified_response["keywords"] = response["keywords"][keyword_key]

        return simplified_response

    def get_person_detailed_info(self, id):
        """ Gets detailed information of a person. """

        response = requests.get(
            f"https://api.themoviedb.org/3/person/{id}?api_key={self.api_key}&language=en-US&append_to_response=movie_credits,tv_credits,images"
        ).json()

        actor_info = {
            "id": response["id"],
            "full_name": response["name"],
            "department": response["known_for_department"],
            "gender": TMDB_LISTED_GENDERS[response["gender"]],
            "place_of_birth": response["place_of_birth"] or "N/A",
            "biography": response["biography"],
        }

        # If there is no poster image, add the default one.
        if response["profile_path"] == None:
            actor_info["poster"] = url_for("static", filename="img/no_poster.png")
        else:
            actor_info[
                "poster"
            ] = f"https://image.tmdb.org/t/p/w{POSTER_SIZE}/{response['images']['profiles'][-1]['file_path']}"

        # Date of birth
        actor_info["date_of_birth"] = prettify_date(response["birthday"])

        # Date of death
        actor_info["date_of_death"] = prettify_date(response["deathday"])

        # Movie Credits
        movie_credits = []

        for credit in response["movie_credits"]["cast"]:
            movie_credit = {
                "link": url_for("get_movie_detail", id=credit["id"]),
                "title": credit["title"],
                "role": credit["character"],
            }

            try:
                movie_credit["year"] = credit["release_date"].split("-")[0]
            except (KeyError, AttributeError):
                movie_credit["year"] = "N/A"

            movie_credits.append(movie_credit)

        movie_credits = sorted(movie_credits, key=itemgetter("year"))
        actor_info["movie_credits"] = movie_credits

        # TV Credits
        tv_credits = []

        for credit in response["tv_credits"]["cast"]:
            tv_credit = {
                "link": url_for("get_tv_detail", id=credit["id"]),
                "title": credit["name"],
                "role": credit["character"],
            }

            try:
                tv_credit["year"] = credit["first_air_date"].split("-")[0]
            except (KeyError, AttributeError):
                tv_credit["year"] = "N/A"

            tv_credits.append(tv_credit)

        tv_credits = sorted(tv_credits, key=itemgetter("year"))
        actor_info["tv_credits"] = tv_credits

        # IMDB link
        actor_info["imdb_link"] = f"https://www.imdb.com/name/{response['imdb_id']}"

        return actor_info

    def get_search_query_results(self, query):
        response = requests.get(
            f"https://api.themoviedb.org/3/search/multi?api_key={self.api_key}&language=en-US&query={query}&page=1&include_adult=false"
        ).json()
        return simplify_response(response["results"])

    def search_by_keyword(self, keyword, media_type):
        response = requests.get(
            f"https://api.themoviedb.org/3/discover/{media_type}?api_key={self.api_key}&with_keywords={keyword}"
        ).json()

        # Get the name of the keyword
        keyword_name = requests.get(
            f"https://api.themoviedb.org/3/keyword/{keyword}?api_key={self.api_key}"
        ).json()["name"]

        return keyword_name, simplify_response(response["results"], media_type)


def simplify_response(response_list, media_type="all"):
    """ Returns a simplified version of the response with only the basic info of the movies, shows or people. """

    simplified_response = []
    media_title = ""
    media_date_name = ""

    for media_item in response_list:

        item_data_to_add = {}

        # Set the dictionary's key names depending on the type of media
        if media_type == "all":
            m_type = media_item["media_type"]
        else:
            m_type = media_type

        if m_type == "movie":
            media_title = "title"
            media_date_name = "release_date"
            poster_title = "poster_path"
        elif m_type == "tv":
            media_title = "name"
            media_date_name = "first_air_date"
            poster_title = "poster_path"
        else:  # if the media_item is the info of a person
            media_title = "name"
            poster_title = "profile_path"

        # Add the media's ID
        item_data_to_add["id"] = media_item["id"]

        # The link to the media's detail page
        item_data_to_add["detail_link"] = url_for(
            f"get_{m_type}_detail", id=media_item["id"]
        )

        # If the media_item is a person, the description will be a short list of the movies/tv shows the person has been in.
        # The title will be the person's name.
        if m_type == "person":
            seen_in_media = []
            for item in media_item["known_for"]:
                if media_item["known_for"].index(item) > 2:
                    break
                else:
                    seen_in_media.append(
                        item["title"] if item["media_type"] == "movie" else item["name"]
                    )

            description = f"Seen in {', '.join(seen_in_media)}"

            item_data_to_add["full_title"] = media_item[media_title]

        # else, the description will be the overview of the media.
        else:
            description = media_item["overview"]

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

            # Add the release/air date
            item_data_to_add["date"] = prettify_date(media_item[media_date_name])

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

        # Add the desctiption and trim it to 250 characters (if larger).
        item_data_to_add["description"] = (
            (description[:OVERVIEW_MAX_CHARS] + "...")
            if len(description) > (OVERVIEW_MAX_CHARS + 3)
            else description
        )

        # If there is no poster image, add the default one.
        if media_item[poster_title] == None:
            item_data_to_add["poster"] = url_for("static", filename="img/no_poster.png")
        else:
            item_data_to_add[
                "poster"
            ] = f"https://image.tmdb.org/t/p/w{POSTER_SIZE}/{media_item[poster_title]}"

        simplified_response.append(item_data_to_add)

    return simplified_response


def prettify_date(date):
    try:
        if date != "":
            date_list = date.split("-")
    except (KeyError, AttributeError):
        new_date = "Unavailable"
    else:
        new_date = f"{MONTHS[int(date_list[1]) - 1]} {date_list[2]}, {date_list[0]}"

    return new_date

def format_cast_dict(cast_dict):
    # Cast
    cast = []
    for actor in cast_dict:
        actor_info = {}
        actor_info["id"] = actor["id"]
        actor_info["name"] = actor["name"]
        actor_info["character"] = actor["character"]
        actor_info["link"] = url_for("get_person_detail", id=actor["id"])

        # If there is no poster image, add the default one.
        if actor["profile_path"] == None:
            actor_info["image"] = url_for("static", filename="img/no_poster.png")
        else:
            actor_info[
                "image"
            ] = f"https://image.tmdb.org/t/p/w{ACTOR_POSTER_SIZE}/{actor['profile_path']}"

        cast.append(actor_info)

    return cast