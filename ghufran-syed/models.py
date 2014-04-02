from google.appengine.ext import ndb


class WikiData(ndb.Model):
    address = ndb.StringProperty(required=True)
    # cannot use the address as the key in instantiation
    # as key cannot be empty string, but address can be (root page)
    title = ndb.StringProperty(required=True)  # was subject
    #  TODO change references to subject
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now=True, auto_now_add=True)
    author = ndb.StringProperty(required=True)  # new property


class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
