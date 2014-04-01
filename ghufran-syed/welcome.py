import webapp2
import jinja2
import os
import security

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


form_params = {"username": "",
               "username_err": "",
               "password_1_err": "",
               "password_2_err": "",
               "email": "",
               "email_err": ""}


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(**params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class WelcomeHandler(Handler):
    def get(self):
        user_id_check = (security.check_secure_val
                         (self.request.cookies.get('user_id')))
        if user_id_check:
            form_params["username"] = user_id_check
            self.render('welcome.html', **form_params)
        else:
            self.redirect("/signup")
