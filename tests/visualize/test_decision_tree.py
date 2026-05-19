"""Tests for data_analytics_tools.visualize.decision_tree."""

import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import matplotlib.pyplot as plt
import pytest

from data_analytics_tools.visualize.decision_tree import train_trees


@pytest.fixture()
def iris_csv(tmp_path: Path) -> Path:
    """Create a tiny CSV suitable for decision-tree training."""
    p = tmp_path / "iris.csv"
    lines = [
        "sepal_len|sepal_wid|petal_len|petal_wid|species",
        "5.1|3.5|1.4|0.2|0",
        "4.9|3.0|1.4|0.2|0",
        "7.0|3.2|4.7|1.4|1",
        "6.4|3.2|4.5|1.5|1",
        "6.3|3.3|6.0|2.5|2",
        "5.8|2.7|5.1|1.9|2",
        "5.1|3.5|1.4|0.2|0",
        "4.9|3.0|1.4|0.2|0",
        "7.0|3.2|4.7|1.4|1",
        "6.4|3.2|4.5|1.5|1",
    ]
    p.write_text("\n".join(lines))
    return p


class TestTrainTrees:
    def test_basic(self, iris_csv: Path):
        results = train_trees(iris_csv)
        assert len(results) > 0
        for r in results:
            assert 0.0 <= r.accuracy <= 1.0
            assert r.model is not None
            plt.close(r.figure)

    def test_drop_columns(self, iris_csv: Path):
        results = train_trees(iris_csv, drop_columns=["sepal_len", "sepal_wid"])
        targets = {r.target for r in results}
        assert "sepal_len" not in targets
        for r in results:
            plt.close(r.figure)

    def test_save_dir(self, iris_csv: Path, tmp_path: Path):
        out = tmp_path / "trees"
        results = train_trees(iris_csv, save_dir=out)
        pngs = list(out.glob("*.png"))
        assert len(pngs) == len(results)
        for r in results:
            plt.close(r.figure)
