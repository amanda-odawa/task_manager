from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database connection
engine = create_engine('sqlite:///task_manager.db')

# Create session
SessionLocal = sessionmaker(bind = engine)


