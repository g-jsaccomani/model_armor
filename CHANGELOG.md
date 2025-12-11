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

