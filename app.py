import os
from pathlib import Path

from flask import Flask, render_template
import requests
import decouple

name = "Alexis"

github_projects_url = "https://api.github.com/users/acumpstone/repos"
projects_from_github = requests.get(github_projects_url).json()

contact = decouple.config("CONTACT_FORM_API", default=None)

projects = []

blog_posts = []

with os.scandir("blog") as it:
    for entry in it:
        if entry.name.endswith(".md") and entry.is_file():
            post_data = Path(entry.path).read_text()

            blog_posts.append({
                "name": entry.name,
                "data": post_data
            })

print(blog_posts)

exit(0)

for project in projects_from_github:
    project_name = project["name"]
    desc = project["description"]
    url = project["html_url"]

    projects.append({
        "name": project_name,
        "desc": desc,
        "url": url,
    })

app = Flask(__name__)

list_of_hobbies = {
    "anime",
    "piano",
    "reading"
}

@app.route("/")
def about_page():
    return render_template("about.html", name=name, list_of_hobbies=list_of_hobbies)

@app.route("/blog")
def blog_entry_page():
    return render_template("blog_listing.html", name=name)

@app.route("/blog/<post_name>")
def blog_listing_page(post_name):
    return render_template("blog_entry.html", name=name, post_name=post_name)

@app.route("/projects")
def projects_page():
    return render_template("projects.html", name=name, projects=projects)

@app.route("/contact")
def contact_page():
    return render_template("contact.html", name=name, api=contact)