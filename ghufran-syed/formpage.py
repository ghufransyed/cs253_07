from mainpage import MainPage
from mainhandler import params
import re
from models import WikiData # TODO change refs below from BlogData
from google.appengine.api import memcache


SUBJECT_RE = re.compile(".{5,}")
CONTENT_RE = re.compile(".{5,}")


class FormPage(MainPage):
    def get(self):
        self.render("newpost.html", **params)

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        self.error_handling(subject, content)

    def error_handling(self, p_subject, p_content):
        params["subject"] = p_subject
        params["content"] = p_content

        subject_match = re.match(SUBJECT_RE, p_subject)
        content_match = re.match(CONTENT_RE, p_content)
        if subject_match and content_match:
            blogpost = BlogData(subject=p_subject, content=p_content)
            blogpost.put()
            blogpost_id = blogpost.key().id()
            # add code to refill cache
            memcache.flush_all()

            # next few lines reset params
            params["title_err"] = ""
            params["content_err"] = ""
            params["subject"] = ""
            params["content"] = ""

            self.redirect(str(blogpost_id))
            return
        # need to include return statement here after putting in code
        # for 'success' page

        # next code is to handle errors
        if not subject_match:
            params["title_err"] = """Sorry, that is not a valid
            subject entry (minumum 5 characters)"""
        else:
            params["title_err"] = ""
        if not content_match:
            params["content_err"] = """Sorry, that is not a valid
             blog entry (minumum 5 characters)"""
        else:
            params["content_err"] = ""
        self.render("newpost.html", **params)
