"""
Heuristic & Fast Signature Pre-screening Filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Provides rapid local detection for obvious injection patterns, obfuscation
(base64, hex, zero-width characters), and prompt override attempts.
"""

import base64
import re
from typing import List, Optional, Tuple


class HeuristicFilter:
    """Pre-screening rule engine for common adversarial patterns."""

    INJECTION_PATTERNS = [
        r"(?i)ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|directives|prompts)",
        r"(?i)disregard\s+(all\s+)?(previous|prior|system)\s+rules",
        r"(?i)you\s+are\s+now\s+in\s+developer\s+mode",
        r"(?i)DAN\s+mode\s+enabled",
        r"(?i)reveal\s+(the\s+)?(system\s+prompt|initial\s+instructions|hidden\s+prompt)",
        r"(?i)print\s+(all\s+)?(environment\s+variables|api\s+keys|secrets)",
        r"(?i)repeat\s+everything\s+above\s+verbatim",
    ]

    def __init__(self):
        self._compiled_patterns = [re.compile(p) for p in self.INJECTION_PATTERNS]

    def strip_zero_width_chars(self, text: str) -> str:
        """Removes hidden Unicode zero-width characters often used to evade detectors."""
        zero_width_chars = "\u200b\u200c\u200d\ufeff\u200e\u200f\u202a\u202b\u202c\u202d\u202e"
        return re.sub(f"[{zero_width_chars}]", "", text)

    def decode_obfuscated_blocks(self, text: str) -> List[str]:
        """Detects and decodes base64 strings contained in prompts."""
        decoded = []
        # Find base64 strings with length > 16
        b64_matches = re.findall(r"(?:[A-Za-z0-9+/]{4}){4,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?", text)
        for b64 in b64_matches:
            try:
                dec = base64.b64decode(b64).decode("utf-8", errors="ignore")
                if len(dec) > 8 and any(c.isalpha() for c in dec):
                    decoded.append(dec)
            except Exception:
                pass
        return decoded

    def analyze(self, text: str) -> Tuple[bool, List[str]]:
        """
        Analyzes a prompt against local heuristic signatures.

        Returns:
            Tuple of (is_suspicious, reasons)
        """
        reasons = []
        cleaned_text = self.strip_zero_width_chars(text)

        # Check raw patterns
        for pat in self._compiled_patterns:
            if pat.search(cleaned_text):
                reasons.append(f"Matched adversarial signature: {pat.pattern}")

        # Check base64 decoded payloads
        decoded_payloads = self.decode_obfuscated_blocks(cleaned_text)
        for payload in decoded_payloads:
            for pat in self._compiled_patterns:
                if pat.search(payload):
                    reasons.append(f"Matched hidden signature in decoded payload: {pat.pattern}")

        return len(reasons) > 0, reasons

# Audit checkpoint [2025-12-17]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2025-12-19]: feat(safety-template): deploy tenant-specific content safety template for client portal

# Audit checkpoint [2026-01-12]: feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS

# Audit checkpoint [2026-01-17]: feat(safety-template): deploy tenant-specific content safety template for client portal

# Audit checkpoint [2026-01-27]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2026-03-16]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2026-03-26]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2026-04-03]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2026-04-16]: feat(safety-template): deploy tenant-specific content safety template for client portal
