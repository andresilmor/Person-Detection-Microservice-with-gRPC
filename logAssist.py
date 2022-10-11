from distutils.core import setup
import logging
from config import Settings
from functools import lru_cache

'''
dbComms_logger = logging.getLogger("dbComms_logger")
dbComms_file = logging.FileHandler("logs/dbComms.log", mode="w")
dbComms_file.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(message)s'))
dbComms_stream = logging.StreamHandler()
dbComms_stream.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(message)s'))
dbComms_logger.setLevel(logging.INFO)
dbComms_logger.addHandler(dbComms_file)
dbComms_logger.addHandler(dbComms_stream)

connections_logger = logging.getLogger("connections_logger")
connections_file = logging.FileHandler("logs/connections.log", mode="w")
connections_file.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(message)s'))
connections_stream = logging.StreamHandler()
connections_stream.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(message)s'))
connections_logger.setLevel(logging.INFO)
connections_logger.addHandler(connections_file)
connections_logger.addHandler(connections_stream)
'''

def setupLogger(loggerName):
    logger = logging.getLogger(loggerName + "_logger")
    logger_file = logging.FileHandler("logs/" + loggerName + ".log", mode="w")
    logger_file.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(message)s'))
    logger_stream = logging.StreamHandler()
    logger_stream.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d %(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(logger_file)
    logger.addHandler(logger_stream)


setupLogger("connections")
setupLogger("dbComms")


@lru_cache()
def logWebSocketConnection(clientIP, route, clientUser = 'unknown'):
    logging.getLogger('connections_logger').info(clientIP + ' ' + clientUser + ' : START websocket connection (' + route + ')')

@lru_cache()
def logDatabaseComm(clientIP, route, operation, entity, clientUser = 'unknown'):
   logging.getLogger('dbComms_logger').info(clientIP + ' ' + clientUser + ' : ' + operation + ' ' + entity + ' (' + route + ')')

