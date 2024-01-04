"""
Given a Spotify playlist URL, like or dislike all the tracks of it. For this we will need to get all of our tracks, then like or dislike them all individually.

in text: Spotify Playlist URL
in list: Action - Like | Dislike
out: Message - Success | Error
"""

from os import path
from rich.console import Console
from rich.traceback import install
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler

from utils import (
    check_and_prompt_data,
    get_action,
    get_url,
    load_json,
    perfrom_action_on_tracks,
    save_json,
)

install()
console = Console()
current_dir = path.dirname(path.abspath(__file__))
auth_file = path.join(current_dir, "..", "data", "auth.json")
cache_file = path.join(current_dir, "..", "data", "cache.json")
scope = "user-library-modify"


# TODO: Add options for Albums and Artists
def main() -> None:
    # Get the URL and action from the user
    url = get_url()
    action = get_action()

    # Load the authentication data from a JSON file
    auth_data = load_json(path=auth_file)

    # Extract the client ID, client secret, and redirect URL from the authentication data
    client_id, client_secret, redirect_url = (
        check_and_prompt_data(auth_data=auth_data, variable="client_id"),
        check_and_prompt_data(auth_data=auth_data, variable="client_secret"),
        check_and_prompt_data(auth_data=auth_data, variable="redirect_url"),
    )

    # Save the extracted authentication data back to the JSON file
    save_json(
        path=auth_file,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_url": redirect_url,
        },
    )

    # Create a Spotify object with the extracted authentication details
    spotify = Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_url,
            cache_handler=CacheFileHandler(cache_path=cache_file),
        )
    )

    # Get the playlist using the Spotify object and the provided URL
    playlist = spotify.playlist(url)

    # Perform the specified action on the tracks in the playlist
    perfrom_action_on_tracks(
        playlist=playlist, spotify=spotify, console=console, action=action
    )


if __name__ == "__main__":
    main()
