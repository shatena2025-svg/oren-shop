from sqlalchemy import *  
from extentions import db , get_current_time
from sqlalchemy.orm import backref

class ProductColor(db.Model):
    __allow_unmapped__ = True  
    __tablename__ = 'product_colors'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    color_name = Column(String(50), nullable=False)  
    color_code = Column(String(7), nullable=True)    
    stock = Column(Integer, default=0)              
    price = Column(Integer, nullable=True)           
    sku = Column(String(50), unique=True, nullable=True) 
    sort_order = Column(Integer, default=0)
    date_created = Column(String(15), default=get_current_time)
    
    product = db.relationship('Product', back_populates='colors')

