__all__ = ["Config"]

import re
from argparse import Namespace
from datetime import timedelta
from os import environ


class Config:
    repo_url: str
    repo_username: str
    repo_password: str
    repo_branch: str
    clone_dir: str
    port_file_path: str
    port_yaml_path: str
    min_update_freq: timedelta

    def __init__(self) -> None:
        self.min_update_freq = timedelta(hours=12)

    def init_args(self, args: Namespace) -> None:
        for config in [
            "repo_url",
            "repo_username",
            "repo_password",
            "repo_branch",
            "clone_dir",
            "port_yaml_path",
            "port_file_path",
        ]:
            env_name = f"PUSHER_{config.upper()}"
            if value := getattr(args, config, None) or environ.get(env_name):
                setattr(self, config, value)
            else:
                raise ValueError(
                    f"Must set --{config.replace('_', '-')} or env {env_name}"
                )
        if self.repo_password is None:
            raise ValueError("Must set env PUSHER_REPO_PASSWORD")

    @property
    def repo_clone_url(self):
        if match := re.match(r"^(?P<proto>https?:\/\/)(?P<url>.*)", self.repo_url):
            return f"{match.group('proto')}{self.repo_username}:{self.repo_password}@{match.group('url')}"
        raise ValueError("Could not match repo URL")
