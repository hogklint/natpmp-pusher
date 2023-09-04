__all__ = ["Config"]

import re
from argparse import Namespace
from os import environ


class Config:
    def __init__(self) -> None:
        self.repo_url = environ.get("PUSHER_REPO_URL")
        self.repo_username = environ.get("PUSHER_REPO_USERNAME")
        self.repo_password = environ.get("PUSHER_REPO_PASSWORD")
        self.clone_dir = environ.get("PUSHER_CLONE_DIR")

    def init_args(self, args: Namespace) -> None:
        for config in ["repo_url", "repo_username", "repo_branch", "clone_dir"]:
            if value := getattr(args, config, None):
                setattr(self, config, value)
            elif value := getattr(self, config) is None:
                raise ValueError(
                    f"Must set --{config.replace('_', '-')} or env PUSHER_{config.upper()}"
                )
        if self.repo_password is None:
            raise ValueError("Must set env PUSHER_REPO_PASSWORD")

    @property
    def repo_clone_url(self):
        if match := re.match(r"^(?P<proto>https?:\/\/)(?P<url>.*)", self.repo_url):
            return f"{match.group('proto')}{self.repo_username}:{self.repo_password}@{match.group('url')}"
        raise ValueError("Could not match repo URL")
