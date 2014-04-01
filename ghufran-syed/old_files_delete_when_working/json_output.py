import webapp2
import jinja2
import os
import re
from google.appengine.ext import db
import json


SUBJECT_RE = re.compile(".{5,}")
CONTENT_RE = re.compile(".{5,}")


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

params = {}


class BlogData(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now=True, auto_now_add=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        blog_query = db.GqlQuery("""SELECT * FROM BlogData
                                 ORDER BY created DESC
                                 LIMIT 0,10""")
        params["blog_query"] = blog_query
        self.render("frontpage.html", **params)


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

            # next few lines reset params
            params["title_err"] = ""
            params["content_err"] = ""
            params["subject"] = ""
            params["content"] = ""

            self.redirect("/blog/" + str(blogpost_id))
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


class PermalinkPage(Handler):
    def get(self, blogpost_id_p):
        blog_query = BlogData.get_by_id(int(blogpost_id_p))
        params["blog_query"] = blog_query
        self.render("permalink.html",
                    **params)


class MainPageJson(Handler):
    def get(self):
        blog_query = db.GqlQuery("""SELECT * FROM BlogData
                                 ORDER BY created DESC
                                 LIMIT 0,10""")
        json_results = []
        for element in blog_query:
            subject = element.subject
            content = element.content
            created = element.created.strftime("%c")
            last_modified = element.created.strftime("%c")
            json_results.append({
                                "subject": subject,
                                "content": content,
                                "created": created,
                                "last_modified": last_modified
                                })

        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(json_results))


class PermalinkJson(Handler):
    def get(self, blogpost_id_p):
        blog_query = BlogData.get_by_id(int(blogpost_id_p))
        json_results = []
        subject = blog_query.subject
        content = blog_query.content
        created = blog_query.created.strftime("%c")
        last_modified = blog_query.created.strftime("%c")
        json_results.append({
                            "subject": subject,
                            "content": content,
                            "created": created,
                            "last_modified": last_modified
                            })

        self.response.headers['Content-Type'] = 'application/json'
        self.write(json.dumps(json_results))


app = webapp2.WSGIApplication([
    (r'/blog/(\d+)', PermalinkPage),
    (r'/blog/(\d+).json', PermalinkJson),
    (r'/blog', MainPage),
    (r'/blog.json', MainPageJson),
    (r'/blog/newpost', FormPage),
], debug=True)
