from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base

# Database connection
engine = create_engine('sqlite:///task_manager.db')

# Create session
SessionLocal = sessionmaker(bind = engine)

# Create tables
Base.metadata.create_all(engine)
print("Task Manager Initialized!")
