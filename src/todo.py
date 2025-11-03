#!/usr/bin/env python3
"""
A simple command-line todo list application that stores tasks in a JSON file.
"""

import argparse
import json
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

# Constants
TASKS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tasks.json")

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"

    def __str__(self):
        return self.value

class TodoList:
    def __init__(self, tasks_file: str = TASKS_FILE):
        self.tasks_file = tasks_file
        self.tasks: List[Dict] = self._load_tasks()

    def _load_tasks(self) -> List[Dict]:
        """Load tasks from JSON file."""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        return []

    def _save_tasks(self) -> None:
        """Save tasks to JSON file."""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def _get_task_by_id(self, task_id: int) -> Optional[Dict]:
        """Get a task by its ID."""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None

    def _update_task_metadata(self, task: Dict) -> None:
        """Update task modification timestamp."""
        task['modified_at'] = datetime.now().isoformat()

    def add_task(self, title: str, description: Optional[str] = None) -> Dict:
        """Add a new task to the list."""
        now = datetime.now().isoformat()
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'status': TaskStatus.PENDING.value,
            'created_at': now,
            'modified_at': now,
            'completed_at': None
        }
        self.tasks.append(task)
        self._save_tasks()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        task = self._get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self._save_tasks()
            return True
        return False

    def update_task(self, task_id: int, 
                    title: Optional[str] = None,
                    description: Optional[str] = None,
                    status: Optional[Union[str, TaskStatus]] = None) -> Optional[Dict]:
        """Update a task's attributes."""
        task = self._get_task_by_id(task_id)
        if not task:
            return None

        if title is not None:
            task['title'] = title
        if description is not None:
            task['description'] = description
        if status is not None:
            status_value = status.value if isinstance(status, TaskStatus) else status
            if status_value == TaskStatus.COMPLETED.value and task['status'] != TaskStatus.COMPLETED.value:
                task['completed_at'] = datetime.now().isoformat()
            task['status'] = status_value

        self._update_task_metadata(task)
        self._save_tasks()
        return task

    def list_tasks(self, status: Optional[str] = None, sort_by_status: bool = False) -> List[Dict]:
        """List all tasks, optionally filtered by status and sorted."""
        tasks = self.tasks.copy()  # Work with a copy to avoid modifying the original list
        if status:
            tasks = [task for task in tasks if task['status'] == status]
        
        if sort_by_status:
            # Sort by status (pending first, then in-progress, then completed)
            status_order = {
                TaskStatus.PENDING.value: 0,
                TaskStatus.IN_PROGRESS.value: 1,
                TaskStatus.COMPLETED.value: 2
            }
            tasks = sorted(tasks, key=lambda x: (status_order.get(x['status'], 999), x['created_at']))
        return tasks

def main():
    parser = argparse.ArgumentParser(description='Todo List CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('-d', '--description', help='Task description')

    # List tasks command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('-s', '--status', 
                            choices=[s.value for s in TaskStatus],
                            help='Filter tasks by status')
    list_parser.add_argument('--sort', action='store_true',
                            help='Sort tasks by status')

    # Delete task command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', type=int, help='ID of the task to delete')

    # Update task command
    update_parser = subparsers.add_parser('update', help='Update a task')
    update_parser.add_argument('task_id', type=int, help='ID of the task to update')
    update_parser.add_argument('-t', '--title', help='New task title')
    update_parser.add_argument('-d', '--description', help='New task description')
    update_parser.add_argument('-s', '--status', 
                             choices=[s.value for s in TaskStatus],
                             help='New task status')

    args = parser.parse_args()
    todo = TodoList()

    if args.command == 'add':
        task = todo.add_task(args.title, args.description)
        print(f"Added task {task['id']}: {task['title']}")
    
    elif args.command == 'list':
        tasks = todo.list_tasks(args.status, args.sort)
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

    elif args.command == 'delete':
        if todo.delete_task(args.task_id):
            print(f"Deleted task {args.task_id}")
        else:
            print(f"Task {args.task_id} not found")

    elif args.command == 'update':
        if not any([args.title, args.description, args.status]):
            print("Please specify at least one field to update (title, description, or status)")
            return

        task = todo.update_task(args.task_id, args.title, args.description, args.status)
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
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()