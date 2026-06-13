from sqlalchemy import Column, Integer, String, Text  
from extentions import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    __allow_unmapped__ = True  
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)  
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False, index=True)
    phone = Column(String(11), nullable=False, index=True)
    address = Column(Text, nullable=False, index=True) 