import os
import requests
from flask import json, jsonify


class MediaFinder:
    def __init__(self):
        self.api_key = os.environ.get("MOVIEDB_API_KEY")

    def get_info(self, url):
        response = requests.get(f"{url}?api_key={self.api_key}")
        return response.json()["results"]

    # For the homepage
    def get_trending_movies(self):
        return self.get_info(
            "https://api.themoviedb.org/3/trending/movie/week")

    def get_trending_shows(self):
        return self.get_info("https://api.themoviedb.org/3/trending/tv/week")

    def get_spotlight(self):
        return self.get_info("https://api.themoviedb.org/3/trending/all/day")

    # For movies

    def get_now_playing_movies(self):
        return self.get_info("https://api.themoviedb.org/3/movie/now_playing")

    def get_upcoming_movies(self):
        return self.get_info("https://api.themoviedb.org/3/movie/upcoming")

    def get_popular_movies(self):
        return self.get_info("https://api.themoviedb.org/3/movie/popular")

    def get_top_rated_movies(self):
        return self.get_info("https://api.themoviedb.org/3/movie/top_rated")

    # For TV

    def get_shows_airing_today(self):
        return self.get_info("https://api.themoviedb.org/3/tv/airing_today")

    def get_shows_on_the_air(self):
        return self.get_info("https://api.themoviedb.org/3/tv/on_the_air")

    def get_popular_shows(self):
        return self.get_info("https://api.themoviedb.org/3/tv/popular")

    def get_top_rated_shows(self):
        return self.get_info("https://api.themoviedb.org/3/tv/top_rated")