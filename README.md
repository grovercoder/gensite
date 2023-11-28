# gensite.py

`gensite` is a tool for creating a static website based on a template and markdown files.

## Usage

1. clone this project
1. (optional) Create a virtual workspace and activate it:

    ```bash
    cd <project_root>
    python3 -v venv .venv
    source .venv/bin/activate
    ```

1. install dependencies

    ```bash
    cd <project_root>
    pip install -r requirements.txt
    ```

1. ensure the `<project_root>/gensite.py` file is executable

    ```bash
    cd <project_root>
    chmod +x gensite.py
    ```

1. Create a website folder.  The folder should contain the following structure:

    ```bash
    my_website
    - css
      - style.css
    - img
      - # place static site images here
    - posts
      - # store your site's postings here as *.md files
    - template
      - index.html  # your common layout
      - posts.html  # (optional) for article layouts
      - listitem.html  # the html snippet for listing postings
    . about.md  # (optional) - or any other fixed static page
    ```

    See more details below.

1. Change into your website folder and call the `gensite.py` file


    ```
    cd path/to/my_website
    python3 path/to/gensite.py
    ```

    > Note: If you have set up a virtual workspace, then you should do this from inside that workspace.

This will create a `my_website/dist` folder containing your static site.  The contents of this `dist` folder can be copied to your web server.

## Serving the generated site

Copy the contents of the `dist` folder to your web server.

For development purposes, you can use the "Live Server" extension in VS Code (assuming you are using VS Code of course).  You can change the `liveServer.settings.root` value in your workspace settings.json file to "/dist".  This will use the correct web root and the URL path references will work as needed.

## Website setup

`gensite.py` has been refactored from a [previous version](https://github.com/grovercoder/static_site).  That earlier draft tightly coupled the site templates with the generation code.  `gensite.py` attempts to decouple the generation code from the sites content files.  To do so, some assumptions have been made:

- Your website folder contains a `/template` directory, and that contains:
    - `index.html` which is the Layout for your site.  Place the text `{placeholder=post_list}` where you want the dynamic content to be.
    - `listitem.html` - this is an HTML snippet that represents what a summary list item looks like for a post.  You can use the following place holders:
        - `{post_url}` - becomes the generated URL to the post
        - `{post_title}` - the defined title for the post
        - `{post_date}` - the published_date for the post
        - `{post_summary}` - the summary text for the post
- Your website's postings are stored in a `/posts` directory.
- Your page styles are defined in the `/css` folder.  Note that the only real requirement here is a `style.css` file.  You can expand that to include `style.css.map` and/or SCSS files if desired.
- Your sites image files are stored in the `/img` folder.  This is copied verbatim into the generated site.
- any root level static pages are defined as `*.md` files at the root of the website folder.

### Templates

Your page template(s) should define a `<title>` tag.  The contents of this tag is used as the default title.  Post titles are pre-pended to this during generation.

### Posts

The filenames for your posts are arbitrary.  However, I recommend you store them with a datestamp section - once you generate numerous posts, it will be easier to find the files if needed.  i.e. `20231201-some-meaningful-text.md`

Posts have a "frontmatter" section where you can define various properties.  This is done by adding a section to the start of your markdown file using the `---` characters.

```markdown
---
title: "My Title"
published: "2023-11-29"
summary: "A short description for your post"
---
# My Post Title

My post content goes here.
```

> All front matter properties should be quoted strings.

The current list of properties used:

- `title` - the title for your post.  This value will be prepanded to the page title, so keep it fairly short (for SEO purposes).  The title does not need to match your page's Markdown title, but should be similar.
- `published` - the date/time your post was created/published.  This value is used for sorting the posts.
- `summary` - a short description for your post.  This value is used in the "list of posts".
- `tags` - not fully implemented yet.  This is a comma delimited string of categories for your post.  The intent is to provide a post filter or search that would use this to help group posts into meaningful content.



