"""
Tests for the todo list application's core functionality.
"""

import pytest
from datetime import datetime
from src.todo import TodoList, TaskStatus

def test_add_task(todo_list):
    """Test adding a new task."""
    task = todo_list.add_task("Test Task", "Test Description")
    
    assert task['id'] == 1
    assert task['title'] == "Test Task"
    assert task['description'] == "Test Description"
    assert task['status'] == TaskStatus.PENDING.value
    assert 'created_at' in task
    assert 'modified_at' in task
    assert task['completed_at'] is None

def test_add_task_without_description(todo_list):
    """Test adding a task without a description."""
    task = todo_list.add_task("Test Task")
    
    assert task['description'] is None
    assert task['title'] == "Test Task"

def test_list_tasks(populated_todo_list):
    """Test listing all tasks."""
    tasks = populated_todo_list.list_tasks()
    
    assert len(tasks) == 3
    assert all(isinstance(task['id'], int) for task in tasks)
    assert all(task['status'] == TaskStatus.PENDING.value for task in tasks)

def test_list_tasks_by_status(populated_todo_list):
    """Test listing tasks filtered by status."""
    # Update one task to completed
    populated_todo_list.update_task(1, status=TaskStatus.COMPLETED.value)
    
    pending_tasks = populated_todo_list.list_tasks(TaskStatus.PENDING.value)
    completed_tasks = populated_todo_list.list_tasks(TaskStatus.COMPLETED.value)
    
    assert len(pending_tasks) == 2
    assert len(completed_tasks) == 1
    assert completed_tasks[0]['id'] == 1

def test_list_tasks_sorted(populated_todo_list):
    """Test listing tasks with sorting by status."""
    # Set different statuses
    populated_todo_list.update_task(1, status=TaskStatus.COMPLETED.value)
    populated_todo_list.update_task(2, status=TaskStatus.IN_PROGRESS.value)
    
    sorted_tasks = populated_todo_list.list_tasks(sort_by_status=True)
    
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0]['status'] == TaskStatus.PENDING.value
    assert sorted_tasks[1]['status'] == TaskStatus.IN_PROGRESS.value
    assert sorted_tasks[2]['status'] == TaskStatus.COMPLETED.value

def test_delete_task(populated_todo_list):
    """Test deleting a task."""
    initial_count = len(populated_todo_list.tasks)
    success = populated_todo_list.delete_task(1)
    
    assert success is True
    assert len(populated_todo_list.tasks) == initial_count - 1
    assert all(task['id'] != 1 for task in populated_todo_list.tasks)

def test_delete_nonexistent_task(populated_todo_list):
    """Test attempting to delete a non-existent task."""
    initial_count = len(populated_todo_list.tasks)
    success = populated_todo_list.delete_task(999)
    
    assert success is False
    assert len(populated_todo_list.tasks) == initial_count

def test_update_task_title(populated_todo_list):
    """Test updating a task's title."""
    task = populated_todo_list.update_task(1, title="Updated Title")
    
    assert task is not None
    assert task['title'] == "Updated Title"
    assert task['modified_at'] != task['created_at']

def test_update_task_description(populated_todo_list):
    """Test updating a task's description."""
    task = populated_todo_list.update_task(1, description="Updated Description")
    
    assert task is not None
    assert task['description'] == "Updated Description"
    assert task['modified_at'] != task['created_at']

def test_update_task_status(populated_todo_list):
    """Test updating a task's status."""
    task = populated_todo_list.update_task(1, status=TaskStatus.COMPLETED)
    
    assert task is not None
    assert task['status'] == TaskStatus.COMPLETED.value
    assert task['completed_at'] is not None
    assert task['modified_at'] != task['created_at']

def test_update_nonexistent_task(populated_todo_list):
    """Test attempting to update a non-existent task."""
    task = populated_todo_list.update_task(999, title="Updated Title")
    
    assert task is None

def test_task_timestamps(todo_list):
    """Test that task timestamps are properly managed."""
    # Add a task
    task = todo_list.add_task("Test Task")
    created_at = task['created_at']
    modified_at = task['modified_at']
    
    assert created_at == modified_at
    assert task['completed_at'] is None
    
    # Update the task
    import time
    time.sleep(0.001)  # Ensure timestamp will be different
    task = todo_list.update_task(task['id'], description="Updated")
    
    assert task['created_at'] == created_at
    assert task['modified_at'] != created_at
    
    # Complete the task
    task = todo_list.update_task(task['id'], status=TaskStatus.COMPLETED)
    
    assert task['completed_at'] is not None
    assert task['modified_at'] != created_at