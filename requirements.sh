#!/bin/bash
# install_extra_deps.sh
# This script installs additional dependencies not managed by rosdep.

# Exit immediately if any command fails
set -e

echo "Starting manual installation of extra dependencies..."

# Install Python libraries not handled by rosdep
pip3 install --upgrade pip
pip3 install control

# Install system packages not handled by rosdep
# Uncomment the line below if you need to install a system package, e.g., python3-pyqt6
# sudo apt-get update && sudo apt-get install -y python3-pyqt6

echo "Finished installing extra dependencies."
