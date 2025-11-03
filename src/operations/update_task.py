"""Update task operation."""

from typing import Optional, Dict
from datetime import datetime
from .base import BaseOperation
from ..todo_list import TodoList, TaskStatus

class UpdateTaskOperation(BaseOperation):
    """Operation to update a task."""

    def execute(self, task_id: int, title: Optional[str] = None,
               description: Optional[str] = None, status: Optional[str] = None) -> Optional[Dict]:
        """Execute the update task operation."""
        return self.todo_list.update_task(task_id, title, description, status)

    def add_parser(self, subparsers) -> None:
        """Add the parser for this operation."""
        parser = subparsers.add_parser('update', help='Update a task')
        parser.add_argument('task_id', type=int, help='ID of the task to update')
        parser.add_argument('-t', '--title', help='New task title')
        parser.add_argument('-d', '--description', help='New task description')
        parser.add_argument('-s', '--status',
                          choices=[s.value for s in TaskStatus],
                          help='New task status')

    def handle_args(self, args) -> None:
        """Handle the parsed arguments."""
        if not any([args.title, args.description, args.status]):
            print("Please specify at least one field to update (title, description, or status)")
            return

        task = self.execute(args.task_id, args.title, args.description, args.status)
        if task:
            print(f"Updated task {task['id']}:")
            print(f"  Title: {task['title']}")
            print(f"  Status: {task['status']}")
            if task['description']:
                print(f"  Description: {task['description']}")
            modified = datetime.fromisoformat(task['modified_at']).strftime('%Y-%m-%d %H:%M')
            print(f"  Last modified: {modified}")
        else:
            print(f"Task {args.task_id} not found")