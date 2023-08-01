variable "location" {
  description = "The Azure region in which all resources should be created"
  default     = "West Europe"
}

variable "resource_group_name" {
  description = "The name of the resource group"
  default     = "rg-serverlesscomments-euw"
}

variable "storage_account_name" {
  description = "The name of the storage account"
  default     = "stserverlesscommentseuw"
}

variable "storage_table_name" {
  description = "The name of the storage table"
  default     = "commenttable"
}

variable "app_service_plan_name" {
  description = "The name of the app service plan"
  default     = "appserv-servlcmnt-euw"
}

variable "function_app_name" {
  description = "The name of the function app"
  default     = "servlcmnt-funcapp-euw"
}
