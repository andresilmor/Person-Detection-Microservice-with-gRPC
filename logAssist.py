import logging
from functools import lru_cache

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    format = '%(asctime)s | %(levelname)8s | %(message)s'

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

@lru_cache
def setupLogger(loggerName):
    logger = logging.getLogger(loggerName + "_logger")
    logger_file = logging.FileHandler("logs/" + loggerName + ".log", mode="a")
    logger_file.setFormatter(logging.Formatter(fmt='%(asctime)s | %(levelname)8s | %(message)s'))
    #logger_file.setFormatter(CustomFormatter())
    logger_stream = logging.StreamHandler()
    #logger_stream.setFormatter(logging.Formatter(fmt=fmt))
    logger_stream.setFormatter(CustomFormatter())
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logger_file)
    logger.addHandler(logger_stream)

setupLogger("connections")
setupLogger("requests")

def logWebSocketConnection(clientIP, route, clientUser = 'unknown'):
    logging.getLogger('connections_logger').info(clientIP + ' ' + clientUser + ' : START websocket connection (' + route + ')')


async def logRequest(clientIP, port, operation, type = "info"):
    if type == "info":
        logging.getLogger('requests_logger').info(str(clientIP) + ':' + str(port) + ' | ' + operation )
    else:
        logging.getLogger('requests_logger').critical(str(clientIP) + ':' + str(port) + ' | ' + operation )

