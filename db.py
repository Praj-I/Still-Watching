"""SQLite file."""

import sqlite3
from typing import Any

def init_db() -> None:
    """Constructor to create 3 tables: one for shows added,
    one for the episodes of those shows, and one for emails.
    Used to check for updates via episode count."""

    # Open a connection to database
    conn = sqlite3.connect("still_watching.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            netflix_id INTEGER UNIQUE,
            title TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodes (
            episode_id INTEGER PRIMARY KEY,
            show_netflix_id INTEGER,
            season INTEGER,
            episode INTEGER,
            title TEXT
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS email_configurations (
        id INTEGER PRIMARY KEY,
        notify_email TEXT
    )
""")

    # Save changes
    conn.commit()
    conn.close()

def add_show(netflix_id: int, title: str) -> None:
    """Adds a new row to the show table."""
    conn = sqlite3.connect("still_watching.db")
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO shows (netflix_id, title) VALUES (?, ?)",
                    (netflix_id, title)
    )

    conn.commit()
    conn.close()

def list_shows() -> list[Any]:
    """Returns a list of all shows the user wants to be updated on."""

    conn = sqlite3.connect("still_watching.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM shows")

    all_shows = cursor.fetchall()

    conn.close()

    return all_shows

def current_episodes(netflix_id: int) -> set[Any]:
    """Returns all current episode ids for a given show."""

    conn = sqlite3.connect("still_watching.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM episodes WHERE show_netflix_id = ?",
                    (netflix_id,) # Pass as tuple
                    )

    all_episode_ids = {row[0] for row in cursor.fetchall()}

    conn.close()

    return all_episode_ids

def add_episode(episode_id: int, show_netflix_id: int, season_number: int,
                episode_number: int, title: str) -> None:
    """If a show is updated, insert the new episode into the database."""

    conn = sqlite3.connect("still_watching.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO episodes (episode_id, show_netflix_id, season, episode, title) VALUES (?, ?, ?, ?, ?)",
                        (episode_id, show_netflix_id, season_number, episode_number, title)
                    )

    conn.commit()
    conn.close()

def remove_show(netflix_id: int) -> None:
    """Removes a show and all its stored episodes from both databases."""
    conn = sqlite3.connect("still_watching.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM episodes WHERE show_netflix_id = ?",
                    (netflix_id,))
    cursor.execute("DELETE FROM shows WHERE netflix_id = ?",
                    (netflix_id,))

    conn.commit()
    conn.close()

def set_email(email: str) -> None:
    """Saves the user's email for notifications."""
    conn = sqlite3.connect("still_watching.db")
    cursor = conn.cursor()

    cursor.execute("INSERT OR REPLACE INTO email_configurations (id, notify_email) VALUES (1, ?)",
                    (email,)
                    )

    conn.commit()
    conn.close()

def get_email() -> str | None:
    """Returns the user's email."""
    conn = sqlite3.connect("still_watching.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT notify_email FROM email_configurations WHERE id = 1")

    email = cursor.fetchone()

    conn.close()

    if not email:
        return None
    else:
        return str(email["notify_email"])
