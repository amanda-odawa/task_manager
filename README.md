How to Use It
Run the CLI:
python src.cli.py
Add a Task:
python cli.py add-task
(It will prompt for name, due date, priority, category, and user ID)
List All Tasks:
python cli.py list-tasks

🔹 Setup Before Testing
1️⃣ Ensure Virtual Environment is Active
source env/bin/activate  

2️⃣ Ensure Database is Up to Date
alembic upgrade head

3️⃣ Run the CLI
python -m src.cli

🔹 Testing Categories
✅ Add a Category
python -m src.cli add-category
  
✅ List All Categories
python -m src.cli list-categories

🔹 Testing Users
✅ Add a User
python -m src.cli add-user
  
✅ List All Users
python -m src.cli list-users

✅ Assign a task to a user (user's name and task id)
python -m src.cli assign-task
    
✅ Show User Assignments
python -m src.cli show-user-assignments

🔹 Testing Tasks
✅ Add a task
python -m src.cli add-task

✅ Update a Task
python -m src.cli update-task

✅ Delete a Task
python -m src.cli delete-task
    
✅ List All Tasks
python -m src.cli list-tasks

✅ Mark Task as Completed
python -m src.cli mark-task-completed

🔹 Filtering Tasks
✅ Filter by Priority
python -m src.cli filter-tasks