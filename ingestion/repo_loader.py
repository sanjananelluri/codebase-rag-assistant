from git import Repo
import os

BASE_DIR = "repos"


def clone_repo(repo_url: str) -> str:
    os.makedirs(BASE_DIR, exist_ok=True)
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_path = os.path.join(BASE_DIR, repo_name)

    if not os.path.exists(repo_path):
        Repo.clone_from(repo_url, repo_path)

    return repo_path


def read_code_files(repo_path: str):
    code_files = []
    allowed_ext = (".py", ".js", ".ts", ".java")

    for root, dirs, files in os.walk(repo_path):
        if ".git" in root or "node_modules" in root or "venv" in root:
            continue

        for file in files:
            if file.endswith(allowed_ext):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        code_files.append({
                            "path": full_path,
                            "content": f.read()
                        })
                except Exception:
                    pass

    return code_files