"""
Given a Spotify playlist URL, like or dislike all the tracks of it. For this we will need to get all of our tracks, then like or dislike them all individually.

in text: Spotify Playlist URL
in list: Action - Like | Dislike
out: Message - Success | Error
"""

from os import path, remove
from rich.console import Console
from rich.traceback import install
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth, CacheFileHandler

from utils import *

install()
console = Console()
currentDir = path.dirname(path.abspath(__file__))
authFile = path.join(currentDir, "..", "data", "auth.json")
cacheFile = path.join(currentDir, "..", "data", "cache.json")
scope = "user-library-modify"


def main() -> None:
    # Load the authentication data from a JSON file
    authData = loadJson(path=authFile)

    # Extract the client ID, client secret, and redirect URL from the authentication data
    clientId, clientSecret, redirectUrl = (
        checkAndPromptAuthData(authData=authData, variable="client_id"),
        checkAndPromptAuthData(authData=authData, variable="client_secret"),
        checkAndPromptAuthData(authData=authData, variable="redirect_url"),
    )

    # Save the extracted authentication data back to the JSON file
    saveJson(
        path=authFile,
        data={
            "client_id": clientId,
            "client_secret": clientSecret,
            "redirect_url": redirectUrl,
        },
    )

    # Get collection type from the user
    collectionType = getCollectionType()
    url = getUrl(collectionType)
    action = getAction()

    # Create a Spotify object with the extracted authentication details
    spotify = Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=clientId,
            client_secret=clientSecret,
            redirect_uri=redirectUrl,
            cache_handler=CacheFileHandler(cache_path=cacheFile),
        )
    )

    # Declare necessary variables like collection ID, tracks holder and error hint message
    collectionId = getId(url)
    tracks = []
    errorHintMessage = "\n[grey0]Spotify might be down at the moment, check out status - https://downdetector.com/status/spotify/[/grey0]"

    if collectionType == "Playlist":
        # Try creating a Spotify container
        try:
            container = spotify.playlist(playlist_id=collectionId)
        except Exception as e:
            console.print(f"[red]Failed to get playlist: '{e}'[/red]{errorHintMessage}")
            # Try removing cache file and see if it helps
            remove(cacheFile)
            return

        # Extract all the tracks from the playlist
        tracks = container["tracks"]["items"]
    elif collectionType == "Album":
        # Try creating a Spotify container
        try:
            container = spotify.album(album_id=collectionId)
        except Exception as e:
            console.print(f"[red]Failed to get album: '{e}'[/red]{errorHintMessage}")
            # Try removing cache file and see if it helps
            remove(cacheFile)
            return

        # Extract all the tracks from the album
        tracks = container["tracks"]["items"]
    elif collectionType == "Artist":
        # Try creating a Spotify container
        try:
            container = spotify.artist_albums(artist_id=collectionId)
        except Exception as e:
            console.print(f"[red]Failed to get artist: '{e}'[/red]{errorHintMessage}")
            # Try removing cache file and see if it helps
            remove(cacheFile)
            return

        # Loop over all albums in the given artist
        for album in container["items"]:
            # Create a Spotify container for the album
            albumObject = spotify.album(album_id=album["id"])
            # Extract all the tracks from the album
            currentTracks = albumObject["tracks"]["items"]
            # Append the tracks to the list
            tracks.extend(currentTracks)

    # Perform the specified action on the tracks in the playlist
    performActionOnTracks(
        tracks=tracks,
        collectionType=collectionType,
        spotify=spotify,
        console=console,
        action=action,
    )


if __name__ == "__main__":
    main()
