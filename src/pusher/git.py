from git import Repo
from pusher import conf


class GitPush:
    def __init__(self):
        self.repo = Repo.clone_from(
            conf.repo_clone_url, conf.clone_dir, branch=conf.repo_branch
        )
