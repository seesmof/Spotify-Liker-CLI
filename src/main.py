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

    # Get the playlist using the Spotify object and the provided URL
    if collectionType == "Playlist":
        container = spotify.playlist(url)
        tracks = container["tracks"]["items"]
    elif collectionType == "Album":
        container = spotify.album(album_id=getId(url))
        tracks = container["tracks"]["items"]
    elif collectionType == "Artist":
        container = spotify.artist_albums(artist_id=getId(url))
        tracks = []
        for album in container["items"]:
            albumObject = spotify.album(album_id=album["id"])
            currentTracks = albumObject["tracks"]["items"]
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
