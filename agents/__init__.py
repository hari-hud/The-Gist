"""
The-Gist Agents Module

This module contains the AI agents that power the book summary to audio workflow:
- ResearchAgent: Gathers book information and key themes
- SummarizerAgent: Generates compelling book summaries
- NarratorAgent: Converts text to professional audio
- OrchestratorAgent: Coordinates the entire workflow
"""

from .research_agent import ResearchAgent
from .summarizer_agent import SummarizerAgent
from .narrator_agent import NarratorAgent
from .orchestrator import OrchestratorAgent

__all__ = [
    "ResearchAgent",
    "SummarizerAgent", 
    "NarratorAgent",
    "OrchestratorAgent",
]

