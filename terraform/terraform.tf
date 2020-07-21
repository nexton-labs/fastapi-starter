terraform {
  backend "remote" {
    organization = "nexton"

    workspaces {
      name = "fastapi-starter"
    }
  }
}