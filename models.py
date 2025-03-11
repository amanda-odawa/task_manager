from sqlalchemy import ForeignKey, Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Category model
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)

# User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)

# Task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    due_date = Column(Date)
    status = Column(String, default = 'Pending')  # Pending, Completed
    priority = Column(String, nullable = False)   # High, Medium, Low
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    category = relationship('Category', backref = 'tasks')
    user = relationship('User', backref = 'assigned_tasks')


