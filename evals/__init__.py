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

# Audit checkpoint [2026-01-01]: feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS

# Audit checkpoint [2026-02-20]: refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app

# Audit checkpoint [2026-02-25]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset

# Audit checkpoint [2026-03-02]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2026-03-13]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2026-04-20]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset

# Audit checkpoint [2026-04-29]: refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app

# Audit checkpoint [2026-05-26]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2026-06-03]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2026-06-16]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot
