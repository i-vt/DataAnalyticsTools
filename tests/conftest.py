"""Shared fixtures for the test-suite."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture()
def tmp(tmp_path: Path) -> Path:
    """Shortcut for the built-in tmp_path."""
    return tmp_path


@pytest.fixture()
def sample_dates_file(tmp_path: Path) -> Path:
    p = tmp_path / "dates.txt"
    p.write_text("20230101\n20230101\n20230315\n20230720\n")
    return p


@pytest.fixture()
def sample_weekdays_file(tmp_path: Path) -> Path:
    p = tmp_path / "days.txt"
    p.write_text("Monday\nWednesday\nFriday\nMonday\nSunday\n")
    return p


@pytest.fixture()
def sample_csv_xy(tmp_path: Path) -> Path:
    p = tmp_path / "data.csv"
    p.write_text("1 10\n2 20\n3 30\n4 40\n")
    return p
