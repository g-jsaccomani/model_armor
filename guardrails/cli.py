"""
Model Armor CLI Utility
~~~~~~~~~~~~~~~~~~~~~~~
Command-line interface to inspect prompts, test completions, manage templates,
and apply Model Armor security policies in Google Cloud.
"""

import argparse
import json
import os
import sys
from typing import Optional
from .client import ModelArmorClient, ModelArmorSecurityException


def main():
    parser = argparse.ArgumentParser(
        prog="model-armor",
        description="Google Cloud Model Armor Guardrails CLI",
    )
    parser.add_argument("--project", "-p", help="GCP Project ID", default=None)
    parser.add_argument("--location", "-l", help="Model Armor Location", default="us-central1")

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Command: check-prompt
    p_check = subparsers.add_parser("check-prompt", help="Inspect a prompt for attacks & policy violations")
    p_check.add_argument("prompt", help="The prompt text to sanitize")
    p_check.add_argument("--template", "-t", default="secops-guardrail-default", help="Template ID")

    # Command: check-response
    p_resp = subparsers.add_parser("check-response", help="Inspect an LLM response for PII/safety violations")
    p_resp.add_argument("response", help="The LLM completion text to sanitize")
    p_resp.add_argument("--template", "-t", default="secops-guardrail-default", help="Template ID")

    # Command: list-templates
    p_list = subparsers.add_parser("list-templates", help="List all Model Armor templates in project/location")

    # Command: get-floor-setting
    p_floor = subparsers.add_parser("get-floor-setting", help="View project FloorSetting")

    # Command: apply-template
    p_apply = subparsers.add_parser("apply-template", help="Create or update a template from a JSON file")
    p_apply.add_argument("--template-id", required=True, help="ID for the new template")
    p_apply.add_argument("--file", "-f", required=True, help="Path to template JSON file")

    # Command: apply-floor-setting
    p_apply_floor = subparsers.add_parser("apply-floor-setting", help="Apply FloorSetting configuration from file")
    p_apply_floor.add_argument("--file", "-f", required=True, help="Path to FloorSetting JSON file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = ModelArmorClient(project_id=args.project, location=args.location)

    try:
        if args.command == "check-prompt":
            print(f"[*] Inspecting prompt with template: {args.template} (location: {args.location})...")
            res = client.sanitize_user_prompt(args.prompt, template_id=args.template)
            if res.is_blocked:
                print(f"[!] BLOCKED: Violation detected!")
                print(f"    Error Code: {res.error_code}")
                print(f"    Message: {res.error_message}")
                print(f"    Triggered Filters: {res.matched_filters}")
                sys.exit(2)
            else:
                print("[+] PASSED: Prompt passed all security guardrails.")
                sys.exit(0)

        elif args.command == "check-response":
            print(f"[*] Inspecting response with template: {args.template}...")
            res = client.sanitize_model_response(args.response, template_id=args.template)
            if res.is_blocked:
                print(f"[!] BLOCKED: Model output violation detected!")
                print(f"    Error Code: {res.error_code}")
                print(f"    Message: {res.error_message}")
                print(f"    Triggered Filters: {res.matched_filters}")
                sys.exit(2)
            else:
                print("[+] PASSED: Model output passed all security guardrails.")
                sys.exit(0)

        elif args.command == "list-templates":
            print(f"[*] Fetching templates in {client.project_id} ({args.location})...")
            templates = client.list_templates()
            if not templates:
                print("No templates found in this location.")
            for t in templates:
                print(f" - {t.get('name')}")
            sys.exit(0)

        elif args.command == "get-floor-setting":
            print(f"[*] Fetching FloorSetting for {client.project_id}...")
            floor = client.get_floor_setting()
            print(json.dumps(floor, indent=2))
            sys.exit(0)

        elif args.command == "apply-template":
            with open(args.file, "r") as f:
                config = json.load(f)
            print(f"[*] Creating template '{args.template_id}' from {args.file}...")
            res = client.create_template(args.template_id, config)
            print(f"[+] Template created: {res.get('name')}")
            sys.exit(0)

        elif args.command == "apply-floor-setting":
            with open(args.file, "r") as f:
                config = json.load(f)
            print(f"[*] Updating FloorSetting from {args.file}...")
            res = client.update_floor_setting(config)
            print(f"[+] FloorSetting updated: {res.get('name')}")
            sys.exit(0)

    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# Audit checkpoint [2025-12-16]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2025-12-30]: refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app

# Audit checkpoint [2026-01-09]: refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app

# Audit checkpoint [2026-01-13]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2026-01-31]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset

# Audit checkpoint [2026-02-02]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant

# Audit checkpoint [2026-02-10]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset

# Audit checkpoint [2026-03-12]: feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset

# Audit checkpoint [2026-03-19]: refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app

# Audit checkpoint [2026-04-11]: feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS

# Audit checkpoint [2026-04-24]: fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot

# Audit checkpoint [2026-05-07]: feat(jailbreak-filter): configure customized jailbreak detection filters for client banking assistant
