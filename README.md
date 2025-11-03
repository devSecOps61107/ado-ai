# Python Todo CLI

A simple command-line todo list application built with Python. This application allows you to manage your tasks through a CLI interface, storing them in a JSON file for persistence.

## Features

- Add new tasks with titles and optional descriptions
- List all tasks with creation and modification timestamps
- Filter and sort tasks by status (pending/in-progress/completed)
- Update task title, description, and status
- Delete tasks by ID
- Task metadata tracking (created, modified, completed timestamps)
- Data persistence using JSON storage
- Command-line interface using argparse

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/devSecOps61107/ado-ai.git
   cd ado-ai
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The application provides the following commands:

### Add a new task
```bash
python src/todo.py add "Task title" -d "Optional task description"
```

### List all tasks
```bash
python src/todo.py list
```

### List tasks with optional filtering and sorting
```bash
python src/todo.py list                    # List all tasks
python src/todo.py list -s pending         # Filter by status
python src/todo.py list -s in-progress     # Show in-progress tasks
python src/todo.py list -s completed       # Show completed tasks
python src/todo.py list --sort             # Sort by status
```

### Update a task
```bash
python src/todo.py update 1 -t "New title"           # Update title
python src/todo.py update 1 -d "New description"     # Update description
python src/todo.py update 1 -s "completed"           # Update status
```

### Delete a task
```bash
python src/todo.py delete 1                # Delete task with ID 1
```

## Project Structure

```
ado-ai/
├── src/
│   └── todo.py      # Main application code
├── tasks.json       # Task storage file
├── requirements.txt # Project dependencies
└── README.md       # Project documentation
```

## Development

To contribute to the project:

1. Create a new branch for your feature
2. Make your changes
3. Run the tests (when implemented)
4. Submit a pull request

## Future Enhancements

- Add due dates for tasks
- Add task priorities
- Add task categories/tags
- Add task search functionality
- Add batch operations
- Add task export/import
- Add unit tests
- Add task reminders