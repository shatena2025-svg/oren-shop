from sqlalchemy import *  
from extentions import db

class Cart(db.Model):
    __allow_unmapped__ = True  
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True)
    status = Column(String,default='pending') 
    user_id =Column(Integer, ForeinKey(users.id),nullable=False)
    user = db.relationship('User', backref='carts')
