output "project_id" {
  description = "The GCP Project ID where Model Armor is deployed"
  value       = var.project_id
}

output "location" {
  description = "The location of the Model Armor template"
  value       = var.location
}

output "template_name" {
  description = "The full resource name of the deployed Model Armor template"
  value       = "projects/${var.project_id}/locations/${var.location}/templates/${var.template_id}"
}

output "dlp_inspect_template_id" {
  description = "The resource name of the Cloud DLP inspect template"
  value       = try(google_data_loss_prevention_inspect_template.model_armor_dlp_inspect[0].name, null)
}
