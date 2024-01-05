def getId(url: str) -> str:
    res = url.split("/")[-1]
    return res.split("?")[0]


def performActionOnTracks(
    tracks: list,
    collectionType: str,
    spotify: object,
    console: object,
    action: str,
):
    try:
        with console.status("Processing all the tracks..."):
            for track in tracks:
                trackId = track["id"]
                spotify.current_user_saved_tracks_add(
                    [trackId]
                ) if action == "Like" else spotify.current_user_saved_tracks_delete(
                    [trackId]
                )
        console.print(
            f"[green]Successfully {action.lower()}d all tracks in a given {collectionType.lower()}[/green]"
        )
    except Exception as e:
        console.print(f"[red]Failed to {action.lower()} all tracks: {e}[/red]")
