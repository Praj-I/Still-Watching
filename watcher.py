"""File to poll UNoGS."""

import time
from sqlite3 import Error
from requests import RequestException
from db import list_shows, current_episodes, add_episode
from unogs_client import get_episodes
from notifier import send_notification

POLL_INTERVAL_SECONDS = 4 * 60 * 60 # Every 4 hours

def check_for_new_episodes() -> None:
    """Goes through each tracked show, notes current episodes in db
    and current episodes from UNoGS API. If there's new episodes, adds to db
    and sends notification."""

    all_shows = list_shows()

    for show in all_shows:
        current_netflix_id = show["netflix_id"]
        current_title = show["title"]

        try:
            old_episodes = current_episodes(current_netflix_id)
            new_episodes = get_episodes(current_netflix_id)
        except RequestException as exception:
            print(f"Network/API error checking {current_title}: {exception}")
            continue
        except Error as exception:
            print(f"Database error checking {current_title}: {exception}")
            continue

        for episode in new_episodes:
            if episode["episode_id"] not in old_episodes:
                add_episode(
                    episode["episode_id"],
                    current_netflix_id,
                    episode["season_number"],
                    episode["episode_number"],
                    episode["title"])

                send_notification(current_title, episode["season_number"],
                                episode["episode_number"], episode["title"])

def run_watcher() -> None:
    """Runs episode checks on a loop every POLL_INTERVAL_SECONDS."""

    while True:
        check_for_new_episodes()
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_watcher()
