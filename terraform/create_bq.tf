module "bigquery" {
  source  = "terraform-google-modules/bigquery/google"
  version = "5.4.1"
  dataset_id                  = "dataset1"
  dataset_name                = "dataset1"
  description                 = "My dataset"
  project_id                  = "proj1"
  location                    = "EU"
  default_table_expiration_ms = 3600000
  tables = []
}
