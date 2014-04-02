import webapp2
from signup import SignupHandler
from login import LoginHandler
from logout import LogoutHandler
from wikipage import WikiPage


PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([
    (r'/signup', SignupHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/_edit' + PAGE_RE, EditPage),
    (r'/_history' + PAGE_RE, HistoryPage),
    (PAGE_RE, WikiPage),
], debug=True)
