module "storage" {
  source      = "git::https://github.com/CloudNativeTech/terraform-module-gcs.git"
  bucket_name = "bucket1"
  storage_class= "STANDARD"
  project_id  = "project1"
  labels = {
    "environment" = "poc"
    "team"        = "mychapter"
  }
}

