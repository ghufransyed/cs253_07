from google.appengine.ext import ndb
from google.appengine.api import memcache
from mainhandler import Handler, params
import logging
import datetime


class MainPage(Handler):
    def get(self):
        blog_query = memcache.get('blog_query')
        if blog_query is not None:
            logging.error('cache-hit')
            self.time_elapsed_fn(blog_query)
        else:
            logging.error('cache-miss')
            timestamp = datetime.datetime.now()
            blog_query = (list(ndb.gql("""SELECT * FROM BlogData
                                     ORDER BY created DESC
                                     LIMIT 0,10""")), timestamp)
            memcache.set('blog_query', blog_query)
            self.time_elapsed_fn(blog_query)

    def time_elapsed_fn(self, blog_query_p):
        last_updated = blog_query_p[1]
        blog_query = blog_query_p[0]
        now = datetime.datetime.now()
        time_elapsed = (now - last_updated).seconds
        params["blog_query"] = blog_query
        params["time_elapsed"] = time_elapsed
        self.render("frontpage.html", **params)
