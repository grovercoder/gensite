import os
import markdown

class Template:
    def __init__(self, source=None):
        self.file = source
        self.raw = ""
        self.in_progress = ""

        if not self.file:
            raise Exception("Template file not specified")

        if not os.path.exists:
            raise Exception(f"Template '{self.file}' not found")

        with open(self.file, 'r') as src:
            self.raw = src.read()
        
    def content(self):
        if not self.in_progress :
            self.in_progress = self.raw
        
        return self.in_progress

    def replacePlaceholder(self, placeholder, content):
        if not self.in_progress :
            self.in_progress = self.raw
        
        # - self.raw should be treated as immutable
        # - multiple placeholders may be applied as well
        # - so we will use the self.in_progress variable as the transisitional content
        self.in_progress = self.in_progress.replace(placeholder, content)
        return self.in_progress

    

