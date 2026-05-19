"""Tests for data_analytics_tools.cleanup.formatting."""

from pathlib import Path

import pytest

from data_analytics_tools.cleanup.formatting import (
    move_to_own_folders,
    read_files_recursively,
    remove_prefix,
)


class TestRemovePrefix:
    def test_basic_rename(self, tmp_path: Path):
        (tmp_path / "PREFIX_file1.txt").write_text("a")
        (tmp_path / "PREFIX_file2.txt").write_text("b")
        (tmp_path / "other.txt").write_text("c")

        results = remove_prefix(tmp_path, "PREFIX_")
        assert len(results) == 2
        assert all(r.success for r in results)
        assert (tmp_path / "file1.txt").exists()
        assert (tmp_path / "file2.txt").exists()
        assert (tmp_path / "other.txt").exists()

    def test_no_matches(self, tmp_path: Path):
        (tmp_path / "noprefix.txt").write_text("x")
        results = remove_prefix(tmp_path, "ZZZ_")
        assert results == []

    def test_skips_ds_store(self, tmp_path: Path):
        (tmp_path / ".DS_Store").write_text("")
        results = remove_prefix(tmp_path, ".")
        assert results == []


class TestMoveToOwnFolders:
    def test_moves_files(self, tmp_path: Path):
        (tmp_path / "report.pdf").write_text("content")
        (tmp_path / "notes.txt").write_text("text")

        results = move_to_own_folders(tmp_path)
        assert len(results) == 2
        assert (tmp_path / "report" / "report.pdf").exists()
        assert (tmp_path / "notes" / "notes.txt").exists()

    def test_empty_dir(self, tmp_path: Path):
        results = move_to_own_folders(tmp_path)
        assert results == []


class TestReadFilesRecursively:
    def test_reads_nested(self, tmp_path: Path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "a.txt").write_text("hello")
        (sub / "b.txt").write_text("world")

        results = read_files_recursively(tmp_path)
        assert len(results) == 2
        contents = {r.content for r in results}
        assert contents == {"hello", "world"}

    def test_callback(self, tmp_path: Path):
        (tmp_path / "f.txt").write_text("data")
        seen = []
        read_files_recursively(tmp_path, on_file=lambda fc: seen.append(fc.path))
        assert len(seen) == 1

    def test_empty_dir(self, tmp_path: Path):
        assert read_files_recursively(tmp_path) == []
