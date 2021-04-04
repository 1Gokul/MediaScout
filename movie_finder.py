import os
import requests
from flask import json, jsonify


class MovieFinder:
    def __init__(self):
        self.api_key = os.environ.get("MOVIEDB_API_KEY")

    def get_info(self, url):
        response = requests.get(f"{url}?api_key={self.api_key}")
        return response.json()["results"]

    def get_trending_movies(self):
        return self.get_info(
            "https://api.themoviedb.org/3/trending/movie/week")

    def get_trending_shows(self):
        return self.get_info("https://api.themoviedb.org/3/trending/tv/week")

    def get_spotlight(self):
        return self.get_info("https://api.themoviedb.org/3/trending/all/day")
