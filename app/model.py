from sqlalchemy import Column, Integer, Float, String,TIMESTAMP , text , ForeignKey
from .database import Base 


class Course(Base):
    __tablename__ = "classes"  

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)  
    duration = Column(Float, nullable=False)
    website = Column(String, nullable=False) 
    creator_id = Column(Integer , ForeignKey("users.id", onupdate="CASCADE") , nullable=False)




class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True , nullable=False)
    email = Column(String , nullable=False , unique=True)
    password = Column(String , nullable=False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable= False ,server_default=text("now()") )