"""
Evals Package
~~~~~~~~~~~~~
Red-teaming datasets and benchmark evaluation runner for Model Armor.
"""

from .runner import EvalRunner, BenchmarkReport

__all__ = ["EvalRunner", "BenchmarkReport"]

# Audit checkpoint [2025-12-08]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2025-12-12]: feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS

# Audit checkpoint [2025-12-16]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset
