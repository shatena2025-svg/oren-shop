from sqlalchemy import *  
from extentions import db , get_current_time

class Payment(db.Model):
    __allow_unmapped__ = True  
    __tablename__ = 'Payments'
    id = Column(Integer, primary_key=True)
    status = Column(String(50),default='pending')
    price = Column(Integer) 
    token = Column(String(255))
    refid = Column(String(255))
    cart_pan = Column(String(255))
    transaction_id = Column(String(255))
    date_created = Column(String(15), default=get_current_time) 
    cart_id =Column(Integer, ForeignKey('carts.id'),nullable=False)
    cart = db.relationship('Cart', backref='payments')
    
