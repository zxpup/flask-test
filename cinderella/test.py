#! /usr/bin/python3
# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/Cinderella'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////test.db'
db = SQLAlchemy(app)


class Accounts(db.Model):
    account_id = db.Column(db.String(30), nullable=False, primary_key=True)
    password = db.Column(db.String(128))
    nickname = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    titles = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(30), nullable=False)
    province = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    birthday = db.Column(db.String(50), nullable=False)
    promo_code = db.Column(db.String(30))
    agent_id = db.Column(db.String(30))
    type = db.Column(db.String(30))
    status = db.Column(db.String(30))
    create_datetime = db.Column(db.String(50))

    def __repr__(self):
        return '<Accounts %r>' % self.account_id


class BankCard(db.Model):
    account_id = db.Column(db.String(30), nullable=False, primary_key=True)
    bank = db.Column(db.String(30), nullable=False)
    branch = db.Column(db.String(30), nullable=False)
    card_no = db.Column(db.String(40), nullable=False)
    account = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<BankCard %r>' % self.account_id


class PromoCodes(db.Model):
    promo_code = db.Column(db.String(30), primary_key=True)

    def __repr__(self):
        return '<PromoCodes %r>' % self.account_id


class Sequence(db.Model):
    sequence_name = db.Column(db.String(30), nullable=False, primary_key=True)
    sequence_value = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Sequence %r>' % self.sequence_name


class Vouchers(db.Model):
    account_id = db.Column(db.String(30), nullable=False)
    voucher_no = db.Column(db.String(40), nullable=False, primary_key=True)
    amount = db.Column(db.Float(asdecimal=True), nullable=False)
    deposit = db.Column(db.Integer, nullable=False)
    create_datetime = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer)
    remark = db.Column(db.String(128))

    def __repr__(self):
        return '<Vouchers %r>' % self.voucher_no

db.create_all()
