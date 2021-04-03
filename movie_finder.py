import os
import requests
from flask import json, jsonify


class MovieFinder:
    def __init__(self):
        self.api_key = os.environ.get("MOVIEDB_API_KEY")

    def get_trending_movies(self):
        response = requests.get(
            f"https://api.themoviedb.org/3/trending/movie/week?api_key={self.api_key}"
        )
        return response.json()["results"]

    def get_trending_shows(self):
        response = requests.get(
            f"https://api.themoviedb.org/3/trending/tv/week?api_key={self.api_key}"
        )
        return response.json()["results"]

    def get_spotlight(self):
        response = requests.get(
            f"https://api.themoviedb.org/3/trending/all/day?api_key={self.api_key}"
        )
        return response.json()["results"]
