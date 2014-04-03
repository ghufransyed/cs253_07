from mainhandler import params
from models import WikiData
from google.appengine.api import memcache
import logging
# import re

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'


def get_data(wikipage_address):
    #edit_p = re.search('_edit' + PAGE_RE, wikipage_address)
    #if edit_p:
        #wikipage_address = edit_p.group(0)

    wikipage_query = memcache.get(wikipage_address)
    if wikipage_query:
        logging.error('cache-hit')
        params["wikipage_query"] = wikipage_query
        return True
    else:
        logging.error('cache-miss')
        wikipage_query = WikiData.get_by_id(wikipage_address)
        if wikipage_query:
            memcache.set(wikipage_address, wikipage_query)
            params["wikipage_query"] = wikipage_query
            return True
    params["wikipage_query"] = ''
    return False
