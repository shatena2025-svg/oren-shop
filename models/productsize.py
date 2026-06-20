from sqlalchemy import *  
from extentions import db, get_current_time

class ProductSize(db.Model):
    __tablename__ = 'product_sizes'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    size = Column(Enum('S', 'M', 'L', 'XL', 'XXL', 'XXXL', name='size_enum'), nullable=False)
    stock = Column(Integer, default=0)
    price = Column(Integer, nullable=True)
    sort_order = Column(Integer, default=0)
    date_created = Column(String(15), default=get_current_time)
    
    product = db.relationship('Product', back_populates='sizes')