from flask import Blueprint
from flask import render_template
from flask_login import login_required, current_user

# from main.models import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/index")
def index():
    # posts = Post.query.all()
    return render_template("index.html", selected_button="welcome")


@main.route("/settings")
@login_required
def settings():
    # posts = Post.query.all()
    return render_template("settings.html", selected_button="settings")


@main.route("/dashboard")
@login_required
def dashboard():
    # posts = Post.query.all()
    return render_template("dashboard.html", selected_button="dashboard")


@main.route("/watchlists")
@login_required
def watchlists():
    # posts = Post.query.all()
    return render_template("watchlists.html", selected_button="watchlists")
