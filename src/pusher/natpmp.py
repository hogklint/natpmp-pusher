import logging
from datetime import datetime, timedelta

from natpmp import NATPMP_PROTOCOL_TCP, NATPMP_PROTOCOL_UDP, PortMapResponse, map_port
from pusher import conf

log = logging.getLogger(__name__)


class NatPmpError(Exception):
    ...


class NatPmp:
    def __init__(self) -> None:
        self.lifetime = 60
        self.public_port = 0
        self.map_time = datetime.min

    def get_port(self) -> tuple[int, int]:
        if (datetime.now() - self.map_time) > timedelta(seconds=self.lifetime - 30):
            self.map_port()
        return self.public_port, self.lifetime - 5

    def map_port(self) -> None:
        try:
            response = map_port(
                protocol=NATPMP_PROTOCOL_UDP if conf.nat_udp else NATPMP_PROTOCOL_TCP,
                public_port=conf.nat_public_request_port,
                private_port=conf.nat_private_port,
                lifetime=conf.nat_lifetime,
                gateway_ip=conf.nat_gateway,
            )
        except Exception as e:
            raise NatPmpError("Error mapping port") from e

        log.debug("%s", response)
        if not isinstance(response, PortMapResponse) or response.result != 0:
            raise NatPmpError(
                "Error mapping port, result: {response.result}, opcode: {response.opcode}"
            )

        self.map_time = datetime.now()
        self.lifetime = response.lifetime
        if self.public_port != (port := response.public_port):
            log.info("New NAT port: %s, lifetime: %s", port, self.lifetime)
            self.public_port = port
