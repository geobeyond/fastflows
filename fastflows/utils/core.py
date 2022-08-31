from typing import Optional, Union
from pathlib import Path


def check_path_is_dir(path: Optional[Union[Path, str]]) -> Optional[Path]:
    """raise error or return path if it is a dir"""
    if isinstance(path, str):
        path = Path(path)
    if path:
        check_path_exists(path)
        if not path.is_dir():
            raise ValueError(f"Path '{path}' is not a directory")
        return path


def check_path_exists(path: Optional[Union[Path, str]]) -> Optional[Path]:
    """raise error or return path if it is a dir"""
    if isinstance(path, str):
        path = Path(path)
    if path:
        if not path.exists():
            raise ValueError(f"Path '{path}' does not exist")
        return path
