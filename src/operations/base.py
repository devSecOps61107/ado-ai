"""Base operation class for todo list operations."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..todo_list import TodoList

class BaseOperation(ABC):
    """Base class for all todo operations."""
    
    def __init__(self, todo_list: TodoList):
        self.todo_list = todo_list

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the operation with the given arguments."""
        pass

    @abstractmethod
    def add_parser(self, subparsers) -> None:
        """Add this operation's parser to the subparsers."""
        pass

    @abstractmethod
    def handle_args(self, args) -> None:
        """Handle the parsed arguments for this operation."""
        pass