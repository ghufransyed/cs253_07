from mainhandler import Handler
from google.appengine.ext import db
import json


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
