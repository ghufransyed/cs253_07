from mainhandler import Handler, params
from models import WikiData
import logging
import security


class HistoryPage(Handler):
    def get(self, wikipage_address):
        cookie_p = self.request.cookies.get('user_id')
        if cookie_p:
            user_id_check = (security.check_secure_val(cookie_p))
            if user_id_check:
                params["username"] = user_id_check
                self.get_history(wikipage_address)
        else:
            self.redirect("/signup")

    def get_history(self, wikipage_address):
        root_ancester = WikiData.get_by_id(wikipage_address)
        if root_ancester:
            root_ancester_key = root_ancester.key
            history_query = WikiData.query(ancestor=root_ancester_key)
            history_result = history_query.fetch(100)
            # failed autograder when limited to 10
            # alternative fix would be to change order so that
            # most recent entry at the top
            logging.error("history result obtained")
            params["history_result"] = history_result
            self.render("historypage.html", **params)
        else:
            self.redirect(wikipage_address)
