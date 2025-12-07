"""
Base Agent class for The-Gist workflow.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

from rich.console import Console
from rich.panel import Panel

console = Console()


@dataclass
class AgentResult:
    """Result from an agent execution."""
    success: bool
    data: Any
    agent_name: str
    execution_time: float = 0.0
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.timestamp = datetime.now().isoformat()


class BaseAgent(ABC):
    """Abstract base class for all agents in the workflow."""
    
    def __init__(self, name: str, verbose: bool = True):
        self.name = name
        self.verbose = verbose
        self.logger = logging.getLogger(f"the-gist.{name}")
        
    def log(self, message: str, style: str = "cyan"):
        """Log a message with rich formatting."""
        if self.verbose:
            console.print(f"[{style}]🤖 [{self.name}][/{style}] {message}")
    
    def log_success(self, message: str):
        """Log a success message."""
        self.log(f"✅ {message}", style="green")
        
    def log_error(self, message: str):
        """Log an error message."""
        self.log(f"❌ {message}", style="red")
        
    def log_thinking(self, message: str):
        """Log a thinking/processing message."""
        self.log(f"💭 {message}", style="yellow")
    
    def show_panel(self, content: str, title: str):
        """Display content in a rich panel."""
        if self.verbose:
            console.print(Panel(content, title=f"[bold]{title}[/bold]", border_style="blue"))
    
    @abstractmethod
    async def execute(self, **kwargs) -> AgentResult:
        """Execute the agent's task. Must be implemented by subclasses."""
        ...
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name='{self.name}')>"

