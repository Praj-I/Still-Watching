"""FastAPI backend file."""

import threading
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from unogs_client import search_show, get_episodes
from db import (
    init_db,
    add_show,
    remove_show,
    list_shows,
    add_episode,
    set_email,
    get_email,
    get_show_title,
)
from watcher import run_watcher

init_db()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ShowInput(BaseModel):
    """Represents a single show."""

    netflix_id: int
    title: str

class ShowList(BaseModel):
    """Represents a batch of shows, used for returning users."""

    show_list: list[ShowInput]

class SetupInput(BaseModel):
    """Represents first-time setup: a batch of shows plus an email."""

    show_list: list[ShowInput]
    email: str



def chosen_shows(netflix_id: int, title: str) -> None:
    """Adds a show and silently saves its current episodes with no notifications."""

    add_show(netflix_id, title)

    current_episodes = get_episodes(netflix_id)

    for episode in current_episodes:
        add_episode(
            episode["episode_id"],
            netflix_id,
            episode["season_number"],
            episode["episode_number"],
            episode["title"],
        )

@app.get("/search")
def search(title: str) -> Any:
    """Search uNoGS for shows matching the given title."""

    return search_show(title)

@app.get("/shows")
def get_shows() -> list[Any]:
    """List all tracked shows."""

    return list_shows()

@app.post("/settings/setup")
def initial_setup(payload: SetupInput) -> dict[str, str]:
    """First-time setup: saves shows, sets email, and starts the poller."""

    for show in payload.show_list:
        chosen_shows(show.netflix_id, show.title)

    set_email(payload.email)

    poller_thread = threading.Thread(target=run_watcher, daemon=True)
    poller_thread.start()

    return {"message": "Setup complete. Notifications are now active."}

@app.post("/shows")
def create_show(payload: ShowList) -> dict[str, str]:
    """Batch-add shows for a returning user. Assumes the poller is already running."""

    for show in payload.show_list:
        chosen_shows(show.netflix_id, show.title)

    return {"message": f"{len(payload.show_list)} show(s) added."}

@app.delete("/shows/{netflix_id}")
def delete_show(netflix_id: int) -> dict[str, str]:
    """Remove a tracked show."""

    title = get_show_title(netflix_id)
    remove_show(netflix_id)

    return {"message": f"{title} removed from tracking."}

@app.get("/settings/email")
def get_notification_email() -> dict[str, str | None]:
    """Return the currently stored notification email, if any."""

    return {"email": get_email()}
