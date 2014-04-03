from wikipage import WikiPage
from models import WikiData
from google.appengine.api import memcache
import security
import logging
from get_data import get_data, params


class EditPage(WikiPage):
    def get(self, wikipage_address):
        cookie_p = self.request.cookies.get('user_id')
        if cookie_p:
            user_id_check = (security.check_secure_val
                             (cookie_p))
            if user_id_check:
                params["username"] = user_id_check
                get_data(wikipage_address)
                self.render("editpage.html", **params)
        else:
            self.redirect("/signup")

    def post(self, wikipage_address):
        logging.error(wikipage_address)
        user_id_check = (security.check_secure_val
                         (self.request.cookies.get('user_id')))
        if user_id_check:
            params["username"] = user_id_check
        else:
            self.redirect("/login")
        page_content = self.request.get("content")
        if get_data(wikipage_address):
            parent_p = params["wikipage_query"].key
        else:
            parent_p = None
        page_data = WikiData(
            id=wikipage_address,
            parent=parent_p,
            content=page_content,
            author=user_id_check)
        page_data.put()
        memcache.set(page_data.key.id(), page_data)

        # next few lines reset params
        params["content_err"] = ""
        params["content"] = ""

        self.redirect(wikipage_address)
        return
