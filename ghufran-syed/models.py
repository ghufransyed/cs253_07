from google.appengine.ext import ndb


class WikiData(ndb.Model):
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now=True, auto_now_add=True)
    author = ndb.StringProperty(required=True)  # new property


class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
