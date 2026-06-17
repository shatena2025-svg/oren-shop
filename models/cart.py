from sqlalchemy import *  
from extentions import db
from sqlalchemy.orm import backref

class Cart(db.Model):
    __allow_unmapped__ = True  
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    status = Column(String(50),default='pending') 
    user_id =Column(Integer,ForeignKey('users.id'),nullable=False)
    
    user = db.relationship('User', backref=backref('carts' , lazy='dynamic'))
