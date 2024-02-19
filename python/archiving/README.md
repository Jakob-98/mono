# Git Repository Archiver

This script searches for Git repositories in a specified directory and its subdirectories, and creates an archive of each repository found. It bypasses the safety checks by setting up a custom Git configuration.

## Usage

1. Run the script with the directory to search for Git repositories as an argument.
2. Optionally, specify the maximum depth for directory traversal with `--depth`.

bash python git_archiver.py <directory> [--depth <max_depth>]

**Warning:** This script bypasses Git's safety mechanisms by using a custom Git configuration. Use with caution and understand the risks before proceeding.

## Example

`python git_archiver.py /path/to/search --depth 3`

This will search for Git repositories in `/path/to/search` and its subdirectories up to 3 levels deep, and create an archive for each repository found.