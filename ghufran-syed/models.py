from google.appengine.ext import ndb


class BlogData(ndb.Model):
    subject = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now=True, auto_now_add=True)


class User(ndb.Model):
    user_id = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
