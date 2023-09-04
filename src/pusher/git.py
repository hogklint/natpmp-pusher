from typing import cast

from git import Actor, Blob, Repo
from pusher import conf
from yaml import safe_dump, safe_load


class GitPush:
    def __init__(self, file_path: str):
        self.repo = Repo.clone_from(
            conf.repo_clone_url, conf.clone_dir, branch=conf.repo_branch
        )
        self.file_path = file_path
        self.author = Actor("PmpNatBot", "-")

    @property
    def file(self) -> Blob:
        return cast(Blob, self.repo.tree() / self.file_path)

    def read_yaml_file(self) -> dict:
        y = safe_load(self.file.data_stream.read())
        return y

    def write_yaml_file(self, data: dict) -> None:
        with open(self.file.abspath, "w") as f:
            f.write(safe_dump(data))

    def commit_file(self, commit_message) -> None:
        self.repo.index.add([self.file.abspath])
        self.repo.index.commit(commit_message, author=self.author)
