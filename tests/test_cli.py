"""Tests for the CLI entry point."""

from pathlib import Path

import pytest

from data_analytics_tools.cli import main


class TestCLI:
    def test_summary(self, tmp_path: Path):
        csv = tmp_path / "d.csv"
        csv.write_text("val\n1\n2\n3\n4\n5\n")
        assert main(["summary", str(csv)]) == 0

    def test_bootstrap(self):
        assert main(["bootstrap", "[1,2,3,4,5]", "--n", "10", "--seed", "0"]) == 0

    def test_normal(self):
        assert main(["normal", "--mean", "5", "--std", "2", "--n", "10"]) == 0

    def test_tokenize_token(self):
        assert main(["tokenize", '["a","b","c"]']) == 0

    def test_tokenize_hash(self):
        assert main(["tokenize", '["x","y"]', "--method", "hash"]) == 0

    def test_histogram_dates(self, sample_dates_file: Path, tmp_path: Path):
        out = tmp_path / "h.png"
        assert main(["histogram-dates", str(sample_dates_file), "--save", str(out)]) == 0
        assert out.exists()

    def test_histogram_weekdays(self, sample_weekdays_file: Path, tmp_path: Path):
        out = tmp_path / "w.png"
        assert main(["histogram-weekdays", str(sample_weekdays_file), "--save", str(out)]) == 0
        assert out.exists()

    def test_graph(self, sample_csv_xy: Path, tmp_path: Path):
        out = tmp_path / "g.png"
        assert main(["graph", str(sample_csv_xy), "--save", str(out)]) == 0
        assert out.exists()

    def test_bad_command_returns_error(self):
        with pytest.raises(SystemExit):
            main(["nonexistent-command"])
