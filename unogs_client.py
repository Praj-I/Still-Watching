"""UNoGS API file."""

import os
from typing import Any
from tenacity import retry, wait_exponential, stop_after_attempt
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("UNOGS_API_KEY")
API_HOST = "unogs-unogs-v1.p.rapidapi.com"

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

SEARCH_URL = "https://unogs-unogs-v1.p.rapidapi.com/search/titles"
EPISODES_URL = "https://unogs-unogs-v1.p.rapidapi.com/title/episodes"

def search_show (query: str) -> Any:
    """Search for a show by title. Returns a list of matches
    (title, netflix_id, title_type, year, etc.)
    Used when the user adds a new show to track."""

    querystring = { "title": query,
                    "type": "series",
                    "order_by": "date"}
    response = requests.get(SEARCH_URL, headers=headers, params=querystring, timeout=10)
    response.raise_for_status()
    show = response.json()

    return show["results"]

@retry(wait=wait_exponential(), stop=stop_after_attempt(4))
def get_episodes(netflix_id: int) -> Any:
    """Get the full episode list for a show.
    Returns a list of episodes with episode_id, season_number,
    episode_number, and title. Used to check for updates."""

    querystring = {"netflix_id": netflix_id}
    response = requests.get(EPISODES_URL, headers=headers, params=querystring, timeout=10)
    response.raise_for_status()
    episodes = response.json()

    return episodes["results"]
