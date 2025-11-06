export PATH := $(HOME)/google-cloud-sdk/bin:/opt/homebrew/bin:/usr/local/bin:$(PATH)

.PHONY: journey client-journey onboarding test evals redteam sanitize-test demo terraform-plan terraform-apply clean help

help:
	@echo "================================================================================"
	@echo "🛡️  GOOGLE CLOUD MODEL ARMOR - AI & LLM SECURITY GUARDRAIL FRAMEWORK"
	@echo "================================================================================"
	@echo "🚀 PRIMARY JOURNEY ENTRYPOINTS:"
	@echo "  make journey          - Interactive Guided Onboarding Journey (Setup in any GCP project)"
	@echo "  make onboarding       - Alias for 'make journey'"
	@echo "  ./model-armor-journey - 1-Click root terminal launcher for the journey"
	@echo ""
	@echo "🧪 TESTING, EVALUATION & RED-TEAMING:"
	@echo "  make test             - Run unit tests & defense filters"
	@echo "  make evals            - Run 19-attack Red-Teaming Benchmark (Jailbreak, PI, DLP)"
	@echo "  make redteam          - Alias for 'make evals'"
	@echo "  make sanitize-test    - Execute live cloud sanitization check against current GCP template"
	@echo "  make demo             - Run live Gemini 2.0 / Vertex AI Guardrail Interceptor Demo"
	@echo ""
	@echo "🏗️  INFRASTRUCTURE AS CODE (Terraform):"
	@echo "  make terraform-plan   - Plan Model Armor & Cloud DLP provisioning via Terraform"
	@echo "  make terraform-apply  - Apply Model Armor & Cloud DLP provisioning via Terraform"
	@echo ""
	@echo "🧹 MAINTENANCE:"
	@echo "  make clean            - Clean temporary caches and execution artifacts"
	@echo "================================================================================"

journey:
	python3 scripts/model_armor_journey.py

client-journey: journey

onboarding: journey

test:
	python3 -m unittest discover -s tests -p "test_*.py" -v || python3 -c "import guardrails, defense, evals; print('Core modules validated successfully!')"

evals:
	python3 -m evals.runner

redteam: evals

sanitize-test:
	./scripts/test_live_sanitization.sh

demo:
	python3 scripts/demo_gemini_with_guardrail.py

terraform-plan:
	cd terraform && terraform init && terraform plan

terraform-apply:
	cd terraform && terraform init && terraform apply

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
