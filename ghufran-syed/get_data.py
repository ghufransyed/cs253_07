from mainhandler import params
from models import WikiData
from google.appengine.api import memcache
import logging


def get_data(wikipage_address):
    wikipage_query = memcache.get(wikipage_address)
    if wikipage_query:
        logging.error('cache-hit')
        params["wikipage_query"] = wikipage_query
        return True
    else:
        logging.error('cache-miss')
        logging.error(wikipage_address)
        root_ancester = WikiData.get_by_id(wikipage_address)
        if root_ancester:
            logging.error("root_ancester True")
            root_ancester_key = root_ancester.key
            logging.error(root_ancester_key)
            wikipage_query = WikiData.query(ancestor=root_ancester_key)
            wikipage_query = wikipage_query.order(-WikiData.created)
            wikipage_result = wikipage_query.fetch(1)
            logging.error(wikipage_result)
            logging.error(wikipage_result[0].content)
            params["wikipage_query"] = wikipage_result[0]
            memcache.set(wikipage_address, wikipage_result[0])
            return True
    params["wikipage_query"] = ''
    logging.error("no previous data found for page")
    return False
