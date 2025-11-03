"""Add task operation."""

from typing import Optional, Dict
from .base import BaseOperation
from ..todo_list import TodoList

class AddTaskOperation(BaseOperation):
    """Operation to add a new task."""

    def execute(self, title: str, description: Optional[str] = None) -> Dict:
        """Execute the add task operation."""
        return self.todo_list.add_task(title, description)

    def add_parser(self, subparsers) -> None:
        """Add the parser for this operation."""
        parser = subparsers.add_parser('add', help='Add a new task')
        parser.add_argument('title', help='Task title')
        parser.add_argument('-d', '--description', help='Task description')

    def handle_args(self, args) -> None:
        """Handle the parsed arguments."""
        task = self.execute(args.title, args.description)
        print(f"Added task {task['id']}: {task['title']}")