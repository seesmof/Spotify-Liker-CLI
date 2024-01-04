import json
import inquirer


def get_url() -> str:
    question = [
        inquirer.Text(
            "url",
            message="Enter a Spotify Playlist URL",
            validate=lambda _, x: x != ""
            and x.startswith("https://open.spotify.com/playlist/"),
        )
    ]
    answer = inquirer.prompt(question)
    return answer["url"]


def get_action() -> str:
    question = [
        inquirer.List(
            "action",
            message="Choose an action to take",
            choices=["Like", "Dislike"],
            default="Like",
        )
    ]
    answer = inquirer.prompt(question)
    return answer["action"]


def load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def check_and_prompt_data(auth_data: dict, variable: str) -> str:
    if auth_data[variable] != "":
        return auth_data[variable]
    else:
        name = variable.replace("_", " ").title().replace("Url", "URL")
        question = [
            inquirer.Text(
                variable,
                message=f"Enter your {name}",
            )
        ]
        answer = inquirer.prompt(question)
        return answer[variable]


def perfrom_action_on_tracks(
    playlist: dict, spotify: object, console: object, action: str
):
    tracks = playlist["tracks"]["items"]
    try:
        with console.status("Processing all the tracks..."):
            for track in tracks:
                track_id = track["track"]["id"]
                spotify.current_user_saved_tracks_add(
                    [track_id]
                ) if action == "Like" else spotify.current_user_saved_tracks_delete(
                    [track_id]
                )
        console.print(
            f"[green]Successfully {action.lower()}d all tracks in {playlist['name']}[/green]"
        )
    except Exception as e:
        console.print(f"[red]Failed to {action.lower()} all tracks: {e}[/red]")
