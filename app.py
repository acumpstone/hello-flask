import os
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template
import requests
import decouple
import markdown
import sqlite3

# time stamp: 33:30

db_connection = sqlite3.connect("./database.db")

db_cursor = db_connection.cursor()
db_cursor.execute(
    """
CREATE TABLE IF NOT EXISTS anime (
    name TEXT,
    PRIMARY KEY (name)
)
"""
)
db_cursor.close()
db_connection.commit()


name = "Alexis"

github_projects_url = "https://api.github.com/users/acumpstone/repos"
projects_from_github = requests.get(github_projects_url).json()

contact = decouple.config("CONTACT_FORM_API", default=None)

projects = []
blog_posts = []

with os.scandir("blog") as it:
    for entry in it:
        if entry.name.endswith(".md") and entry.is_file():
            raw_post_date, post_name = entry.name.split("_")
            post_name = post_name.rstrip(".md")

            post_date = datetime.strptime(raw_post_date, "%Y-%m-%d")

            post_data = Path(entry.path).read_text()
            html = markdown.markdown(post_data)

            blog_posts.append({
                "name": post_name,
                "date": post_date,
                "html": html
            })

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

@app.route("/")
def about_page():
    db_cursor = sqlite3.connect("./database.db").cursor()
    db_cursor.execute("SELECT * FROM anime")
    list_of_anime = db_cursor.fetchall()
    return render_template("about.html", name=name, list_of_anime=list_of_anime)

@app.route("/blog")
def blog_entry_page():
    return render_template("blog_listing.html", blog_posts=blog_posts)

@app.route("/blog/<post_name>")
def blog_listing_page(post_name):

    for post in blog_posts:
        if post_name == post["name"]:
            return render_template("blog_entry.html", name=name, post=post)

    return "Blog post not found"

@app.route("/projects")
def projects_page():
    return render_template("projects.html", name=name, projects=projects)

@app.route("/contact")
def contact_page():
    return render_template("contact.html", name=name, api=contact)

@app.route("/anime/add/<name>")
def add_item_page(name):
    db_connection = sqlite3.connect("./database.db")
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        "INSERT INTO anime VALUES (:name)",
        {"name": name},
    )
    db_connection.commit()
    return f"Added anime '{name}"