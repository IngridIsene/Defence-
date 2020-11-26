from flask import Flask, session, g
from datetime import timedelta
from flask_login import LoginManager, login_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
  app = Flask(__name__)

  app.config['SECRET_KEY'] = 'M8iFfMSt-S_kyuf0TUUkXLjf3VhxBxQc2W0SRGE2BUw'

  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db = SQLAlchemy()

  db.init_app(app)
  
  # blueprint for auth routes in our app
  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  # blueprint for non-auth parts of app
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  with app.app_context():
    db.create_all()

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)
  
  from .models import User, Accounts, Messages

  @login_manager.user_loader
  def load_user(social_security_number):
    return User.query.get(int(social_security_number))

  @app.before_request
  def before_request():
    session.permament=True
    app.permanent_session_lifetime=timedelta(minutes=15)
    g.user = current_user

  # blueprint for non-auth parts of app
  from .main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return app

