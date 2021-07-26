from flask import Flask, render_template
import requests

name = "Alexis"

github_projects_url = "https://api.github.com/users/acumpstone/repos"
projects_from_github = requests.get(github_projects_url).json()

projects = []

for project in projects_from_github:
    name = project["name"]
    desc = project["description"]
    url = project["html_url"]

    projects.append({
        "name": name,
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

@app.route("/projects")
def projects_page():
    return render_template("projects.html", name=name, projects=projects)

@app.route("/contact")
def contact_page():
    return render_template("contact.html", name=name)