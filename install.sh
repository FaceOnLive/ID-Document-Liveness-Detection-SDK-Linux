#!/bin/sh

echo "Install environment..."

. /etc/os-release
ubuntu_version="$VERSION_ID"
echo "Ubuntu version: $ubuntu_version"

# Check if the version is 22.04 or later
if [ "$ubuntu_version" \< "22.04" ]; then
    # Print an error message and exit
    echo "Error: Ubuntu version must be 22.04 or later"
    exit 1
fi

# Install packages:
sudo apt-get update -y && sudo apt-get install -y binutils python3 python3-pip python3-opencv

# Install requirements:
python3 -m pip install --upgrade pip && python3 -m pip install -r requirements.txt

# Copy library  
sudo cp -rf ./dependency/* /usr/lib

echo "Installed successfully!"
