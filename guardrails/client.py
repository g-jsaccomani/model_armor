"""
Google Cloud Model Armor Python Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Enterprise client library for Google Cloud Model Armor API (v1).
Supports prompt sanitization, model completion sanitization,
FloorSettings management, and Template lifecycle operations.
"""

from dataclasses import dataclass, field
import json
import os
import subprocess
from typing import Any, Dict, List, Optional
import urllib.error
import urllib.parse
import urllib.request


class ModelArmorSecurityException(Exception):
    """Raised when Model Armor security filters detect an adversarial attack or policy violation."""

    def __init__(self, message: str, findings: Dict[str, Any], error_code: int = 400):
        super().__init__(message)
        self.findings = findings
        self.error_code = error_code


@dataclass
class SanitizationResult:
    is_blocked: bool
    filter_match_state: str
    error_message: Optional[str] = None
    error_code: Optional[int] = None
    matched_filters: List[str] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)
    sanitized_text: Optional[str] = None


class ModelArmorClient:
    """Client for Google Cloud Model Armor."""

    def __init__(
        self,
        project_id: Optional[str] = None,
        location: str = "us-central1",
        credentials_token: Optional[str] = None,
    ):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
        if not self.project_id:
            # Attempt to resolve from gcloud
            try:
                out = subprocess.check_output(
                    ["gcloud", "config", "get-value", "project"],
                    stderr=subprocess.DEVNULL,
                    text=True,
                ).strip()
                if out:
                    self.project_id = out
            except Exception:
                pass

        if not self.project_id:
            raise ValueError("project_id must be provided or configured in GCP environment.")

        self.location = location
        self._token = credentials_token

    def _get_access_token(self) -> str:
        """Retrieves active OAuth2 access token for GCP API calls."""
        if self._token:
            return self._token

        # Try google.auth if installed
        try:
            import google.auth
            import google.auth.transport.requests

            creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)
            return creds.token
        except Exception:
            pass

        # Fallback to gcloud CLI
        try:
            env = os.environ.copy()
            env["CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE"] = "false"
            env["CLOUDSDK_CONTEXT_AWARE_USE_ECP_HTTP_PROXY"] = "false"
            token = subprocess.check_output(
                ["gcloud", "auth", "print-access-token"],
                env=env,
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
            return token
        except Exception as e:
            raise RuntimeError(f"Failed to acquire GCP access token: {e}")

    def _get_base_url(self, location: Optional[str] = None) -> str:
        loc = location or self.location
        if loc == "global":
            return "https://modelarmor.googleapis.com"
        return f"https://modelarmor.{loc}.rep.googleapis.com"

    def _request(
        self,
        method: str,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Executes an HTTP request against the Model Armor API."""
        base_url = self._get_base_url(location)
        url = f"{base_url}/{path.lstrip('/')}"
        token = self._get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "X-Goog-User-Project": self.project_id,
            "Content-Type": "application/json; charset=utf-8",
        }

        data_bytes = None
        if body is not None:
            data_bytes = json.dumps(body).encode("utf-8")

        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)

        import ssl
        try:
            import certifi
            ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        except Exception:
            ssl_ctx = ssl.create_default_context()

        try:
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=30) as resp:
                resp_data = resp.read().decode("utf-8")
                return json.loads(resp_data) if resp_data else {}
        except urllib.error.HTTPError as e:
            err_content = e.read().decode("utf-8", errors="ignore")
            try:
                err_json = json.loads(err_content)
                msg = err_json.get("error", {}).get("message", err_content)
            except Exception:
                msg = err_content
            raise RuntimeError(f"Model Armor API error ({e.code}): {msg}")

    def sanitize_user_prompt(
        self,
        text: str,
        template_id: str = "secops-guardrail-default",
        location: Optional[str] = None,
        raise_on_violation: bool = False,
    ) -> SanitizationResult:
        """
        Sanitizes a user prompt using the specified Model Armor template.

        Args:
            text: The user prompt string to inspect and sanitize.
            template_id: The Model Armor template ID.
            location: The location of the template (defaults to client location).
            raise_on_violation: If True, raises ModelArmorSecurityException on detection.
        """
        loc = location or self.location
        path = f"v1/projects/{self.project_id}/locations/{loc}/templates/{template_id}:sanitizeUserPrompt"
        body = {"userPromptData": {"text": text}}

        resp = self._request("POST", path, body=body, location=loc)
        san_res = resp.get("sanitizationResult", {})
        match_state = san_res.get("filterMatchState", "NO_MATCH_FOUND")
        is_blocked = match_state == "MATCH_FOUND"

        matched = []
        filter_results = san_res.get("filterResults", {})
        for fname, fval in filter_results.items():
            for subk, subv in fval.items():
                if isinstance(subv, dict) and subv.get("matchState") == "MATCH_FOUND":
                    matched.append(fname)
                    break

        meta = san_res.get("sanitizationMetadata", {})
        err_msg = meta.get("errorMessage")
        err_code = int(meta.get("errorCode", 400)) if meta.get("errorCode") else None

        result = SanitizationResult(
            is_blocked=is_blocked,
            filter_match_state=match_state,
            error_message=err_msg,
            error_code=err_code,
            matched_filters=matched,
            raw_response=resp,
        )

        if is_blocked and raise_on_violation:
            raise ModelArmorSecurityException(
                message=err_msg or f"Prompt blocked by Model Armor filter: {matched}",
                findings=san_res,
                error_code=err_code or 400,
            )

        return result

    def sanitize_model_response(
        self,
        text: str,
        template_id: str = "secops-guardrail-default",
        location: Optional[str] = None,
        raise_on_violation: bool = False,
    ) -> SanitizationResult:
        """
        Sanitizes an LLM output / model response using Model Armor.

        Args:
            text: The LLM completion text to inspect and sanitize.
            template_id: The Model Armor template ID.
            location: The location of the template.
            raise_on_violation: If True, raises ModelArmorSecurityException on violation.
        """
        loc = location or self.location
        path = f"v1/projects/{self.project_id}/locations/{loc}/templates/{template_id}:sanitizeModelResponse"
        body = {"modelResponseData": {"text": text}}

        resp = self._request("POST", path, body=body, location=loc)
        san_res = resp.get("sanitizationResult", {})
        match_state = san_res.get("filterMatchState", "NO_MATCH_FOUND")
        is_blocked = match_state == "MATCH_FOUND"

        matched = []
        filter_results = san_res.get("filterResults", {})
        for fname, fval in filter_results.items():
            for subk, subv in fval.items():
                if isinstance(subv, dict) and subv.get("matchState") == "MATCH_FOUND":
                    matched.append(fname)
                    break

        meta = san_res.get("sanitizationMetadata", {})
        err_msg = meta.get("errorMessage")
        err_code = int(meta.get("errorCode", 400)) if meta.get("errorCode") else None

        result = SanitizationResult(
            is_blocked=is_blocked,
            filter_match_state=match_state,
            error_message=err_msg,
            error_code=err_code,
            matched_filters=matched,
            raw_response=resp,
        )

        if is_blocked and raise_on_violation:
            raise ModelArmorSecurityException(
                message=err_msg or f"Model response blocked by Model Armor filter: {matched}",
                findings=san_res,
                error_code=err_code or 400,
            )

        return result

    def get_floor_setting(self) -> Dict[str, Any]:
        """Retrieves global FloorSetting resource for the project."""
        path = f"v1/projects/{self.project_id}/locations/global/floorSetting"
        return self._request("GET", path, location="global")

    def update_floor_setting(
        self,
        config: Dict[str, Any],
        update_mask: str = "filterConfig,enableFloorSettingEnforcement",
    ) -> Dict[str, Any]:
        """Updates the project-level global FloorSetting resource."""
        path = f"v1/projects/{self.project_id}/locations/global/floorSetting?updateMask={update_mask}"
        return self._request("PATCH", path, body=config, location="global")

    def list_templates(self, location: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists all Model Armor templates in the specified location."""
        loc = location or self.location
        path = f"v1/projects/{self.project_id}/locations/{loc}/templates"
        resp = self._request("GET", path, location=loc)
        return resp.get("templates", [])

    def get_template(self, template_id: str, location: Optional[str] = None) -> Dict[str, Any]:
        """Gets details of a specific Model Armor template."""
        loc = location or self.location
        path = f"v1/projects/{self.project_id}/locations/{loc}/templates/{template_id}"
        return self._request("GET", path, location=loc)

    def create_template(
        self,
        template_id: str,
        config: Dict[str, Any],
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a new Model Armor template."""
        loc = location or self.location
        path = f"v1/projects/{self.project_id}/locations/{loc}/templates?templateId={template_id}"
        return self._request("POST", path, body=config, location=loc)

    def delete_template(self, template_id: str, location: Optional[str] = None) -> Dict[str, Any]:
        """Deletes a Model Armor template."""
        loc = location or self.location
        path = f"v1/projects/{self.project_id}/locations/{loc}/templates/{template_id}"
        return self._request("DELETE", path, location=loc)

# Audit checkpoint [2026-02-19]: feat(safety-template): deploy tenant-specific content safety template for client portal

# Audit checkpoint [2026-03-24]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2026-03-27]: feat(safety-template): deploy tenant-specific content safety template for client portal

# Audit checkpoint [2026-03-27]: refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app

# Audit checkpoint [2026-04-14]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset

# Audit checkpoint [2026-04-14]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant
