from pusher.git import GitPush


class PortCache:
    def __init__(self, git_push: GitPush, port_path: str) -> None:
        self.git_push = git_push
        self.port_path = port_path
        self.file_data = None

    @property
    def port(self) -> int:
        return self._get_port()

    @port.setter
    def port(self, port: int) -> None:
        self._set_port(port)
        self.git_push.write_yaml_file(self._values())
        self.git_push.commit_file(f"Updating to port {port}")
        self.git_push.push()

    def _values(self, refresh: bool = False) -> dict:
        if self.file_data is None or refresh:
            self.file_data = self.git_push.read_yaml_file()
        return self.file_data

    def _set_port(self, port: int) -> None:
        d = self._values()
        parts = self.port_path.split(".")
        for key in parts[:-1]:
            d = d[key]
        d[parts[-1]] = port

    def _get_port(self) -> int:
        d = self._values()
        for key in self.port_path.split("."):
            d = d[key]
        if not isinstance(d, int):
            raise TypeError("Port path does not point to an int")
        return d
