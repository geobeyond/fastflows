import os
from typing import Optional


def check_path_is_dir(path: Optional[str]) -> Optional[str]:
    """raise error or return path if it is a dir"""
    if path:
        check_path_exists(path)
        if not os.path.isdir(path):
            raise ValueError(f"Path '{path}' is not a directory")
        return path


def check_path_exists(path: Optional[str]) -> Optional[str]:
    """raise error or return path if it is a dir"""

    if path:
        if not os.path.exists(path):
            raise ValueError(f"Path '{path}' does not exist")
        return path
