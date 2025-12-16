# Changelog - model_armor

All notable changes and security updates recorded below.

### [2025-12-08] fix(latency-optimization): optimize Model Armor inspection latency for real-time customer voice bot
- Refactored inspection pipeline to enable parallelized asynchronous checks for non-critical safety categories.

### [2025-12-09] feat(safety-template): deploy tenant-specific content safety template for client portal
- Configured custom safety templates with distinct sensitivity thresholds for internal vs external users.

### [2025-12-10] refactor(fastapi-middleware): enhance FastAPI wrapper for Model Armor proxy integration in client app
- Built drop-in ASGI middleware intercepting incoming requests and outgoing LLM streaming responses.

### [2025-12-11] docs(adversarial-tests): document adversarial robustness testing results for client validation
- Authored technical report detailing red-team findings on Model Armor protected endpoints.

### [2025-12-12] feat(tenant-sanitization): add input/output prompt sanitization rules for multi-tenant client SaaS
- Configured output sanitization rules preventing model from leaking internal system prompts and database schemas.

### [2025-12-16] feat(audit-telemetry): export Model Armor safety violation telemetry to client BigQuery dataset
- Created streaming telemetry exporter sending structured violation records to customer analytical warehouse.

