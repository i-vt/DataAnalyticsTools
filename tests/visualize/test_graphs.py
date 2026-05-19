"""Tests for data_analytics_tools.visualize.graphs."""

import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import matplotlib.pyplot as plt
import pytest

from data_analytics_tools.visualize.graphs import plot_from_csv, plot_xy


class TestPlotFromCsv:
    def test_basic(self, sample_csv_xy: Path):
        fig = plot_from_csv(sample_csv_xy)
        assert fig is not None
        plt.close(fig)

    def test_save(self, sample_csv_xy: Path, tmp_path: Path):
        out = tmp_path / "graph.png"
        fig = plot_from_csv(sample_csv_xy, save_path=out)
        assert out.exists()
        plt.close(fig)


class TestPlotXY:
    def test_basic(self):
        fig = plot_xy([1, 2, 3], [10, 20, 30])
        assert fig is not None
        plt.close(fig)

    def test_custom_labels(self):
        fig = plot_xy([0], [0], xlabel="Time", ylabel="Value", title="Test")
        axes = fig.get_axes()
        assert axes[0].get_title() == "Test"
        plt.close(fig)

    def test_save(self, tmp_path: Path):
        out = tmp_path / "xy.png"
        fig = plot_xy([1, 2], [3, 4], save_path=out)
        assert out.exists()
        plt.close(fig)
