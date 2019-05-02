#!/bin/bash

# This script is used for installing and setting up the docker container that runs everything. 
# Run the build_project.sh instead for automatic install and activation

# This script is for ubuntu 18.04

# update everything 
sudo apt-update

# install prerequisite packages
sudo apt install apt-transport-https ca-certificates curl software - properties-common

# Adding the GPG key for official docker system
curl -fsSl https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# adding the docker repository to APT sources:
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"

# updating everything
sudo apt update

# installing Docker-ce
sudo apt install docker-ce

# checking status of docker
sudo systemctl status docker

# Adding docker to group to run without sudo
sudo usermod -aG docker "$(whoami)"

# Docker is now installed
