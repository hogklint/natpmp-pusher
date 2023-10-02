import logging
from argparse import ArgumentParser

from pusher import conf
from pusher.event_loop import run
from pusher.git import GitPush
from pusher.natpmp import NatPmp
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
    parser.add_argument("--repo-password", nargs="?")
    parser.add_argument("--repo-branch", nargs="?", default="master")
    parser.add_argument("--clone-dir", nargs="?")
    parser.add_argument("--port-file-path", nargs="?")
    parser.add_argument("--port-yaml-path", nargs="?")
    parser.add_argument(
        "--nat-gateway", nargs="?", help="gateway IP (default to looking it up)"
    )
    parser.add_argument(
        "--nat-udp", action="store_true", help="use UDP (TCP by default)"
    )
    parser.add_argument(
        "--nat-private-port",
        nargs="?",
        type=int,
        help="private port",
    )
    parser.add_argument(
        "--nat-public-request-port",
        nargs="?",
        type=int,
        help="public request port",
    )
    parser.add_argument(
        "--nat-lifetime", nargs="?", default=3600, type=int, help="desired lifetime"
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    conf.init_args(args)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    log.info("am main")
    port_cache = PortCache(GitPush())
    natpmp = NatPmp()
    run(port_cache, natpmp)
