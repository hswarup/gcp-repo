resource "google_notebooks_instance" "instance" {
  name = "notebooks-instance"
  location = "australia-southeast1-a"
  machine_type = "n1-standard-4"
  metadata = {
    terraform  = "true"
  }
  container_image {
    repository = "gcr.io/deeplearning-platform-release/pytorch-gpu"
    tag = "latest"
  }
}
