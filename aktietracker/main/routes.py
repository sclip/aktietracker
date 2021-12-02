from flask import Blueprint
from flask import render_template, jsonify, request
from flask_login import login_required, current_user
from aktietracker.main.forms import NewWatchlistForm, AddStockForm
from loguru import logger

from aktietracker.models import Watchlist, Stock
from aktietracker import db

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


@main.route("/watchlists", methods=["GET", "POST"])
@login_required
def watchlists():

    watchlists_ = current_user.watchlists

    print(watchlists_)

    return render_template("watchlists.html", selected_button="watchlists")


@main.route("/process_get_watchlists", methods=["GET", "POST"])
def process_get_watchlists():
    user_watchlists = current_user.watchlists
    return jsonify({"watchlists": [x.name for x in user_watchlists], "success": True})


@main.route("/process_watchlist_request", methods=["GET", "POST"])
def process_watchlist_request():
    user_watchlists = current_user.watchlists

    for watchlist in user_watchlists:
        if watchlist.name == request.get_data(as_text=True).split("=")[1]:
            return jsonify({"stocks": [stock.ticker for stock in watchlist.stocks], "success": True})

    return jsonify({"stocks": ["None"], "success": False})


@main.route("/process_add_watchlist", methods=["GET", "POST"])
def process_add_watchlist():
    """ Create a new watchlist and add it to the database """

    data = [x.split('=') for x in request.get_data(as_text=True).split("&")][0]
    new_watchlist_name = " ".join(data[1].split("+"))
    # some wack stuff has to be done for it to work

    if 0 < len(new_watchlist_name) < 120:
        watchlist = Watchlist(
            name=new_watchlist_name,
            user_id=current_user.id
        )

        db.session.add(watchlist)
        db.session.commit()

        return jsonify({"success": True})

    return jsonify({"success": False})


@main.route("/process_add_stock", methods=["GET", "POST"])
def process_add_stock():
    user_watchlists = current_user.watchlists

    data = [x.split('=') for x in request.get_data(as_text=True).split("&")]

    for watchlist in user_watchlists:
        if watchlist.name == data[1][1]:  # data[1][1] is the watchlist name
            new_stock_ticker = data[0][1]  # the stock ticker

            # todo: validate tickers
            # todo: add the option to add tickers with company names
            # todo:  ... if valid_ticker(): ...

            stock = Stock(
                ticker=new_stock_ticker,
                watchlist_id=watchlist.id
            )

            db.session.add(stock)
            db.session.commit()

            logger.info(f"Successfully added stock to watchlist ({new_stock_ticker})")
            return jsonify({"success": True})

    return jsonify({"success": False})
