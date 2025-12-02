#!/usr/bin/env bash
# ==============================================================================
# Model Armor - Fast GCP Setup & Provisioning Script
# ==============================================================================
set -euo pipefail

PROJECT_ID="${1:-$(gcloud config get-value project 2>/dev/null || echo "")}"
LOCATION="${2:-us-central1}"
TEMPLATE_ID="${3:-secops-guardrail-default}"

if [[ -z "$PROJECT_ID" ]]; then
  echo "[-] ERROR: GCP Project ID is required. Usage: ./setup_gcp_model_armor.sh <PROJECT_ID> [LOCATION] [TEMPLATE_ID]"
  exit 1
fi

echo "======================================================================"
echo " Setting up Google Cloud Model Armor"
echo " Project:   $PROJECT_ID"
echo " Location:  $LOCATION"
echo " Template:  $TEMPLATE_ID"
echo "======================================================================"

export CLOUDSDK_CONTEXT_AWARE_USE_CLIENT_CERTIFICATE=false
export CLOUDSDK_CONTEXT_AWARE_USE_ECP_HTTP_PROXY=false

# 1. Enable Required APIs
echo "[+] Enabling required APIs (modelarmor.googleapis.com, dlp.googleapis.com, logging.googleapis.com)..."
gcloud services enable modelarmor.googleapis.com dlp.googleapis.com logging.googleapis.com --project="$PROJECT_ID"

# 2. Grant IAM Roles
ACTIVE_USER="$(gcloud config get-value account 2>/dev/null || echo "")"
if [[ -n "$ACTIVE_USER" ]]; then
  echo "[+] Granting roles/modelarmor.admin to $ACTIVE_USER on project $PROJECT_ID..."
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="user:$ACTIVE_USER" \
    --role="roles/modelarmor.admin" \
    --quiet >/dev/null 2>&1 || true
fi

TOKEN="$(gcloud auth print-access-token)"

# 3. Configure Global FloorSetting
echo "[+] Configuring Model Armor Global FloorSetting..."
curl -s -X PATCH \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Goog-User-Project: $PROJECT_ID" \
  -H "Content-Type: application/json" \
  "https://modelarmor.googleapis.com/v1/projects/$PROJECT_ID/locations/global/floorSetting?updateMask=filterConfig,enableFloorSettingEnforcement" \
  -d '{
    "enableFloorSettingEnforcement": true,
    "filterConfig": {
      "raiSettings": {
        "raiFilters": [
          {"filterType": "HATE_SPEECH", "confidenceLevel": "MEDIUM_AND_ABOVE"},
          {"filterType": "HARASSMENT", "confidenceLevel": "MEDIUM_AND_ABOVE"},
          {"filterType": "SEXUALLY_EXPLICIT", "confidenceLevel": "MEDIUM_AND_ABOVE"},
          {"filterType": "DANGEROUS", "confidenceLevel": "MEDIUM_AND_ABOVE"}
        ]
      },
      "piAndJailbreakFilterSettings": {
        "filterEnforcement": "ENABLED",
        "confidenceLevel": "MEDIUM_AND_ABOVE"
      },
      "maliciousUriFilterSettings": {
        "filterEnforcement": "ENABLED"
      }
    }
  }' >/dev/null

# 4. Provision Model Armor Guardrail Template
echo "[+] Provisioning Model Armor Template ($TEMPLATE_ID in $LOCATION)..."
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Goog-User-Project: $PROJECT_ID" \
  -H "Content-Type: application/json" \
  "https://modelarmor.$LOCATION.rep.googleapis.com/v1/projects/$PROJECT_ID/locations/$LOCATION/templates?templateId=$TEMPLATE_ID" \
  -d '{
    "filterConfig": {
      "raiSettings": {
        "raiFilters": [
          {"filterType": "HATE_SPEECH", "confidenceLevel": "MEDIUM_AND_ABOVE"},
          {"filterType": "HARASSMENT", "confidenceLevel": "MEDIUM_AND_ABOVE"},
          {"filterType": "SEXUALLY_EXPLICIT", "confidenceLevel": "MEDIUM_AND_ABOVE"},
          {"filterType": "DANGEROUS", "confidenceLevel": "MEDIUM_AND_ABOVE"}
        ]
      },
      "piAndJailbreakFilterSettings": {
        "filterEnforcement": "ENABLED",
        "confidenceLevel": "MEDIUM_AND_ABOVE"
      },
      "maliciousUriFilterSettings": {
        "filterEnforcement": "ENABLED"
      }
    },
    "templateMetadata": {
      "logSanitizeOperations": true,
      "customPromptSafetyErrorMessage": "Prompt blocked by Model Armor security guardrail.",
      "customPromptSafetyErrorCode": 400,
      "customLlmResponseSafetyErrorMessage": "Model completion blocked by Model Armor security guardrail.",
      "customLlmResponseSafetyErrorCode": 400
    },
    "labels": {
      "managed-by": "setup-script",
      "environment": "lab"
    }
  }' >/dev/null || true

echo "[+] Model Armor setup completed successfully for $PROJECT_ID!"
echo "[+] Verify with: python3 -m evals.runner --project=$PROJECT_ID --template=$TEMPLATE_ID"
