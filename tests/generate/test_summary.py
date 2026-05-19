"""Tests for data_analytics_tools.generate.summary."""

import numpy as np
import pandas as pd
import pytest

from data_analytics_tools.generate.summary import summary, summary_with_correlation


class TestSummary:
    def test_basic_array(self):
        result = summary([1, 2, 3, 4, 5])
        assert result["min"] == 1.0
        assert result["max"] == 5.0
        assert result["mean"] == 3.0
        assert result["median"] == 3.0

    def test_numpy_array(self):
        result = summary(np.array([10, 20, 30]))
        assert result["min"] == 10.0
        assert result["mean"] == 20.0

    def test_single_element(self):
        result = summary([42])
        assert result["min"] == result["max"] == result["mean"] == 42.0

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="empty"):
            summary([])

    def test_quartiles(self):
        data = list(range(1, 101))  # 1..100
        result = summary(data)
        assert result["q1"] == pytest.approx(25.75, abs=0.1)
        assert result["q3"] == pytest.approx(75.25, abs=0.1)

    def test_pandas_series(self):
        result = summary(pd.Series([5, 10, 15]))
        assert result["mean"] == 10.0


class TestSummaryWithCorrelation:
    def test_basic(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        stats, corr = summary_with_correlation(df)
        assert "mean" in stats.columns
        assert corr.shape == (2, 2)
        assert corr.loc["a", "a"] == pytest.approx(1.0)

    def test_not_dataframe_raises(self):
        with pytest.raises(TypeError):
            summary_with_correlation([1, 2, 3])

    def test_no_numeric_raises(self):
        df = pd.DataFrame({"name": ["a", "b"]})
        with pytest.raises(ValueError, match="no numeric"):
            summary_with_correlation(df)

    def test_mixed_columns(self):
        df = pd.DataFrame({"x": [1, 2], "y": [3, 4], "label": ["a", "b"]})
        stats, corr = summary_with_correlation(df)
        assert "label" not in corr.columns
