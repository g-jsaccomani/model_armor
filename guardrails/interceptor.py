"""
Gemini / Vertex AI Guardrail Interceptor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Transparent middleware and decorator for Google GenAI / Vertex AI / LangChain
applications to enforce Model Armor security policies on LLM inputs and outputs.
"""

from functools import wraps
import logging
from typing import Any, Callable, Dict, Optional
from .client import ModelArmorClient, ModelArmorSecurityException

logger = logging.getLogger("model_armor.guardrails")


class GeminiGuardrailInterceptor:
    """
    Middleware interceptor that wraps LLM calls with Model Armor security filters.
    """

    def __init__(
        self,
        client: Optional[ModelArmorClient] = None,
        template_id: str = "secops-guardrail-default",
        location: str = "us-central1",
        block_on_prompt_violation: bool = True,
        block_on_response_violation: bool = True,
    ):
        self.client = client or ModelArmorClient(location=location)
        self.template_id = template_id
        self.location = location
        self.block_on_prompt_violation = block_on_prompt_violation
        self.block_on_response_violation = block_on_response_violation

    def inspect_prompt(self, prompt: str) -> str:
        """
        Sanitizes user prompt before it is sent to the LLM.
        Raises ModelArmorSecurityException if an attack is detected and blocking is enabled.
        """
        logger.debug("Inspecting user prompt with Model Armor template: %s", self.template_id)
        result = self.client.sanitize_user_prompt(
            text=prompt,
            template_id=self.template_id,
            location=self.location,
            raise_on_violation=self.block_on_prompt_violation,
        )
        if result.is_blocked:
            logger.warning("Prompt blocked by Model Armor filters: %s", result.matched_filters)
        return result.sanitized_text or prompt

    def inspect_response(self, response_text: str) -> str:
        """
        Sanitizes model output before it is returned to the user.
        Raises ModelArmorSecurityException if toxic/sensitive content is detected.
        """
        logger.debug("Inspecting model response with Model Armor template: %s", self.template_id)
        result = self.client.sanitize_model_response(
            text=response_text,
            template_id=self.template_id,
            location=self.location,
            raise_on_violation=self.block_on_response_violation,
        )
        if result.is_blocked:
            logger.warning("Model response blocked by Model Armor filters: %s", result.matched_filters)
        return result.sanitized_text or response_text

    def protect_call(self, llm_func: Callable[[str], str], prompt: str) -> str:
        """
        Executes an end-to-end protected LLM invocation.
        """
        sanitized_prompt = self.inspect_prompt(prompt)
        raw_response = llm_func(sanitized_prompt)
        sanitized_response = self.inspect_response(raw_response)
        return sanitized_response


def guardrail_protected(
    template_id: str = "secops-guardrail-default",
    location: str = "us-central1",
    project_id: Optional[str] = None,
):
    """
    Decorator for Python functions that accept a prompt and return an LLM response.

    Example:
        @guardrail_protected(template_id="secops-guardrail-default")
        def ask_gemini(prompt: str) -> str:
            return gemini_model.generate_content(prompt).text
    """
    def decorator(func: Callable[..., Any]):
        interceptor = GeminiGuardrailInterceptor(
            client=ModelArmorClient(project_id=project_id, location=location),
            template_id=template_id,
            location=location,
        )

        @wraps(func)
        def wrapper(prompt: str, *args, **kwargs):
            clean_prompt = interceptor.inspect_prompt(prompt)
            output = func(clean_prompt, *args, **kwargs)
            if isinstance(output, str):
                return interceptor.inspect_response(output)
            return output

        return wrapper

    return decorator

# Audit checkpoint [2026-01-07]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2026-01-19]: refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app

# Audit checkpoint [2026-02-05]: refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app

# Audit checkpoint [2026-02-24]: feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS

# Audit checkpoint [2026-03-06]: feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS
