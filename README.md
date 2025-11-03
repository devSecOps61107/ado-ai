# Python Todo CLI

A simple command-line todo list application built with Python. This application allows you to manage your tasks through a CLI interface, storing them in a JSON file for persistence.

## Features

### Task Management
- Add new tasks with titles and optional descriptions
- List all tasks with creation and modification timestamps
- Filter and sort tasks by status (pending/in-progress/completed)
- Update task title, description, and status
- Delete tasks by ID
- Mark tasks as complete

### Technical Features
- Modular, maintainable code structure
- Task metadata tracking (created, modified, completed timestamps)
- Data persistence using JSON storage
- Command-line interface using argparse
- Extensible operation-based architecture

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

### Mark a task as complete
```bash
python src/todo.py complete 1              # Mark task with ID 1 as complete
```

## Project Structure

```
ado-ai/
├── src/
│   ├── operations/                  # Command operations
│   │   ├── __init__.py             # Operation exports
│   │   ├── base.py                 # Base operation class
│   │   ├── add_task.py            # Add task operation
│   │   ├── list_tasks.py          # List tasks operation
│   │   ├── update_task.py         # Update task operation
│   │   ├── delete_task.py         # Delete task operation
│   │   └── complete_task.py       # Complete task operation
│   ├── todo_list.py               # Core TodoList class
│   └── todo.py                    # CLI entry point
├── tasks.json                     # Task storage file
├── requirements.txt               # Project dependencies
└── README.md                     # Project documentation
```

### Code Organization

The project follows a modular structure:

- `todo_list.py`: Core functionality for task management
- `operations/`: Individual command implementations
  - `base.py`: Abstract base class for operations
  - Each operation is in its own file for better maintainability
- `todo.py`: Main CLI entry point and command routing

## Development

To contribute to the project:

1. Create a new branch for your feature
2. Make your changes
3. Run the tests:
   ```bash
   pytest tests/
   ```
4. Submit a pull request

## Testing

The project uses pytest for testing. Tests are located in the `tests/` directory and cover core functionality including:
- Task creation
- Task updates
- Task deletion
- Task completion
- Task listing and filtering

To run the tests:
```bash
pytest tests/
```

## Future Enhancements

- Add due dates for tasks
- Add task priorities
- Add task categories/tags
- Add task search functionality
- Add batch operations
- Add task export/import
- Add unit tests
- Add task reminders