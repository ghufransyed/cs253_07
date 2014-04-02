import webapp2
from signup import SignupHandler
from login import LoginHandler
from logout import LogoutHandler
from formpage import FormPage  # change names and ref to data models
from wikipage import WikiPage
# from welcome import WelcomeHandler
# from mainpage import MainPage
# from mainpagejson import MainPageJson
# from permalinkjson import PermalinkJson
# from flushhandler import FlushHandler


app = webapp2.WSGIApplication([
    (r'/signup', SignupHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogoutHandler),
    (r'/(.*)', WikiPage),  # need to change to take strings
    # TODO change WikiPage to test if exists, go to edit page
    # if not , else to retrieve page
    (r'/newpost', FormPage),
    # (r'/', MainPage),
    # (r'/.json', MainPageJson),
    # (r'/(\d+).json', PermalinkJson),
    # (r'/flush', FlushHandler),
    # (r'/welcome', WelcomeHandler), not needed for wiki
], debug=True)
