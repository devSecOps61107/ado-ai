#!/usr/bin/env python3
"""
A simple command-line todo list application that stores tasks in a JSON file.
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Constants
TASKS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tasks.json")

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

    def add_task(self, title: str, description: Optional[str] = None) -> Dict:
        """Add a new task to the list."""
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        self.tasks.append(task)
        self._save_tasks()
        return task

    def list_tasks(self, status: Optional[str] = None) -> List[Dict]:
        """List all tasks, optionally filtered by status."""
        if status:
            return [task for task in self.tasks if task['status'] == status]
        return self.tasks

def main():
    parser = argparse.ArgumentParser(description='Todo List CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('-d', '--description', help='Task description')

    # List tasks command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('-s', '--status', choices=['pending', 'completed'],
                            help='Filter tasks by status')

    args = parser.parse_args()
    todo = TodoList()

    if args.command == 'add':
        task = todo.add_task(args.title, args.description)
        print(f"Added task {task['id']}: {task['title']}")
    
    elif args.command == 'list':
        tasks = todo.list_tasks(args.status)
        if not tasks:
            print("No tasks found.")
            return

        print("\nTasks:")
        print("-" * 40)
        for task in tasks:
            status = f"[{task['status']}]"
            print(f"{task['id']:3d}. {status:10} {task['title']}")
            if task['description']:
                print(f"     {task['description']}")
        print("-" * 40)
    
    else:
        parser.print_help()

if __name__ == '__main__':
    main()