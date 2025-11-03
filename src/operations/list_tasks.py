"""List tasks operation."""

from typing import Optional, List, Dict
from datetime import datetime
from .base import BaseOperation
from ..todo_list import TodoList, TaskStatus

class ListTasksOperation(BaseOperation):
    """Operation to list tasks."""

    def execute(self, status: Optional[str] = None, sort_by_status: bool = False) -> List[Dict]:
        """Execute the list tasks operation."""
        return self.todo_list.list_tasks(status, sort_by_status)

    def add_parser(self, subparsers) -> None:
        """Add the parser for this operation."""
        parser = subparsers.add_parser('list', help='List tasks')
        parser.add_argument('-s', '--status',
                          choices=[s.value for s in TaskStatus],
                          help='Filter tasks by status')
        parser.add_argument('--sort', action='store_true',
                          help='Sort tasks by status')

    def handle_args(self, args) -> None:
        """Handle the parsed arguments."""
        tasks = self.execute(args.status, args.sort)
        if not tasks:
            print("No tasks found.")
            return

        print("\nTasks:")
        print("-" * 60)
        for task in tasks:
            status = f"[{task['status']}]"
            created = datetime.fromisoformat(task['created_at']).strftime('%Y-%m-%d %H:%M')
            print(f"{task['id']:3d}. {status:12} {task['title']} (Created: {created})")
            if task['description']:
                print(f"     Description: {task['description']}")
            if task['modified_at'] != task['created_at']:
                modified = datetime.fromisoformat(task['modified_at']).strftime('%Y-%m-%d %H:%M')
                print(f"     Last modified: {modified}")
        print("-" * 60)