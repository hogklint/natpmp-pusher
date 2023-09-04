__all__ = ["Config"]

import re
from os import environ


class Config:
    def __init__(self) -> None:
        self.repo_url = environ["PUSHER_REPO_URL"]
        self.repo_username = environ["PUSHER_REPO_USERNAME"]
        self.repo_password = environ["PUSHER_REPO_PASSWORD"]
        self.clone_dir = environ["PUSHER_CLONE_DIR"]

    @property
    def repo_clone_url(self):
        if match := re.match(r"^(?P<proto>https?:\/\/)(?P<url>.*)", self.repo_url):
            return f"{match.group('proto')}{self.repo_username}:{self.repo_password}@{match.group('url')}"
        raise ValueError("Could not match repo URL")
