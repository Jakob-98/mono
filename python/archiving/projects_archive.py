import os
import sys
import subprocess
import argparse
import shutil
from datetime import datetime
from tqdm import tqdm

def find_git_directories(start_path, max_depth):
    git_dirs = []
    start_level = start_path.count(os.sep)
    for root, dirs, files in os.walk(start_path):
        current_level = root.count(os.sep)
        if current_level - start_level >= max_depth:
            dirs[:] = []  # Skip subdirectories when max_depth is reached
            continue
        if '.git' in dirs:
            git_dirs.append(root)  # Store the root, not the .git directory itself
            dirs.remove('.git')  # Don't walk through the .git directory
    print(git_dirs)
    print(f"Found {len(git_dirs)} Git repositories")
    return git_dirs

def create_git_archive(repo_path, archive_root, start_dir):
    relative_repo_path = os.path.relpath(repo_path, start_dir)
    archive_subdir = os.path.join(archive_root, *relative_repo_path.split(os.sep))
    os.makedirs(archive_subdir, exist_ok=True)  # Ensure all directories are created
    archive_path = os.path.join(archive_subdir, 'archive.tar')  # Include the filename

    # Set up a custom global Git configuration to bypass the ownership check
    custom_git_config = os.path.join(repo_path, 'safe_git_config')
    repo_path_escaped = repo_path.replace('\\', '/')
    with open(custom_git_config, 'w') as config_file:
        config_file.write(f"[safe]\n\tdirectory = {repo_path_escaped}\n")

    # Set the environment variable to use the custom configuration
    env = os.environ.copy()
    env['GIT_CONFIG_GLOBAL'] = custom_git_config

    # Create a git archive of the repository at HEAD
    # Use absolute path for the output file
    absolute_archive_path = os.path.abspath(archive_path)
    cmd = ['git', 'archive', '--format=tar', '-o', absolute_archive_path, 'HEAD']
    try:
        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True, env=env)
        if result.returncode != 0:
            print(f"Failed to create archive for {repo_path}: {result.stderr}")
        else:
            print(f"Archive created: {absolute_archive_path}")
    except Exception as e:
        print(f"Failed to create archive for {repo_path}: {e}")

    # Clean up the custom Git configuration file
    os.remove(custom_git_config)

def main(start_dir, max_depth):
    if not os.path.isdir(start_dir):
        print(f"The provided path {start_dir} is not a directory or does not exist.")
        sys.exit(1)

    git_directories = find_git_directories(start_dir, max_depth)
    date_str = datetime.now().strftime('%Y%m%d')
    archive_folder_name = f"{os.path.basename(os.path.normpath(start_dir))}_arc_{date_str}"
    archive_root = os.path.join(start_dir, archive_folder_name)
    os.makedirs(archive_root, exist_ok=True)

    for git_dir in tqdm(git_directories, desc="Archiving repositories"):
        create_git_archive(git_dir, archive_root, start_dir)

    # Tar the final folder and delete the untarred archive folder
    shutil.make_archive(os.path.join(start_dir, archive_folder_name), 'tar', start_dir, archive_folder_name)
    confirmation = input(f"Press 'Y' to delete the untarred archive folder: {archive_root}")
    if confirmation.lower() == 'y':
        print(f"Deleting {archive_root}")
        shutil.rmtree(archive_root)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find and archive Git repositories.')
    parser.add_argument('directory', type=str, help='Directory to search for .git repositories')
    parser.add_argument('--depth', type=int, default=5, help='Maximum depth for directory traversal (default: 5)')
    args = parser.parse_args()

    main(args.directory, args.depth)