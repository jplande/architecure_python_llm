import git
import os
import tempfile
import shutil

def clone_repository(repo_url, branch="main"):
    """
    Clone a git repository and return the path to the cloned repo
    """
    temp_dir = tempfile.mkdtemp()
    try:
        print(f"Cloning repository {repo_url} into {temp_dir}...")
        repo = git.Repo.clone_from(repo_url, temp_dir, branch=branch)
        return temp_dir
    except git.GitCommandError as e:
        print(f"Error cloning repository: {e}")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None

def list_files(repo_path, extension=None):
    """
    List all files in the repository, optionally filtered by extension
    """
    files = []
    for root, dirs, filenames in os.walk(repo_path):
        for filename in filenames:
            if extension is None or filename.endswith(extension):
                files.append(os.path.join(root, filename))
    return files