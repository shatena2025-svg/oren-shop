from sqlalchemy import *  
from extentions import db

class CartItem(db.Model):
    __allow_unmapped__ = True  
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True)
    product_id =Column(Integer, ForeinKey(products.id),nullable=False)
    cart_id = Column(Integer, ForeinKey(carts.id),nullable=False)
    user = db.relationship('User', backref='carts')
    quantity = Column(Integer)
    
    product = db.relationship('Product',backref='cart_items')
    cart = db.relationship('Cart',backref='cart_items')
