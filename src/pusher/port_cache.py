from pusher.git import GitPush


class PortCache:
    def __init__(self, git_push: GitPush) -> None:
        self.git_push = git_push
        self.file_data = None

    @property
    def port(self) -> int:
        return self._values()["rtorrent"]["listenService"]["port"]

    @port.setter
    def port(self, port: int) -> None:
        new_values = self._values()
        new_values["rtorrent"]["listenService"]["port"] = port
        self.git_push.write_yaml_file(new_values)
        self.git_push.commit_file(f"Updating to port {port}")
        self.git_push.push()

    def _values(self) -> dict:
        if self.file_data is None:
            self.file_data = self.git_push.read_yaml_file()
        return self.file_data
