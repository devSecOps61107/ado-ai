"""
Test configuration and fixtures for the todo application.
"""

import json
import os
import pytest
from datetime import datetime
from src.todo import TodoList, TaskStatus

@pytest.fixture
def temp_tasks_file(tmp_path):
    """Create a temporary tasks file for testing."""
    tasks_file = tmp_path / "test_tasks.json"
    with open(tasks_file, 'w') as f:
        json.dump([], f)
    return str(tasks_file)

@pytest.fixture
def todo_list(temp_tasks_file):
    """Create a TodoList instance with a temporary file."""
    return TodoList(temp_tasks_file)

@pytest.fixture
def populated_todo_list(todo_list):
    """Create a TodoList instance with some sample tasks."""
    tasks = [
        ("Task 1", "Description 1"),
        ("Task 2", "Description 2"),
        ("Task 3", "Description 3"),
    ]
    for title, desc in tasks:
        todo_list.add_task(title, desc)
    return todo_list