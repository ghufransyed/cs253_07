from mainhandler import Handler, params
from models import WikiData
from google.appengine.api import memcache
import logging


class WikiPage(Handler):
    def get(self, wikipage_address):
        wikipage_query = memcache.get(wikipage_address)
        if wikipage_query is not None:
            logging.error('cache-hit')
            params["wikipage_query"] = wikipage_query
            self.render("wikipage.html", **params)
        else:
            logging.error('cache-miss')
            wikipage_query = WikiData.query(
                WikiData.address == wikipage_address).fetch(1)
            if wikipage_query:
                memcache.set(wikipage_address, wikipage_query)
                params["wikipage_query"] = wikipage_query
                self.render("wikipage.html", **params)
            else:
                self.redirect("_edit" + wikipage_address)
