import webapp2
from signup import SignupHandler
from login import LoginHandler
from logout import LogoutHandler
from formpage import FormPage
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
    (r'/newpost', FormPage),
    # (r'/', MainPage),
    # (r'/.json', MainPageJson),
    # (r'/(\d+).json', PermalinkJson),
    # (r'/flush', FlushHandler),
    # (r'/welcome', WelcomeHandler), not needed for wiki
], debug=True)
