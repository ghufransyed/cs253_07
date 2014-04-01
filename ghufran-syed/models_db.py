from google.appengine.ext import db


class BlogData(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now=True, auto_now_add=True)


class User(db.Model):
    user_id = db.StringProperty()
    password = db.StringProperty()
    email = db.EmailProperty()
