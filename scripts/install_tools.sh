#!/bin/bash

# The 'set -e' command instructs the shell to immediately exit if any command within the script returns a non-zero exit status.
# This helps prevent the script from continuing execution after an error, which can improve reliability and safety.
set -e

### Install AWS CLI v2 ###

# Check if AWS CLI is already installed
if command -v aws >/dev/null 2>&1; then
    echo "AWS CLI is already installed."
    aws --version
    exit 0
fi

# Determine the architecture of the machine
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    AWSCLI_URL="https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"
elif [ "$ARCH" = "aarch64" ]; then
    AWSCLI_URL="https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

# Download AWS CLI v2 installer
curl "$AWSCLI_URL" -o "/tmp/awscliv2.zip"

# Unzip the installer
unzip -q /tmp/awscliv2.zip -d /tmp

# Install AWS CLI
sudo /tmp/aws/install

# Clean up
rm -rf /tmp/aws /tmp/awscliv2.zip

# Verify installation
aws --version