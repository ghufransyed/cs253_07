from mainhandler import Handler, params
from get_data import get_data


class WikiPage(Handler):
    def get(self, wikipage_address):
        if get_data(wikipage_address):
            self.render("wikipage.html", **params)
        else:
            self.redirect("_edit" + wikipage_address)
