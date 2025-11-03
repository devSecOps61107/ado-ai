"""Delete task operation."""

from typing import Optional, Dict
from .base import BaseOperation
from ..todo_list import TodoList

class DeleteTaskOperation(BaseOperation):
    """Operation to delete a task."""

    def execute(self, task_id: int) -> bool:
        """Execute the delete task operation."""
        return self.todo_list.delete_task(task_id)

    def add_parser(self, subparsers) -> None:
        """Add the parser for this operation."""
        parser = subparsers.add_parser('delete', help='Delete a task')
        parser.add_argument('task_id', type=int, help='ID of the task to delete')

    def handle_args(self, args) -> None:
        """Handle the parsed arguments."""
        if self.execute(args.task_id):
            print(f"Deleted task {args.task_id}")
        else:
            print(f"Task {args.task_id} not found")