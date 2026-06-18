from sqlalchemy import *  
from extentions import db
from extentions import db , get_current_time


class Product(db.Model):
    __allow_unmapped__ = True  
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)  
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False) 
    price = Column(Integer, nullable=False, index=True)
    active = Column(Integer, nullable=False, index=True)
    date_created = Column(String(15), default=get_current_time) 

