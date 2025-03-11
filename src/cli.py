from sqlalchemy.orm import sessionmaker
from src.main import engine
import click
from src.models import Task, Category, User
from datetime import datetime

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
@click.option('--name', prompt = 'Category name')
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
            click.echo(f'Id: {category.id} | Name: {category.name}')

    session.close()

# --------------------------------------------------
                # USER COMMANDS
# --------------------------------------------------

# Add new user
@cli.command()
@click.option('--name', prompt = 'User name')
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
            click.echo(f'Id: {user.id} | Name: {user.name}')

    session.close()

# Assign task to user
@cli.command()
@click.option('--user', prompt = 'User name')
@click.option('--task_id', prompt = 'Task Id', type = int)
def assign_task(user, task_id):
    session = SessionLocal()
    user_obj = session.query(User).filter(User.name == user).first()
    task_obj = session.query(Task).filter(Task.id == task_id).first()

    if not user_obj:
        click.echo(f'Error: User "{user}" not found.')
    elif not task_obj:
        click.echo(f'Error: Task Id {task_id} not found.')
    else:
        task_obj.user_id = user_obj.id
        session.commit()
        click.echo(f'Assigned task {task_obj.name}(Id: {task_id}) to {user_obj.name}.')
    
    session.close()

# Show user assignments
@cli.command()
def show_user_assignments():
    session = SessionLocal()
    users = session.query(User).all()

    if not users:
        click.echo('No users found.')
    else:
        click.echo('User assignments:')
        for user in users:
            click.echo(f'User: {user.name}')
            assigned_tasks = user.assigned_tasks

            if assigned_tasks:
                for task in assigned_tasks:
                    click.echo(f'  Task: {task.name} | Id: {task.id} | Due: {task.due_date.strftime("%Y-%m-%d")} | Priority: {task.priority} | Status: {task.status}')
            else:
                click.echo('No tasks assigned.')

    session.close()

# --------------------------------------------------
                # TASK COMMANDS
# --------------------------------------------------

# Add new task
@cli.command()
@click.option('--name', prompt = 'Task name')
@click.option('--due_date', prompt = 'Due date (YYYY-MM-DD)')
@click.option('--priority', prompt = 'Priority (High, Medium, Low)')
@click.option('--category', prompt = 'Category name')
def add_task(name, due_date, priority, category):
    session = SessionLocal()

    try:
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    except ValueError:
        click.echo('Invalid date format. Please use YYYY-MM-DD.')
        session.close()
        return
    
    category_obj = session.query(Category).filter(Category.name == category).first()
    if not category_obj:
        click.echo(f'Error: Category "{category}" not found.')
        session.close()
        return
    
    task = Task(name = name, due_date = due_date, priority = priority, category_id = category_obj.id)
    session.add(task)
    session.commit()
    click.echo(f'Added task: {task.name} | Id: {task.id}')
    session.close()

# Delete a task
@cli.command()
@click.option('--task_id', prompt='Task Id to delete', type = int)
def delete_task(task_id):
    session = SessionLocal()
    task = session.query(Task).filter(Task.id == task_id).first()

    if not task:
        click.echo('Task not found.')
    else:
        session.delete(task)
        session.commit()
        click.echo(f'Deleted task Id {task_id}, "{task.name}".')

    session.close()

# Update a task
@cli.command()
@click.option('--task_id', prompt='Task Id to update', type=int)
@click.option('--name', prompt='New task name (Leave blank to keep unchanged)', default = '', required = False)
@click.option('--priority', prompt='New priority (High, Medium, Low) (Leave blank to keep unchanged)', default = '', required = False)
@click.option('--due_date', prompt='New due date (YYYY-MM-DD) (Leave blank to keep unchanged)', default = '', required = False)
@click.option('--category_id', prompt='New category Id (Leave blank to keep unchanged)', default = None, type = int, required = False)
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
    click.echo(f'Task Id {task_id}, {task.name} updated.')
    session.close()

# List all tasks
@cli.command()
def list_tasks():
    session = SessionLocal()
    tasks = session.query(Task).all()

    if not tasks:
        click.echo('No tasks found.')
    else:
        click.echo('Tasks:')
        for task in tasks:
            click.echo(f'Id: {task.id} | Name: {task.name} | Category {task.category_id} | Status: {task.status}')

    session.close()

# Mark task as completed
@cli.command()
@click.option('--task_id', prompt = 'Task Id to mark as completed', type = int)
def mark_task_completed(task_id):
    session = SessionLocal()
    task = session.query(Task).filter(Task.id == task_id).first()

    if not task:
        click.echo('Task not found.')
    else:
        task.status = 'Completed'
        session.commit()
        click.echo(f'Task Id {task_id}, "{task.name}" marked as Completed.')

    session.close()

# Filter tasks by priority, due date, or category
@cli.command()
@click.option('--filter_by', type=click.Choice(['priority', 'due_date', 'category']),prompt = "Choose filter")
def filter_tasks(filter_by):
    session = SessionLocal()
    
    if filter_by == 'priority':
        value = click.prompt("Choose priority", type = click.Choice(['Low', 'Medium', 'High']))
    elif filter_by == 'due_date':
        value = click.prompt("Enter due date (YYYY-MM-DD)")
    elif filter_by == 'category':
        categories = session.query(Category.name).all()
        category_names = [cat[0] for cat in categories] if categories else []
        if category_names:
            value = click.prompt("Choose category", type = click.Choice(category_names))
        else:
            click.echo("No categories found.")
            session.close()
            return

    filters = {
        'priority': Task.priority == value,
        'due_date': Task.due_date == value,
        'category': Category.name == value
    }

    query = session.query(Task)
    if filter_by == 'category':
        query = query.join(Category)

    tasks = query.filter(filters[filter_by]).all()
    if tasks:
        click.echo('-' * 40)
        for task in tasks:
            click.echo(f'Task Id: {task.id}')
            click.echo(f'Task: {task.name}')
            click.echo(f'Due: {task.due_date.strftime("%Y-%m-%d")}')
            click.echo(f'Priority: {task.priority}')
            click.echo(f'Status: {task.status}')
            click.echo('-' * 40)
    else:
        click.echo("No tasks found.")

    session.close()

if __name__ == '__main__':
    cli()