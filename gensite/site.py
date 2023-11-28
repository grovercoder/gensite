
import os
from pathlib import Path
import shutil
from gensite.template import Template
from gensite.content import Content
from bs4 import BeautifulSoup

class Site:
    def __init__(self, source=None, template_dir=None, dist_dir=None, post_dir=None):
        self.source = source or os.getcwd()
        self.templates = []
        # where to find templates
        self.templateDir = template_dir or f"{self.source}/template"
        # where to find post entries
        self.postdir = post_dir or f"{self.source}/posts"
        # where to create the site output
        self.distdir = dist_dir or f"{self.source}/dist"
        

        self.posts = []

        # load template files
        self.loadTemplates()
        self.loadPosts()

        # self._dump()

        # use the templates to generate the site
        # self.process()

    def _dump(self): 
        print(self.__dict__)

    def loadTemplates(self):
        if not os.path.exists(self.templateDir):
            raise FileNotFoundError
        
        tpath = Path(self.templateDir)
        self.templates = list(tpath.rglob("*.html"))
        
    
    def build_dist_structure(self):
        if os.path.exists(self.distdir):
            shutil.rmtree(self.distdir, ignore_errors=True)

        shutil.rmtree(self.distdir, ignore_errors=True)
        os.mkdir(self.distdir)

        src = Path(self.source)
        child_directories = [entry for entry in src.iterdir() if entry.is_dir()]
        ignore_dirs = ["dist", "css", "posts", "template"]

        # copy any generic directory to the dist folder
        # "handled" directories should be ignored at this stage
        for child in child_directories:
            dname = child.resolve().name
            if not dname in ignore_dirs:
                # print(f"cp {child} -> {self.distdir}/{dname}")
                shutil.copytree(child, f"{self.distdir}/{dname}")

        self.copyCSS()

    def copyCSS(self, include_map=False):
        src_css = f"{self.source}/css"
        target_dir = f"{self.distdir}/css"
        os.mkdir(target_dir)

        cssdir = Path(src_css)
        cssfiles = cssdir.glob("*.css")

        for f in cssfiles:
            target_file = f"{target_dir}/{f.name}"
            shutil.copy(f, target_file)

        if include_map:
            mapfiles = cssdir.glob("*.css.map")
            for f in mapfiles:
                target_file = f"{target_dir}/{f.name}"                
                shutil.copy(f, target_file)
    

    def loadPosts(self):
        if not os.path.exists(self.postdir):
            raise Exception(f"could not find posts directory at {self.postdir}")

        ltf = f"{self.templateDir}/listitem.html"
        listtemplate = None

        ppath = Path(self.postdir)
        posts = list(ppath.rglob("*.md"))
        posts_url = "/posts"
        self.posts = []

        for post in posts:
            content = Content(post)

            if os.path.exists(ltf):
                # Generate the list item template, replace the values, and store it with the content
                listtemplate = Template(ltf)
                listtemplate.replacePlaceholder("{post_url}", f"{posts_url}/{content.slug()}.html")
                listtemplate.replacePlaceholder("{post_title}", content.meta.get("title", ""))
                if "published" in content.meta and content.meta.get('published'):
                    listtemplate.replacePlaceholder("{post_date}", content.meta.get("published", ""))

                listtemplate.replacePlaceholder("{post_summary}", content.meta.get("summary", ""))
                content.list_content = listtemplate.content()

            self.posts.append(content)

    # Generate the site's index.html file based on the template index.html
    def generate_home(self):
        template = Template(f"{self.templateDir}/index.html")
        
        listcontent = ""
        for post in sorted(self.posts, key=lambda x: x.meta.get("published"), reverse=True):
            listcontent = listcontent + post.list_content

        template.replacePlaceholder("{placeholder=post_list}", listcontent)
        
        with open(f"{self.distdir}/index.html", 'w') as fh:
            fh.write(template.content())

    def adjustPageTitle(self, sourceHtml="", post=None) :
        if not post:
            return sourceHtml
        
        soup = BeautifulSoup(sourceHtml, 'html.parser')
        title_tag = soup.title
        if title_tag and post.meta.get('title'):
            newTitle = [
                post.meta.get('title'),
                title_tag.string
            ]


            soup.title.string = " : ".join(newTitle)
            
        return soup.prettify()


    def generate_posts(self):
        template = None
        home_template = f"{self.templateDir}/index.html"
        post_template = f"{self.templateDir}/posts.html"
        localTemplatePath = post_template
        postdist = f"{self.distdir}/posts"

        if not Path(localTemplatePath).exists():
            localTemplatePath = home_template
        
        if not Path(localTemplatePath).exists():
            raise Exception("Could not determine template to use for posts")
        
        Path(postdist).mkdir(exist_ok=True)

        for post in self.posts:
            if post:
                template = Template(localTemplatePath)
                post_file = f"{postdist}/{post.slug()}.html"
                content = template.replacePlaceholder("{placeholder=post}", post.html())
                content = self.adjustPageTitle(content, post)
                

                with open(post_file, 'w') as pf:
                    pf.write(content)


    def generate_RootPages(self):
        rootpages = Path(self.source).glob("*.md")

        for pg in rootpages:
            template = Template(f"{self.templateDir}/index.html")
            content = Content(pg)
            target = f"{self.distdir}/{pg.stem}.html"
            template.replacePlaceholder("{placeholder=post_list}", content.html())
            templateHtml = self.adjustPageTitle(template.content(), content)

            with open(target, "w") as fh:
                fh.write(templateHtml)

    def build(self):
        self.build_dist_structure()
        self.generate_home()
        self.generate_posts()
        self.generate_RootPages()

            





