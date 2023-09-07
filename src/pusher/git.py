import logging
from datetime import datetime
from typing import cast

from git import Actor, Blob, Repo
from pusher import conf
from yaml import safe_dump, safe_load

log = logging.getLogger(__name__)


class PushError(Exception):
    pass


class PullError(Exception):
    pass


class GitPush:
    def __init__(self):
        self.repo = Repo.clone_from(
            conf.repo_clone_url, conf.clone_dir, branch=conf.repo_branch
        )
        self.actor = Actor("PmpNatBot", "-")

    @property
    def file(self) -> Blob:
        return cast(Blob, self.repo.tree() / conf.port_file_path)

    @property
    def file_date(self) -> datetime:
        commit = next(self.repo.iter_commits(paths=conf.port_file_path, max_count=1))
        return datetime.fromtimestamp(commit.committed_date)

    def read_yaml_file(self) -> dict:
        return safe_load(self.file.data_stream.read())

    def write_yaml_file(self, data: dict) -> None:
        log.debug("Writing file: %s", data)
        with open(self.file.abspath, "w") as f:
            f.write(safe_dump(data))

    def commit_file(self, commit_message) -> None:
        log.debug("Commiting file: %s", self.file.path)
        for pull_info in self.repo.remote().pull():
            if (pull_info.flags & pull_info.ERROR) > 0:
                raise PullError(f"Could not pull: {pull_info.note}")

        self.repo.index.add([self.file.abspath])
        self.repo.index.commit(commit_message, author=self.actor, committer=self.actor)

    def push(self) -> None:
        log.debug("Pushing commit")
        push_info = self.repo.remote().push()[0]
        if (push_info.flags & push_info.ERROR) > 0:
            if (push_info.flags & push_info.REJECTED) > 0:
                raise PushError(
                    "Remote rejected the commit: {push_info.summary.strip()}"
                )
            else:
                raise PushError("Error pushing the commit: {push_info.summary.strip()}")
