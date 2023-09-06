import logging
from time import sleep

from pusher.port_cache import PortCache

log = logging.getLogger(__name__)


def run(port_cache: PortCache) -> None:
    nat_port = 50011
    while True:
        if nat_port != port_cache.port:
            log.info("New NAT port: %s", nat_port)
            port_cache.port = nat_port
        log.info("Sleeping...")
        sleep(10)
