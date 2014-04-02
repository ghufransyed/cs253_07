from mainhandler import Handler, params
from models import BlogData
from google.appengine.api import memcache
import logging
import datetime


class WikiPage(Handler):
    def get(self, wikipage_address):
        blog_query = memcache.get(wikipage_address)
        if blog_query is not None:
            logging.error('cache-hit')
            self.time_elapsed_fn(blog_query)
        else:
            logging.error('cache-miss')
            timestamp = datetime.datetime.now()
            blog_query = (BlogData.get_by_id(int(wikipage_address)),
                          timestamp)
            memcache.set(wikipage_address, blog_query)
            self.time_elapsed_fn(blog_query)

# TODO may need to incorporate the caching code back into
# get function rather than in time_elapsed_fn

    def time_elapsed_fn(self, blog_query_p):
        last_updated = blog_query_p[1]
        blog_query = blog_query_p[0]
        now = datetime.datetime.now()
        time_elapsed = (now - last_updated).seconds
        params["blog_query"] = blog_query
        params["time_elapsed"] = time_elapsed
        self.render("permalink.html", **params)
