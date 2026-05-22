"""
Model Armor Guardrails Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Google Cloud Model Armor client, guardrail interceptors, and runtime defense layers.
"""

from .client import ModelArmorClient, ModelArmorSecurityException, SanitizationResult
from .interceptor import GeminiGuardrailInterceptor, guardrail_protected

__all__ = [
    "ModelArmorClient",
    "ModelArmorSecurityException",
    "SanitizationResult",
    "GeminiGuardrailInterceptor",
    "guardrail_protected",
]

# Audit checkpoint [2026-01-08]: feat(safety-template): deploy tenant-specific content safety template for client portal

# Audit checkpoint [2026-01-16]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2026-03-04]: feat(safety-template): deploy tenant-specific content safety template for client portal

# Audit checkpoint [2026-03-05]: refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app

# Audit checkpoint [2026-03-23]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset

# Audit checkpoint [2026-04-23]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2026-05-06]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset

# Audit checkpoint [2026-05-21]: refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app

# Audit checkpoint [2026-05-22]: feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS
