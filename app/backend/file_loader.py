from pathlib import Path

SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".go",
    ".rs",
    ".md",
    ".json",
}

IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "__MACOSX",   # Added
}

IGNORE_FILES = {
    "package-lock.json",
    "package.json",
    "yarn.lock",
    "pnpm-lock.yaml",
}


def load_files(project_path: Path):
    documents = []

    for file in project_path.rglob("*"):

        if not file.is_file():
            continue

        # Skip ignored directories
        if any(part in IGNORE_DIRS for part in file.parts):
            continue

        # Skip hidden/macOS metadata files
        if file.name.startswith("._") or file.name == ".DS_Store":
            continue

        if file.suffix not in SUPPORTED_EXTENSIONS:
            continue

        if file.name in IGNORE_FILES:
            continue

        try:
            content = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            documents.append(
                {
                    "path": str(file),
                    "content": content,
                }
            )

        except Exception as e:
            print(f"Failed to read {file}: {e}")

    return documents