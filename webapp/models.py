# encoding: utf-8

from sqlalchemy.ext.declarative import declarative_base
from webapp import db

Base = declarative_base()

class Tree(db.Model):
  __tablename__ = 'tree'
  
  id = db.Column(db.Integer(), primary_key=True)
  
  type = db.Column(db.Integer())
  public = db.Column(db.Integer())
  author = db.Column(db.String(255))
  email = db.Column(db.String(255))
  
  address = db.Column(db.String(255))
  postalcode = db.Column(db.String(255))
  city = db.Column(db.String(255))
  
  picture = db.Column(db.Integer())
  descr = db.Column(db.Text())
  
  lat = db.Column(db.Numeric(precision=10,scale=7))
  lng = db.Column(db.Numeric(precision=10,scale=7))
  
  external_id = db.Column(db.String(255))
  created_at = db.Column(db.DateTime())
  updated_at = db.Column(db.DateTime())
  type_suggestion = db.Column(db.Integer())
  
  tree_type_old = db.Column(db.String(255))
  tree_type_new = db.Column(db.String(255))
  chop_reason = db.Column(db.String(255))
  
  
  
  def __init__(self):
    pass

  def __repr__(self):
    return '<Tree %r>' % self.id
