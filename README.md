# Task Management System (CLI)
The Task Management System is a command-line interface (CLI) application that helps users efficiently organize, track, and manage their tasks. It allows users to add tasks, assign them to other users, categorize them, set priorities, and track completion status.

Built using Python, Click, and SQLAlchemy ORM, this project ensures persistent data storage and an interactive CLI experience.

## Table of Contents
- [Features](#features)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

### Features
1. Task Management – Create, update, delete, and list tasks.
2. User Management – Add users and assign tasks to them.
3. Category Organization – Group tasks into different categories.
4. Task Prioritization & Status – Set priority levels (High, Medium, Low) and mark tasks as completed.
5. Task Filtering – View tasks by priority, due date, category, or assigned user.
6. Persistent Data Storage – Uses SQLite with SQLAlchemy ORM.
7. Interactive CLI – User-friendly navigation powered by Click.

### Installation and Setup
1. Fork and Clone the repository:
    ```bash
    git clone https://github.com/amanda-odawa/task_manager.git
    ```
2. Navigate to the project directory:
    ```bash
    cd task_manager
    ```
3. Create a Virtual Environment
    ```bash
    python -m venv env
    ```
4. Navigate to virtual environment
    On Windows (Command Prompt):
    ```bash
    env\Scripts\activate
    ```
    On macOS/Linux:
    ```bash
    source env/bin/activate
    ```
5. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
6. Run migrations(Setup database)
    ```
    python -m alembic upgrade head
    ```

### Usage
To run the CLI, use:
 ```bash
python -m src.cli 
```
#### **Task Commands**
| Command                 | Description                                      |
|-------------------------|--------------------------------------------------|
| `add-task`             | Add a new task                                   |
| `list-tasks`           | View all tasks                                   |
| `update-task`          | Update an existing task                          |
| `delete-task`          | Delete a task                                    |
| `mark-task-completed`  | Mark a task as completed                         |
| `assign-task`          | Assign a task to a user                          |
| `filter-tasks`         | Filter tasks by priority, due date, or category  |

---

#### **User Commands**
| Command                 | Description                                      |
|-------------------------|--------------------------------------------------|
| `add-user`             | Add a new user                                   |
| `list-users`           | View all users                                   |
| `assign-task`          | Assign a task to a user                          |
| `show-user-assignments`| Display all tasks assigned to each user          |

---

#### **Category Commands**
| Command                | Description                                      |
|------------------------|--------------------------------------------------|
| `add-category`        | Add a new category                               |
| `list-categories`     | View all categories                             |

### Contributing
Want to contribute? Follow these steps:
1. Fork the repository
2. Create a new branch 
    ```bash
    git checkout -b Your-Feature-Name
    ```
3. Make your changes
4. Commit changes 
    ```bash
    git commit -m 'Added new feature'
    ```
5. Push to GitHub 
    ```bash
    git push origin Your-Feature-Name
    ```
6. Submit a Pull Request

### Lisense
This project is open-source and available under the MIT License.

