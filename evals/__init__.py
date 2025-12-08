"""
Evals Package
~~~~~~~~~~~~~
Red-teaming datasets and benchmark evaluation runner for Model Armor.
"""

from .runner import EvalRunner, BenchmarkReport

__all__ = ["EvalRunner", "BenchmarkReport"]

# Audit checkpoint [2025-12-08]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot
