from flask import(
  Blueprint,
  render_template,
  redirect,
  url_for,
  abort,
  session
)
from . import db
from flask_login import(
  login_required,
  current_user
)
from sqlalchemy import *
main = Blueprint('main', __name__, template_folder='templates')
from .models import User, Accounts, Messages
from jinja2 import TemplateNotFound


@main.route('/')
def index():
  return render_template('index.html')

@main.route('/signup')
def signup():
  if current_user.is_authenticated:
    return redirect(url_for('main.profile'))
  else:
    return render_template('signup.html')

@main.route('/login')
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.profile'))
  else:
    return render_template('login.html')

@main.route('/login_psw')
def login_psw():
  if 'social_security_number' not in session:
    return redirect(url_for('main.index'))
  if current_user.is_authenticated:
    return redirect(url_for('main.profile'))
  else:
    return render_template('login_psw.html')


@main.route('/profile')
@login_required
def profile():
  return render_template('profile.html', user = current_user)

@main.route('/accounts')
@login_required
def accounts():
  user = current_user
  acc = Accounts.query.filter_by(social_security_number = user.social_security_number).first()
  return render_template('accounts.html', user = user, acc = acc)

@main.route('/messages')
@login_required
def messages():
  user = current_user
  message = Messages.query.filter_by(social_security_number = user.social_security_number).all()
  return render_template('messages.html', user = user, message = message)

@main.route('/')
@main.route('/', defaults={'page': 'index'})
@main.route('/<page>')
def users(page):
  try:
    return render_template('pages/%s.html' % page)
  except TemplateNotFound:
    return render_template('404.html')
