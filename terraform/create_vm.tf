resource "google_compute_instance" "vm_instance" {
  name         = "sample_vm"
  machine_type = "n1-standard-4"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      labels = { image = "pytorch-1-12-cu113-notebooks-v20220928-debian-10" }
    }
  }

  network_interface {
    # A default network is created for all GCP projects
    network = "default"
    access_config {
    }
  }
}
