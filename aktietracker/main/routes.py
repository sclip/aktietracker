from flask import Blueprint
from flask import render_template, jsonify, request
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


@main.route("/process_watchlist_request", methods=["GET", "POST"])
def process_watchlist_request():
    print(request.get_data(as_text=True).split("=")[1])
    user_watchlists = current_user.watchlists
    print(user_watchlists)
    for watchlist in user_watchlists:
        if watchlist.name == request.get_data(as_text=True).split("=")[1]:
            return jsonify({"stocks": watchlist.stocks, "success": True})

    return jsonify({"stocks": ["None"], "success": False})
