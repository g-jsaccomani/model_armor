terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
}

provider "google-beta" {
  project = var.project_id
}

# 1. Enable Required Google Cloud APIs
resource "google_project_service" "modelarmor_api" {
  project            = var.project_id
  service            = "modelarmor.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "dlp_api" {
  project            = var.project_id
  service            = "dlp.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "logging_api" {
  project            = var.project_id
  service            = "logging.googleapis.com"
  disable_on_destroy = false
}

# 2. Cloud DLP (Sensitive Data Protection) Inspection Template
resource "google_data_loss_prevention_inspect_template" "model_armor_dlp_inspect" {
  count        = var.enable_dlp_integration ? 1 : 0
  parent       = "projects/${var.project_id}/locations/${var.location}"
  display_name = "Model Armor Sensitive Data Inspection Template"
  description  = "Inspects PII, financial credentials, and tokens for Model Armor guardrails"

  inspect_config {
    info_types {
      name = "EMAIL_ADDRESS"
    }
    info_types {
      name = "PHONE_NUMBER"
    }
    info_types {
      name = "CREDIT_CARD_NUMBER"
    }
    info_types {
      name = "US_SOCIAL_SECURITY_NUMBER"
    }
    info_types {
      name = "AUTH_TOKEN"
    }
    info_types {
      name = "GCP_CREDENTIALS"
    }
    info_types {
      name = "JSON_WEB_TOKEN"
    }
    info_types {
      name = "GENERIC_API_KEY"
    }

    min_likelihood = "LIKELY"
    include_quote  = true

    limits {
      max_findings_per_item    = 100
      max_findings_per_request = 0
    }
  }

  depends_on = [google_project_service.dlp_api]
}

# 3. Model Armor FloorSetting Provisioning
resource "null_resource" "model_armor_floor_setting" {
  count = var.enable_floor_setting ? 1 : 0

  triggers = {
    project_id = var.project_id
    enforce    = var.enable_floor_setting
  }

  provisioner "local-exec" {
    command = <<-EOT
      TOKEN=$(gcloud auth print-access-token)
      curl -s -X PATCH -H "Authorization: Bearer $TOKEN" -H "X-Goog-User-Project: ${var.project_id}" -H "Content-Type: application/json" \
        "https://modelarmor.googleapis.com/v1/projects/${var.project_id}/locations/global/floorSetting?updateMask=filterConfig,enableFloorSettingEnforcement" \
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
        }'
    EOT
  }

  depends_on = [google_project_service.modelarmor_api]
}

# 4. Model Armor Guardrail Template
resource "null_resource" "model_armor_template" {
  triggers = {
    project_id  = var.project_id
    location    = var.location
    template_id = var.template_id
  }

  provisioner "local-exec" {
    command = <<-EOT
      TOKEN=$(gcloud auth print-access-token)
      curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "X-Goog-User-Project: ${var.project_id}" -H "Content-Type: application/json" \
        "https://modelarmor.${var.location}.rep.googleapis.com/v1/projects/${var.project_id}/locations/${var.location}/templates?templateId=${var.template_id}" \
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
            "managed-by": "terraform",
            "environment": "security-lab"
          }
        }'
    EOT
  }

  depends_on = [google_project_service.modelarmor_api, null_resource.model_armor_floor_setting]
}
