"""Core TodoList class implementation."""

import json
import os
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

class TaskStatus(Enum):
    """Enumeration of possible task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    BACKLOG = "backlog"

    def __str__(self):
        return self.value

class TodoList:
    """Main TodoList class for managing tasks."""

    def __init__(self, tasks_file: str):
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

    def list_tasks(self, status: Optional[str] = None, sort_by_status: bool = False) -> List[Dict]:
        """List all tasks, optionally filtered by status and sorted."""
        tasks = self.tasks.copy()
        if status:
            tasks = [task for task in tasks if task['status'] == status]
        
        if sort_by_status:
            status_order = {
                TaskStatus.PENDING.value: 0,
                TaskStatus.IN_PROGRESS.value: 1,
                TaskStatus.COMPLETED.value: 2
            }
            tasks = sorted(tasks, key=lambda x: (status_order.get(x['status'], 999), x['created_at']))
        return tasks

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

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        task = self._get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self._save_tasks()
            return True
        return False

    def mark_complete(self, task_id: int) -> Optional[Dict]:
        """Mark a task as complete."""
        return self.update_task(task_id, status=TaskStatus.COMPLETED)