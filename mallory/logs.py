import sys
import logging
import logging.handlers

def setup(debug=False):

    level = logging.DEBUG if debug else logging.INFO
    logger = logging.getLogger()
    logger.setLevel(level)
    formatter = logging.Formatter('mallory: %(levelname)s %(message)s')

    if sys.platform != "darwin":
        syslog = logging.handlers.SysLogHandler(address='/dev/log')
        syslog.setFormatter(formatter)
        logger.addHandler(syslog)
    else:
        stderr = logging.StreamHandler(stream=sys.stderr)
        stderr.setFormatter(formatter)
        logger.addHandler(stderr)

    if debug:
        logger.debug("Verbose logging enabled")
