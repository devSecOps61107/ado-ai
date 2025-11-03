"""Complete task operation."""

from typing import Optional, Dict
from datetime import datetime
from .base import BaseOperation
from ..todo_list import TodoList

class CompleteTaskOperation(BaseOperation):
    """Operation to mark a task as complete."""

    def execute(self, task_id: int) -> Optional[Dict]:
        """Execute the complete task operation."""
        return self.todo_list.mark_complete(task_id)

    def add_parser(self, subparsers) -> None:
        """Add the parser for this operation."""
        parser = subparsers.add_parser('complete', help='Mark a task as complete')
        parser.add_argument('task_id', type=int, help='ID of the task to mark as complete')

    def handle_args(self, args) -> None:
        """Handle the parsed arguments."""
        task = self.execute(args.task_id)
        if task:
            print(f"Marked task {task['id']} as complete:")
            print(f"  Title: {task['title']}")
            completed = datetime.fromisoformat(task['completed_at']).strftime('%Y-%m-%d %H:%M')
            print(f"  Completed at: {completed}")
        else:
            print(f"Task {args.task_id} not found")