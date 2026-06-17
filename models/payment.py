from sqlalchemy import *  
from extentions import db

class Payment(db.Model):
    __allow_unmapped__ = True  
    __tablename__ = 'Payments'
    id = Column(Integer, primary_key=True)
    status = Column(String(50),default='pending') 
    cart_id =Column(Integer, ForeignKey('carts.id'),nullable=False)
    cart = db.relationship('Cart', backref='payments')
