from aktietracker import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    watchlists = db.relationship("Watchlist", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Watchlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    stocks = db.relationship("Stock", backref="watchlist", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Watchlist('{self.stocks}')"


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    watchlist_id = db.Column(db.Integer, db.ForeignKey("watchlist.id"), nullable=False)

    def __repr__(self):
        return f"Stock('{self.ticker}')"
