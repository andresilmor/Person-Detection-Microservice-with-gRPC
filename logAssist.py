import logging
from config import Settings
from functools import lru_cache

@lru_cache()
def logWebSocketConnection(clientIP, route, clientUser = 'unknown'):
    
    if (Settings().development):
        logging.basicConfig(filename="logs/connections.log", encoding="utf-8", level=logging.DEBUG, filemode="w", format='%(asctime)s.%(msecs)03d %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    else :
        logging.basicConfig(filename="logs/connections.log", encoding="utf-8", level=logging.INFO, filemode="a", format='%(asctime)s.%(msecs)03d %(message)s')

    logging.info(clientIP + ' ' + clientUser + ' : START websocket connection (' + route + ')')


   