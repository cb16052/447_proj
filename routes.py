from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Study
import yfinance as yf

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "fpoijaf984qiub98rtbnusp9uwrnb150vmpautj"

@app.route("/")
def home():
	return render_template("home.html")

@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		new_email = request.form.get("email")
		if new_email == User.query.filter_by(email=request.form.get("email")).first().email:
			flash("Email exists.  Please login")
			return redirect(url_for("login"))
		user = User(email=new_email,
			   		name=request.form.get("name"),
					password=generate_password_hash(request.form.get("password"), method='scrypt'))
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("login"))
	return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = User.query.filter_by(
			email=request.form.get("email")).first()
		if not (user and check_password_hash(user.password, request.form.get("password"))):
			flash("Bad login.  Try again.")
			return redirect(url_for("home"))
		login_user(user)
		return redirect(url_for("studies"))
	return render_template("login.html")

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

@app.route("/studies")
@login_required
def studies():
	studies = Study.query.filter_by(user_id=current_user.id).all()
	return render_template('studies.html', studies=studies, name=current_user.name)

@app.route("/add_study", methods=["GET", "POST"])
@login_required
def add_study():
	if request.method == "POST":
		newstudy = Study(user_id=current_user.id, ticker=request.form.get("ticker"))
		db.session.add(newstudy)
		db.session.commit()
		return redirect(url_for("studies"))
	return render_template('add_study.html')
