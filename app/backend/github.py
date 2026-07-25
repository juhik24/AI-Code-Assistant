from git import Repo


def clone_repository(repo_url: str, clone_path):
    Repo.clone_from(repo_url, clone_path)