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
    nat_gateway: str
    nat_udp: bool
    nat_private_port: int
    nat_public_request_port: int
    nat_lifetime: int

    def __init__(self) -> None:
        self.min_update_freq = timedelta(hours=12)

    def init_args(self, args: Namespace) -> None:
        for config, required in [
            ("repo_url", True),
            ("repo_username", True),
            ("repo_password", True),
            ("repo_branch", True),
            ("clone_dir", True),
            ("port_yaml_path", True),
            ("port_file_path", True),
            ("nat_gateway", False),
            ("nat_udp", True),
            ("nat_private_port", True),
            ("nat_public_request_port", True),
            ("nat_lifetime", True),
        ]:
            env_name = f"PUSHER_{config.upper()}"
            if (value := getattr(args, config, None)) is not None or (
                value := environ.get(env_name)
            ):
                setattr(self, config, value)
            elif not required:
                setattr(self, config, None)
            else:
                raise ValueError(
                    f"Must set --{config.replace('_', '-')} or env {env_name}"
                )

    @property
    def repo_clone_url(self):
        if match := re.match(r"^(?P<proto>https?:\/\/)(?P<url>.*)", self.repo_url):
            return f"{match.group('proto')}{self.repo_username}:{self.repo_password}@{match.group('url')}"
        raise ValueError("Could not match repo URL")
