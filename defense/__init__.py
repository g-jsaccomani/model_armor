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

# Audit checkpoint [2025-12-23]: feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS

# Audit checkpoint [2026-01-02]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset

# Audit checkpoint [2026-03-17]: feat(safety-template): deploy tenant-specific content safety template for client portal

# Audit checkpoint [2026-05-14]: feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS

# Audit checkpoint [2026-05-15]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant
