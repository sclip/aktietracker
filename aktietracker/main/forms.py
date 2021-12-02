from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from yahooquery import Ticker


class NewWatchlistForm(FlaskForm):

	name = StringField(
		"Watchlist Name",
		validators=[
			DataRequired(),
			Length(max=50)
		]
	)

	submit = SubmitField("Add watchlist")

	def validate_name(self, name):
		"""Check whether or not the name already exists in the database for this user"""
		watchlist = current_user.watchlists.query.filter_by(name=name.data).first()

		if watchlist:
			# Soft-force unique names for watchlists, while allowing different users to have the same watchlist name
			raise ValidationError("You already have a watchlist with this name.")


class AddStockForm(FlaskForm):
	ticker = StringField(
		"Ticker",
		validators=[
			DataRequired()
		]
	)

	def validate_ticker(self, ticker):
		"""Check whether or not the ticker is valid"""

		stock = Ticker(ticker)
		data = stock.asset_profile

		if data[ticker].__contains__("Quote not found"):
			raise ValidationError("Invalid ticker. Make sure that you input a ticker that Yahoo Finance can recognize.")

	submit = SubmitField("Sign In")
