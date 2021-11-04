from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from aktietracker import db, bcrypt
from aktietracker.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from aktietracker.models import User

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash(f"Account successfully created for {form.email.data}", category="success")
        return redirect(url_for("users.login"))

    return render_template("register.html", title="Sign Up", form=form, selected_button="register")


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Logged in successfully!", category="success")

            # first time I actually find an use for the walrus
            # this could be done in other ways, but i'm doing this
            if next_page := request.args.get("next"):
                return redirect(next_page)

            return redirect(url_for("main.dashboard"))
        print("Unsuccessful login")
        flash("Login unsuccessful.", category="danger")
    return render_template("login.html", title="Sign In", form=form, selected_button="login")


@users.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("main.index"))

    logout_user()
    return redirect(url_for("main.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if not current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account information has been updated", category="info")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.email.data = current_user.email

    return render_template("account.html", title="Account", form=form, selected_button="account")
