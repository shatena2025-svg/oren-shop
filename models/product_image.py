from sqlalchemy import *  
from extentions import db , get_current_time


class ProductImage(db.Model):
    __allow_unmapped__ = True  
    __tablename__ = 'product_images'
    
    id = Column(Integer, primary_key=True)  
    product_id = Column(Integer,ForeignKey('products.id'),nullable=False)
    image_path = Column(String(255),nullable=False)
    is_primary = Column(Boolean, default=False)
    sort_order = Column(Integer, nullable=False)
    date_created = Column(String(15), default=get_current_time) 

