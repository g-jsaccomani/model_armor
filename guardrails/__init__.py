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
