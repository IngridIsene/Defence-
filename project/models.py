from flask_login import UserMixin, current_user
from . import db 
from sqlalchemy import Integer, String
import os
import base64
import onetimepass

db.metadata.clear

class User(UserMixin,  db.Model):
  __tablename__ = 'User'
  id = db.Column(db.Integer, primary_key=True)
  social_security_number = db.Column(db.String(16), db.ForeignKey("User.social_security_number"), unique=True)
  email = db.Column(db.String(100), unique=True)
  password = db.Column(db.String(256))
  name = db.Column(db.String(1000))
  phone_number = db.Column(db.String(15))
  address = db.Column(db.String(1000))
  post_code = db.Column(db.String(15))
  validated = db.Column(db.Boolean, default = False)
  otp_secret = db.Column(db.String(16))
  attempts = db.Column(db.Integer, default = 5)
  
  def __init__(self, **kwargs):
    super(User, self).__init__(**kwargs)
    if self.otp_secret is None:
      self.otp_secret=base64.b32encode(os.urandom(10)).decode('utf-8')

  def get_totp_uri(self):
    return 'otpauth://totp/RNI:{0}?secret={1}&issuer=RNI' \
    .format(self.social_security_number, self.otp_secret)

  def verify_totp(self, token):
    return onetimepass.valid_totp(token, self.otp_secret)

  def __repr__(self):
    return '<User %r>' % (self.social_security_number)

class Accounts(UserMixin, db.Model):
  __tablename__ = 'Accounts'
  id = db.Column(db.Integer, primary_key=True)
  social_security_number = db.Column(db.String(16), db.ForeignKey("Accounts.social_security_number"), unique=True)
  acc_num_exp = db.Column(db.Integer, unique = True)
  acc_num_exp_bal = db.Column(db.Integer, default = 0)
  acc_num_sav = db.Column(db.Integer, unique = True)
  acc_num_sav_bal = db.Column(db.Integer, default = 0)

  def acc_num_gen(m=1000):
    from random import sample
    
    value_array = sample(range(100000, 999999),m)

    affiliation = '3141' # identifies the bank
    control = '5432765432'
    k1 = 0
    numbers=[]
    for n in range(len(value_array)): 
      for i in range(len(control)):
        bank_number = affiliation + str(value_array[n])
        k1 += int(control[i])*int(bank_number[i])
      k1 = (11-k1)%11
      if k1 !=10:
        bank_number += str(k1)
        numbers.append(bank_number)
    return numbers

  def transfer(acc1, acc2, amount):
    
    from flask import flash

    if (len(str(acc1)) != 11) or (len(str(acc2)) !=11):
      return flash('invalid account format')
 

    try:
      source_account = Accounts.query.filter_by(acc_num_exp = acc1).first()
      if (source_account != None) and (current_user.social_security_number==source_account.social_security_number):
        if (source_account.acc_num_exp_bal - amount) >= 0:
          source_account.acc_num_exp_bal -= amount
        else: 
          return flash('insufficient funds')
      
      elif (source_account == None): 
        source_account = Accounts.query.filter_by(acc_num_sav = acc1).first()
        if (source_account.acc_num_sav_bal != None) and (current_user.social_security_number==source_account.social_security_number):
          if (source_account.acc_num_sav_bal - amount ) >= 0:
            source_account.acc_num_sav_bal -= amount
        else: 
          return flash('Insufficient funds')
      else: 
        raise TypeError
    except TypeError:
      return flash('Invalid source account')

    destination_account = None
    
    try:
      destination_account = Accounts.query.filter_by(acc_num_exp = acc2).first() 
      if destination_account != None:
        destination_account.acc_num_exp_bal += amount
      elif destination_account == None:
        destination_account = Accounts.query.filter_by(acc_num_sav = acc2).first()
        destination_account.acc_num_sav_bal += amount
      else:
        raise TypeError
    except TypeError:
      return flash('Invalid destination account')

    return db.session.commit(), flash('successful transaction')


class Messages(UserMixin, db.Model):
  __tablename__ = 'Messages'
  id = db.Column(db.Integer, primary_key=True)
  social_security_number = db.Column(db.String(16), db.ForeignKey("Messages.social_security_number"))
  content_title = db.Column(db.String(56), nullable=True)
  content = db.Column(db.String(1000), nullable=True)

#will add content title to messages
