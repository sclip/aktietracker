from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from aktietracker.models import User


class RegistrationForm(FlaskForm):

	email = StringField(
		"Email",
		validators=[
			DataRequired(),
			Email()
		]
	)

	password = PasswordField(
		"Password",
		validators=[
			DataRequired()
		]
	)

	confirm_password = PasswordField(
		"Confirm Password",
		validators=[
			DataRequired(),
			EqualTo("password")
		]
	)

	submit = SubmitField("Sign Up")

	def validate_email(self, email):
		"""Check whether or not the email already exists in the database"""
		user = User.query.filter_by(email=email.data).first()

		if user:
			print("this2")
			raise ValidationError("Email already in use")


class LoginForm(FlaskForm):
	email = StringField(
		"Email",
		validators=[
			DataRequired(),
			Email()
		]
	)

	password = PasswordField(
		"Password",
		validators=[
			DataRequired()
		]
	)

	remember = BooleanField("Remember Me")

	submit = SubmitField("Sign In")


class UpdateAccountForm(FlaskForm):

	email = StringField(
		"Email",
		validators=[
			DataRequired(),
			Email()
		]
	)

	submit = SubmitField("Update")

	def validate_email(self, email):
		"""Check whether or not the email already exists in the database"""
		if email.data == current_user.email:
			return

		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email already in use")
