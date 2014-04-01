from mainhandler import Handler
from models import BlogData
import json


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
