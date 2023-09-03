import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] %(message)s  [%(name)s:%(lineno)s]",
)
log = logging.getLogger(__name__)


def main():
    log.info("am main")
