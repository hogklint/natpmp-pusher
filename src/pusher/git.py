from git import Repo
from pusher import conf
from yaml import safe_load


class GitPush:
    def __init__(self, file_path: str):
        self.repo = Repo.clone_from(
            conf.repo_clone_url, conf.clone_dir, branch=conf.repo_branch
        )
        self.file_path = file_path

    @property
    def file(self):
        return self.repo.tree() / self.file_path

    def get_yaml_file(self) -> dict:
        y = safe_load(self.file.data_stream.read())
        return y
