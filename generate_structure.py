import os

import pathspec


def load_gitignore_patterns(gitignore_path):
    with open(gitignore_path, "r") as f:
        return pathspec.PathSpec.from_lines("gitwildmatch", f)


def should_ignore(file_path, patterns):
    # Ignore files/folders starting with a dot
    if os.path.basename(file_path).startswith("."):
        return True
    return patterns.match_file(file_path)


def generate_project_structure(root_dir, output_file, gitignore_path):
    patterns = load_gitignore_patterns(gitignore_path)

    with open(output_file, "w") as f:
        for root, dirs, files in os.walk(root_dir):
            # Skip directories based on .gitignore and those starting with a dot
            dirs[:] = [
                d for d in dirs if not should_ignore(os.path.join(root, d), patterns)
            ]
            level = root.replace(root_dir, "").count(os.sep)
            indent = " " * 4 * level
            f.write("{}{}/\n".format(indent, os.path.basename(root)))
            subindent = " " * 4 * (level + 1)
            for file in files:
                if not should_ignore(os.path.join(root, file), patterns):
                    f.write("{}{}\n".format(subindent, file))


if __name__ == "__main__":
    root_directory = "."  # Replace with your project's root directory
    gitignore_file = os.path.join(root_directory, ".gitignore")
    output_file_path = "project_structure.txt"  # Output file

    if os.path.exists(gitignore_file):
        generate_project_structure(root_directory, output_file_path, gitignore_file)
        print(f"Project structure saved to {output_file_path}")
    else:
        print(f".gitignore file not found in {root_directory}")
