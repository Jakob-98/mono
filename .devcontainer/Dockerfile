# Base image
FROM python:3.10-slim-buster

# This Dockerfile adds a non-root user with sudo access.
# Update the "remoteUser" setting in devcontainer.json to use it.
# Add sudo support for non-root user
RUN apt-get update \
    && apt-get install -y sudo \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
RUN useradd --create-home --shell /bin/bash vscode \
    && echo "vscode ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

# Set to your username
USER vscode

# Set up a working directory
WORKDIR /workspace

# Copy the requirements.txt file into our workspace
COPY requirements.txt /workspace

# Use pip to install dependencies
RUN python -m pip install --upgrade pip &&\
    pip install -r /workspace/requirements.txt
