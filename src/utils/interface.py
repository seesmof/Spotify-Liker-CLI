import inquirer


def getCollectionType() -> str:
    question = [
        inquirer.List(
            "collection_type",
            message="Choose a collection type",
            choices=["Playlist", "Album", "Artist"],
            default="Playlist",
        )
    ]
    answer = inquirer.prompt(question)
    return answer["collection_type"]


def getUrl(collectionType: str) -> str:
    question = [
        inquirer.Text(
            "url",
            message=f"Enter a Spotify {collectionType.title()} URL",
            validate=lambda _, x: x != ""
            and x.startswith(f"https://open.spotify.com/{collectionType.lower()}/"),
        )
    ]
    answer = inquirer.prompt(question)
    return answer["url"]


def getAction() -> str:
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


def checkAndPromptAuthData(authData: dict, variable: str) -> str:
    if authData[variable] != "":
        return authData[variable]
    else:
        name = (
            variable.replace("_", " ").title().replace("Url", "URL").replace("Id", "ID")
        )
        question = [
            inquirer.Text(
                variable,
                message=f"Enter your {name}",
            )
        ]
        answer = inquirer.prompt(question)
        return answer[variable]
