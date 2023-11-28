import os

class Content:
    def __init__(self, source) :
        self.properties = {}
    
        if source:
            self.load(source)

    
    def load(sef, source):

        if os.path.exists(source):
            with open(source, 'r') as src:
                raw = src.read()

                print(raw)