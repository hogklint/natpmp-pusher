import logging
from argparse import ArgumentParser

from pusher import conf
from pusher.event_loop import run
from pusher.git import GitPush
from pusher.port_cache import PortCache

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] %(message)s  [%(name)s:%(lineno)s]",
)
log = logging.getLogger(__name__)


def main():
    parser = ArgumentParser(prog="NAT PMP Pusher")
    parser.add_argument("--repo-url", nargs="?")
    parser.add_argument("--repo-username", nargs="?")
    parser.add_argument("--repo-branch", nargs="?", default="master")
    parser.add_argument("--port-file-path", nargs="?")
    parser.add_argument("--port-yaml-path", nargs="?")
    parser.add_argument("--clone-dir", nargs="?")
    conf.init_args(parser.parse_args())
    log.info("am main")
    port_cache = PortCache(GitPush())
    run(port_cache)
