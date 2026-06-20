from sqlalchemy import *  
from extentions import db, get_current_time

class Product(db.Model):
    __allow_unmapped__ = True  
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)  
    name = Column(String(50), unique=True, nullable=False, index=True)
    short_description = Column(Text, nullable=False) 
    description = Column(Text, nullable=False) 
    price = Column(Integer, nullable=False, index=True)
    active = Column(Integer, nullable=False, index=True)
    
    date_created = Column(String(15), default=get_current_time) 
    gender = Column(Enum('male', 'female', 'unisex', name='gender_enum'), default='unisex')
    category = Column(Enum('لباس', 'شلوار', 'کفش', 'تیشرت', 'پیراهن', 'کت', 'ژاکت', name='category_enum'), default='لباس')
    
    images = db.relationship('ProductImage', back_populates='product', lazy='dynamic')
    colors = db.relationship('ProductColor', back_populates='product', lazy='dynamic')
    sizes = db.relationship('ProductSize', back_populates='product', lazy='dynamic')