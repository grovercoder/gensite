import markdown
import frontmatter
from slugify import slugify

class Content:
    def __init__(self, source=""):

        self.meta = {}
        self.content = ""
        self.source_file = source
        # to be set by an external method
        self.list_content = ""

        if source:
            data = frontmatter.load(source)
            
        if isinstance(data, frontmatter.Post):
            keys = data.keys()
            for key in keys:
                keylower = key.lower()
                self.meta[keylower] = data[key]
            
            self.content = data.content
            
    def slug(self):
        return slugify(self.meta.get("title", ""))

    def markdown(self):
        return self.content

    def html(self):
        return markdown.markdown(self.content, extensions=['fenced_code'])

    # def listItem(self):

    #     if not self.list_template:
    #         return ""
        
    #     purl = f"{self.post_url}/{slugify(self.meta.get('title', ''))}"
    #     self.list_template.replacePlaceholder("{post_url}", purl)
    #     self.list_template.replacePlaceholder("{post_title}", self.meta.get("title", ""))
    #     self.list_template.replacePlaceholder("{post_date}", self.meta.get("published", ""))
    #     self.list_template.replacePlaceholder("{post_summary}", self.meta.get("summary", ""))
    #     # print(f"listitem content: {self.list_template.content()}")
    #     return self.list_template.content()

        
