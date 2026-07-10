import os
from typing import Any

import yaml


class LoadError(Exception):
    "Base class for load errors."

    pass


class InvalidYamlError(LoadError):
    "Invalid YAML error."

    pass


class TestStructureError(LoadError):
    "Test structure error."

    pass


class DirectoryNotFoundError(LoadError):
    "Directory not found error."

    pass


def load_test_yaml(file_path: str) -> dict[str, str | int | list[Any]] | bool:
    """Loads and parses a YAML test file.

    Args:
        file_path: Path to the .test.yaml or .test.yml file.

    Returns:
        The parsed YAML as a dictionary, or False if the file is not found."
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            test_specification = yaml.safe_load(f)
            if not test_specification:
                test_specification = {}
            return test_specification
    except FileExistsError:
        raise FileExistsError(f"Not a file: {file_path}")
    except yaml.YAMLError as e:
        raise InvalidYamlError(f"Invalid YAML in {file_path}: {e}")
    except UnicodeDecodeError as e:
        raise InvalidYamlError(f"Encoding error in {file_path}: {e}")


def search_files(base_path: str) -> list[str]:
    """Searches for test files with a .yatl.yaml/.yatl.yml suffix.

    If base_path is a single file with a valid extension, returns it directly.
    Otherwise, recursively searches the directory for matching files.

    Args:
        base_path: Path to a .yatl.yaml/.yatl.yml file or a directory.

    Returns:
        List of found file paths.

    Raises:
        DirectoryNotFoundError: If base_path is neither a file nor a directory.
    """
    if os.path.isfile(base_path):
        if base_path.endswith(".yatl.yaml") or base_path.endswith(".yatl.yml"):
            return [base_path]
        return []

    if not os.path.isdir(base_path):
        raise DirectoryNotFoundError(f"Directory does not exist: {base_path}")

    files = []

    def _search(current_path: str):
        for item in os.listdir(current_path):
            full_path = os.path.join(current_path, item)
            if os.path.isfile(full_path) and (
                item.endswith(".yatl.yaml") or item.endswith(".yatl.yml")
            ):
                files.append(full_path)
            elif os.path.isdir(full_path):
                _search(full_path)

    _search(base_path)
    return files
