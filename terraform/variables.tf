variable "project_id" {
  description = "The Google Cloud Project ID where Model Armor will be configured"
  type        = string
}

variable "location" {
  description = "The Google Cloud region for Model Armor templates (e.g., us-central1, us-east1, europe-west1)"
  type        = string
  default     = "us-central1"
}

variable "template_id" {
  description = "The resource ID of the Model Armor template"
  type        = string
  default     = "secops-guardrail-default"
}

variable "enable_floor_setting" {
  description = "Whether to enforce enterprise baseline FloorSettings across the project"
  type        = bool
  default     = true
}

variable "enable_dlp_integration" {
  description = "Whether to provision Cloud DLP / Sensitive Data Protection inspect and de-identify templates"
  type        = bool
  default     = true
}

variable "labels" {
  description = "Resource labels to attach to Model Armor templates"
  type        = map(string)
  default = {
    managed-by  = "terraform"
    environment = "security-lab"
    framework   = "model-armor"
  }
}
