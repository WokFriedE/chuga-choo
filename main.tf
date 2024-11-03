terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.23.1"
    }
  }
}

provider "docker" {
}

resource "docker_image" "backend" {
  name = "backend:latest"
  build {
    path = "./backend"
  }
}

resource "docker_image" "frontend" {
  name = "frontend:latest"
  build {
    path = "./frontend"
  }
}

# resource "docker_image" "nginx" {
#   name = "nginx:latest"
# }

resource "docker_container" "backend" {
  name  = "backend"
  image = docker_image.backend.latest
  ports {
    internal = 8000
    external = 8000
  }
}

resource "docker_container" "frontend" {
  name  = "frontend"
  image = docker_image.frontend.latest
  ports {
    internal = 80
    external = 3000
  }
  depends_on = [docker_container.backend]
}
