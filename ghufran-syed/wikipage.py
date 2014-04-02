from mainhandler import Handler, params
from models import WikiData
from google.appengine.api import memcache
import logging
import re


class WikiPage(Handler):
    def get(self, wikipage_address):
        self.write((repr(wikipage_address)))
        self.write("\n")

        test = re.search("(\w+)", wikipage_address)
        if test:
            logging.error("test positive")
            wikipage_address = test.group(0)
            self.write(wikipage_address)
        else:
            logging.error("test negative")
            wikipage_address = "/"
            print "wikipage_address is '{0}'".format(wikipage_address)
            self.write(wikipage_address)

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
                logging.error("wikipage_query empty, need redirect to edit page")
                pass  # TODO  redirect edit page
