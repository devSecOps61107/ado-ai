# Python Todo CLI

A simple command-line todo list application built with Python. This application allows you to manage your tasks through a CLI interface, storing them in a JSON file for persistence.

## Features

- Add new tasks with titles and optional descriptions
- List all tasks
- Filter tasks by status (pending/completed)
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

### List tasks by status
```bash
python src/todo.py list -s pending
python src/todo.py list -s completed
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

- Mark tasks as completed
- Delete tasks
- Edit existing tasks
- Due dates for tasks
- Task priorities
- Unit tests
- Task categories/tags