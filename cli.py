from sqlalchemy.orm import sessionmaker
from database import engine
import click
from models import Task, Category, User

SessionLocal = sessionmaker(bind = engine)

@click.group()
def cli():
    '''CLI for Task Manager'''
    pass

# --------------------------------------------------
                # CATEGORY COMMANDS
# --------------------------------------------------

# Add new category
@cli.command()
@click.option('--name', prompt = 'Category Name')
def add_category(name):
    session = SessionLocal()
    category = Category(name = name)
    session.add(category)
    session.commit()
    click.echo(f'Added category: {category.name}')
    session.close()

# List all categories
@cli.command()
def list_categories():
    session = SessionLocal()
    categories = session.query(Category).all()
    if not categories:
        click.echo('No categories found.')
    else:
        click.echo('Categories:')
        for category in categories:
            click.echo(f'ID: {category.id}, Name: {category.name}')
    session.close()

# --------------------------------------------------
                # USER COMMANDS
# --------------------------------------------------

# Add new user
@cli.command()
@click.option('--name', prompt='User Name')
def add_user(name):
    session = SessionLocal()
    user = User(name = name)
    session.add(user)
    session.commit()
    click.echo(f'Added user: {user.name}')
    session.close()

# List all users
@cli.command()
def list_users():
    session = SessionLocal()
    users = session.query(User).all()
    if not users:
        click.echo('No users found.')
    else:
        click.echo('Users:')
        for user in users:
            click.echo(f'ID: {user.id}, Name: {user.name}')
    session.close()

# Assign task to user
@cli.command()
@click.option('--user_id', prompt='User ID', type=int)
@click.option('--task_id', prompt='Task ID', type=int)
def assign_task(user_id, task_id):
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    task = session.query(Task).filter(Task.id == task_id).first()

    if not user:
        click.echo(f'User ID {user_id} not found.')
    elif not task:
        click.echo(f'Task ID {task_id} not found.')
    else:
        task.user_id = user_id
        session.commit()
        click.echo(f'Assigned Task ID {task_id} to User {user.name}.')
    session.close()

# Show user assignments
@cli.command()
def show_user_assignments():
    session = SessionLocal()
    user_tasks = {}

    users = session.query(User).all()
    for user in users:
        user_tasks[user.name] = [(task.id, task.name, task.priority) for task in user.assigned_tasks]

    session.close()

    click.echo('User assignments:')
    for user, tasks in user_tasks.items():
        click.echo(f'{user}: {tasks}')

# --------------------------------------------------
                # TASK COMMANDS
# --------------------------------------------------

# Add new task
@cli.command()
@click.option('--name', prompt='Task Name')
@click.option('--due_date', prompt='Due Date (YYYY-MM-DD)')
@click.option('--priority', prompt='Priority (High, Medium, Low)')
@click.option('--category_id', prompt='Category ID', type = int)
@click.option('--user_id', prompt='User ID', type = int)
def add_task(name, due_date, priority, category_id, user_id):
    session = SessionLocal()
    task = Task(name = name, due_date = due_date, priority = priority, category_id = category_id, user_id = user_id)
    session.add(task)
    session.commit()
    click.echo(f'Added task: {task.name} (Priority: {task.priority})')
    session.close()

# Delete a task
@cli.command()
@click.option('--task_id', prompt='Task ID to delete', type = int)
def delete_task(task_id):
    session = SessionLocal()
    task = session.query(Task).filter(Task.id == task_id).first()
    if not task:
        click.echo('Task not found.')
    else:
        session.delete(task)
        session.commit()
        click.echo(f'Deleted Task ID: {task_id}')
    session.close()

# Update a task
@cli.command()
@click.option('--task_id', prompt='Task ID to update', type=int)
@click.option('--name', prompt='New Task Name (Leave blank to keep unchanged)', default='', required=False)
@click.option('--priority', prompt='New Priority (High, Medium, Low) (Leave blank to keep unchanged)', default='', required=False)
@click.option('--due_date', prompt='New Due Date (YYYY-MM-DD) (Leave blank to keep unchanged)', default='', required=False)
@click.option('--category_id', prompt='New Category ID (Leave blank to keep unchanged)', default=None, type=int, required=False)
def update_task(task_id, name, priority, due_date, category_id):
    session = SessionLocal()
    task = session.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        click.echo('Task not found.')
        session.close()
        return

    if name:
        task.name = name
    if priority:
        task.priority = priority
    if due_date:
        task.due_date = due_date
    if category_id:
        task.category_id = category_id

    session.commit()
    click.echo(f'Task ID {task_id} updated.')
    session.close()

# List all tasks
@cli.command()
def list_tasks():
    session = SessionLocal()
    tasks = session.query(Task).all()
    for task in tasks:
        click.echo(f'ID: {task.id}, Name: {task.name}')
    session.close()

# Mark task as completed
@cli.command()
@click.option('--task_id', prompt='Task ID to mark as completed', type = int)
def mark_task_completed(task_id):
    session = SessionLocal()
    task = session.query(Task).filter(Task.id == task_id).first()
    if not task:
        click.echo('Task not found.')
    else:
        task.status = 'Completed'
        session.commit()
        click.echo(f'Task ID {task_id} marked as Completed.')
    session.close()

# Filter tasks by priority, due date or category
@cli.command()
@click.option('--filter_by', type = click.Choice(['priority', 'due_date', 'category']), prompt='Filter by (priority/due_date/category)')
@click.option('--value', prompt='Filter value')
def filter_tasks(filter_by, value):
    session = SessionLocal()

    if filter_by == 'priority':
        tasks = session.query(Task).filter(Task.priority == value).all()
    elif filter_by == 'due_date':
        tasks = session.query(Task).filter(Task.due_date == value).all()
    elif filter_by == 'category':
        tasks = session.query(Task).join(Category).filter(Category.name == value).all()
    
    if not tasks:
        click.echo('No tasks found.')
    else:
        for task in tasks:
            click.echo(f'ID: {task.id}, Name: {task.name}, Priority: {task.priority}, Due: {task.due_date}, Status: {task.status}')
    
    session.close()

if __name__ == '__main__':
    cli()