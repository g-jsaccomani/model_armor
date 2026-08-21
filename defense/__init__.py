"""
Defense Package
~~~~~~~~~~~~~~~
Defense-in-depth components for AI agents: Canary tokens, Heuristics, and Tool Firewalls.
"""

from .canary import CanaryManager, SystemPromptCanary
from .heuristic_filter import HeuristicFilter
from .tool_firewall import ToolFirewall, ToolExecutionPolicy

__all__ = [
    "CanaryManager",
    "SystemPromptCanary",
    "HeuristicFilter",
    "ToolFirewall",
    "ToolExecutionPolicy",
]
