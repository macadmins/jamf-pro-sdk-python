import logging
import sys


def logger_quick_setup(level=logging.INFO):
    """A helper function to quickly setup console logging for the SDK. Setting DEBUG
    logging will also apply these settings to ``urllib3``.

    :param level: Logging Level
    """
    logger = logging.getLogger("jamf_pro_sdk")
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(threadName)s %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    if level == logging.DEBUG:
        urllib3_logger = logging.getLogger("urllib3")
        urllib3_logger.setLevel(logging.DEBUG)
        urllib3_logger.addHandler(handler)
