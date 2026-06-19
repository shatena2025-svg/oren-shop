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
    
    def total_price(self):
        total = 0
        for item in self.cart_items:
            t = item.price * item.quantity
            total += t 
        return total
    
    def get_status_pertion(self):
        if self.status == 'pending':
            return "(سبد خرید)در حال انتظار"
        if self.status == 'paid':
            return "پرداخت شده"
        if self.status == 'sent':
            return "ارسال شده"
        if self.status == 'rejected':
            return "رد شده"
