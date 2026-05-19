"""File-system cleanup helpers: prefix removal, folder organisation, recursive reading."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List, Optional


# ── Result types ────────────────────────────────

@dataclass
class RenameResult:
    """Outcome of a single rename operation."""
    old_name: str
    new_name: str
    success: bool
    error: Optional[str] = None


@dataclass
class MoveResult:
    """Outcome of moving a file into its own folder."""
    filename: str
    folder: str
    success: bool
    error: Optional[str] = None


@dataclass
class FileContent:
    """Content read from a single file."""
    path: str
    length: int
    content: str
    error: Optional[str] = None


# ── Helpers ─────────────────────────────────────

_IGNORED_FILES = frozenset({".DS_Store", "Thumbs.db", "desktop.ini"})


def _should_skip(name: str) -> bool:
    return name in _IGNORED_FILES or name.startswith(".")


# ── Public API ──────────────────────────────────


def remove_prefix(
    dir_path: str | Path,
    prefix: str,
) -> List[RenameResult]:
    """Remove *prefix* from every matching filename in *dir_path*.

    Parameters
    ----------
    dir_path:
        Directory to scan (non-recursive).
    prefix:
        The filename prefix to strip.

    Returns
    -------
    list[RenameResult]
        One entry per file that matched *prefix*.
    """
    dir_path = Path(dir_path)
    results: List[RenameResult] = []
    for entry in sorted(dir_path.iterdir()):
        if _should_skip(entry.name):
            continue
        if entry.name.startswith(prefix):
            new_name = entry.name[len(prefix):]
            if not new_name:
                continue
            try:
                entry.rename(dir_path / new_name)
                results.append(RenameResult(entry.name, new_name, True))
            except OSError as exc:
                results.append(RenameResult(entry.name, new_name, False, str(exc)))
    return results


def move_to_own_folders(dir_path: str | Path) -> List[MoveResult]:
    """Move every file in *dir_path* into a sub-folder named after the file (minus extension).

    Returns
    -------
    list[MoveResult]
        One entry per file processed.
    """
    dir_path = Path(dir_path)
    results: List[MoveResult] = []
    for entry in sorted(dir_path.iterdir()):
        if not entry.is_file() or _should_skip(entry.name):
            continue
        folder_name = entry.stem
        folder_path = dir_path / folder_name
        try:
            folder_path.mkdir(exist_ok=True)
            shutil.move(str(entry), str(folder_path / entry.name))
            results.append(MoveResult(entry.name, folder_name, True))
        except OSError as exc:
            results.append(MoveResult(entry.name, folder_name, False, str(exc)))
    return results


def read_files_recursively(
    root: str | Path,
    *,
    on_file: Optional[Callable[[FileContent], None]] = None,
) -> List[FileContent]:
    """Read every text file under *root* and return their contents.

    Parameters
    ----------
    root:
        Top-level directory.
    on_file:
        Optional callback invoked for each file as it is read.

    Returns
    -------
    list[FileContent]
    """
    root = Path(root)
    results: List[FileContent] = []
    for dirpath, _dirs, filenames in os.walk(root):
        for fname in sorted(filenames):
            if _should_skip(fname):
                continue
            fpath = Path(dirpath) / fname
            try:
                content = fpath.read_text(encoding="utf-8", errors="replace")
                fc = FileContent(str(fpath), len(content), content)
            except OSError as exc:
                fc = FileContent(str(fpath), 0, "", str(exc))
            results.append(fc)
            if on_file:
                on_file(fc)
    return results
