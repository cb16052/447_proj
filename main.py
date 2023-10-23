from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Study
import yfinance as yf
from routes import app

login_manager = LoginManager()
login_manager.login_view = "home"
login_manager.init_app(app)

db.init_app(app)

with app.app_context():
	db.create_all()

@login_manager.user_loader
def loader_user(user_id):
	return User.query.get(user_id)

if __name__ == "__main__":
	app.run()
