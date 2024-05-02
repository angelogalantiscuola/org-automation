import argparse
import subprocess
import os
import shutil


def are_tools_installed():
    # Check if 'gh' is installed
    if shutil.which("gh") is None:
        print("Error: 'gh' (GitHub CLI) is not installed.")
        return False

    # Check if 'git' is installed
    if shutil.which("git") is None:
        print("Error: 'git' is not installed.")
        return False

    return True


def create_repo(username, repo_name):
    # Create a new directory for your project
    os.mkdir(repo_name)

    # Navigate into the new directory
    os.chdir(repo_name)

    # Initialize a new Git repository
    subprocess.run(["git", "init"])

    # Create a README.md file with "TODO" inside
    with open("README.md", "w") as f:
        f.write("TODO")

    # Add the README.md file to the repository
    subprocess.run(["git", "add", "README.md"])

    # Commit the file with a message
    subprocess.run(["git", "commit", "-m", "Initial commit"])

    # Create a new repository on GitHub
    subprocess.run(["gh", "repo", "create", f"{username}/{repo_name}", "--public"])

    # Add the remote repository 'origin'
    subprocess.run(["git", "remote", "add", "origin", f"https://github.com/{username}/{repo_name}.git"])

    # Push the local repository to GitHub
    subprocess.run(["git", "push", "-u", "origin", "main"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new GitHub repository.")
    parser.add_argument("username", type=str, help="Your GitHub username")
    parser.add_argument("repo_name", type=str, help="The name of the new repository")

    args = parser.parse_args()

    if are_tools_installed():
        create_repo(args.username, args.repo_name)
    else:
        print("Please install the missing tools and try again.")
