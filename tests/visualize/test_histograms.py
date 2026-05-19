"""Tests for data_analytics_tools.visualize.histograms."""

import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import pytest

from data_analytics_tools.visualize.histograms import (
    count_dates,
    count_weekdays,
    plot_date_histogram,
    plot_weekday_histogram,
)


class TestCountDates:
    def test_basic(self):
        result = count_dates(["20230101", "20230101", "20230315"])
        assert result == [("2023-01-01", 2), ("2023-03-15", 1)]

    def test_sorted_output(self):
        result = count_dates(["20231231", "20230101"])
        assert result[0][0] < result[1][0]

    def test_whitespace_handling(self):
        result = count_dates(["  20230501  ", "20230501\n"])
        assert result == [("2023-05-01", 2)]

    def test_empty(self):
        assert count_dates([]) == []

    def test_custom_format(self):
        result = count_dates(["01-15-2023"], fmt="%m-%d-%Y")
        assert result == [("2023-01-15", 1)]


class TestCountWeekdays:
    def test_basic(self):
        result = count_weekdays(["Monday", "Monday", "Friday"])
        # Should be in WEEKDAY_ORDER
        assert result[0] == ("Monday", 2)
        assert result[4] == ("Friday", 1)
        # Days not mentioned have 0
        assert result[1] == ("Tuesday", 0)

    def test_all_days(self):
        result = count_weekdays(["Monday", "Tuesday", "Wednesday", "Thursday",
                                  "Friday", "Saturday", "Sunday"])
        assert all(c == 1 for _, c in result)

    def test_empty(self):
        result = count_weekdays([])
        assert all(c == 0 for _, c in result)


class TestPlotDateHistogram:
    def test_returns_figure(self):
        fig = plot_date_histogram(["20230101", "20230201"])
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_save(self, tmp_path: Path):
        path = tmp_path / "dates.png"
        fig = plot_date_histogram(["20230101"], save_path=path)
        assert path.exists()
        assert path.stat().st_size > 0
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            plot_date_histogram([])


class TestPlotWeekdayHistogram:
    def test_returns_figure(self):
        fig = plot_weekday_histogram(["Monday", "Friday"])
        assert fig is not None
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_save(self, tmp_path: Path):
        path = tmp_path / "weekdays.png"
        fig = plot_weekday_histogram(["Tuesday"], save_path=path)
        assert path.exists()
        import matplotlib.pyplot as plt
        plt.close(fig)
