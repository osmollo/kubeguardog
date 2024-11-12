import os
import logging
import coloredlogs


logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', default='INFO'),
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%d-%m-%Y %H:%M",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(name=__name__)
logging.getLogger("urllib3").propagate = False
coloredlogs.install(logger=logger, isatty=True)
