import logging
from time import sleep

from pusher.natpmp import NatPmp
from pusher.port_cache import PortCache

log = logging.getLogger(__name__)


def run(port_cache: PortCache, natpmp: NatPmp) -> None:
    while True:
        nat_port, renew_time = natpmp.get_port()
        if nat_port != port_cache.port:
            port_cache.port = nat_port
        log.debug("Sleeping %s seconds...", renew_time)
        sleep(renew_time)
