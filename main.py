from database import engine
from models import Base

# Create tables
Base.metadata.create_all(engine)
print("Task Manager Initialized!")
