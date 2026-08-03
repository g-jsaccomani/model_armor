# Hands-on Lab Guide: Deploying and Testing Google Cloud Model Armor

## Lab Objectives
By completing this hands-on lab, you will:
1. Enable and configure Google Cloud Model Armor and Cloud DLP in a GCP project.
2. Configure Global FloorSettings to enforce an enterprise security baseline.
3. Deploy a custom Model Armor Template tailored for production AI workloads.
4. Execute live adversarial red-team benchmarks against the guardrail.
5. Integrate Model Armor with Gemini / Vertex AI using Python middleware.

---

## Lab Prerequisites
- Google Cloud Project with Billing Enabled.
- Google Cloud SDK (`gcloud`) installed and authenticated (`gcloud auth login`).
- Python 3.10+ installed.

---

## Step 1: Automated Lab Environment Setup

Run the automated provisioning script to enable the Model Armor API and deploy default guardrails:

```bash
cd /Users/jsaccomani/Documents/Jetsky/My\ Projects/model_armor
./scripts/setup_gcp_model_armor.sh <YOUR_PROJECT_ID> us-central1 secops-guardrail-default
```

---

## Step 2: Verify FloorSettings & Templates

Inspect the deployed resources using the Model Armor CLI:

```bash
# Check project FloorSetting
python3 -m guardrails.cli --project=<YOUR_PROJECT_ID> get-floor-setting

# List active templates
python3 -m guardrails.cli --project=<YOUR_PROJECT_ID> list-templates
```

---

## Step 3: Test Interactive Prompt Sanitization

Run the interactive live testing script to observe real-time protection:

```bash
./scripts/test_live_sanitization.sh <YOUR_PROJECT_ID>
```

---

## Step 4: Run the Red-Teaming Benchmark Suite

Execute the automated safety benchmark across 19+ attack vectors:

```bash
python3 -m evals.runner --project=<YOUR_PROJECT_ID> --template=secops-guardrail-default
```

---

## Step 5: Test End-to-End Gemini Integration

Run the Python demo simulating a protected Gemini application workflow:

```bash
python3 scripts/demo_gemini_with_guardrail.py <YOUR_PROJECT_ID> secops-guardrail-default
```

<!-- Checkpoint: 2025-12-26 - sec(pii-redaction): fine-tune PII masking and redaction rules for customer healthcare LLM pipeline -->

<!-- Checkpoint: 2026-01-06 - sec(pii-redaction): fine-tune PII masking and redaction rules for customer healthcare LLM pipeline -->

<!-- Checkpoint: 2026-02-06 - docs(adversarial-tests): document adversarial robustness testing results for client validation -->

<!-- Checkpoint: 2026-03-19 - docs(adversarial-tests): document adversarial robustness testing results for client validation -->

<!-- Checkpoint: 2026-05-01 - docs(adversarial-tests): document adversarial robustness testing results for client validation -->

<!-- Checkpoint: 2026-06-01 - docs(adversarial-tests): document adversarial robustness testing results for client validation -->

<!-- Checkpoint: 2026-07-06 - docs(adversarial-tests): document adversarial robustness testing results for client validation -->

<!-- Checkpoint: 2026-07-13 - docs(adversarial-tests): document adversarial robustness testing results for client validation -->

<!-- Checkpoint: 2026-08-03 - sec(pii-redaction): fine-tune PII masking and redaction rules for customer healthcare LLM pipeline -->
