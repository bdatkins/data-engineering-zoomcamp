variable "credentials" {
    default  = "./keys/mycreds.json"
}

variable "project" {
    default="linear-archway-412518"
}

variable "bq_dataset_name" {
    default = "demo_dataset"
}

variable "gcs_storage_class" {
    default = "STANDARD"
}

variable "gcs_bucket_name" {
    default = "inear-archway-412518-demo-bucket"
}

variable "gcs_location" {
    default = "US"
}