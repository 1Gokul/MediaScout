import os
import requests
from flask import json, jsonify

class MovieFinder:
    def __init__(self):
        self.api_key = os.environ.get("API_KEY")

    def get_trending(self):
        response = requests.get(f"https://api.themoviedb.org/3/trending/all/week?api_key={self.api_key}")
        return response.json()["results"]



