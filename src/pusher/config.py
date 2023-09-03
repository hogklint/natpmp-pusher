__all__ = ["Config"]

from os import environ


class Config:
    def __init__(self) -> None:
        self.repo_url = environ["PUSHER_REPO_URL"]
