from google.appengine.api import memcache
from mainhandler import Handler
import logging


class FlushHandler(Handler):
    def get(self):
        logging.error("cache-flush")
        memcache.flush_all()
        self.redirect('/')
