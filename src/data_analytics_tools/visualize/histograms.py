"""Histogram builders for dates and weekdays."""

from __future__ import annotations

from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import matplotlib
import matplotlib.pyplot as plt

# Use non-interactive backend by default so plots can be saved without a display.
matplotlib.use("Agg")

WEEKDAY_ORDER = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]


# ── Data helpers (pure, no I/O) ─────────────────


def count_dates(dates: Sequence[str], fmt: str = "%Y%m%d") -> List[Tuple[str, int]]:
    """Parse date strings, count occurrences, and return sorted ``(label, count)`` pairs.

    Parameters
    ----------
    dates:
        Raw date strings (e.g. ``"20230115"``).
    fmt:
        ``strptime`` format of each element.

    Returns
    -------
    list[tuple[str, int]]
        Chronologically sorted pairs of ``(YYYY-MM-DD, count)``.
    """
    parsed = [datetime.strptime(d.strip(), fmt) for d in dates if d.strip()]
    counts = Counter(parsed)
    sorted_items = sorted(counts.items())
    return [(dt.strftime("%Y-%m-%d"), c) for dt, c in sorted_items]


def count_weekdays(days: Sequence[str]) -> List[Tuple[str, int]]:
    """Count weekday occurrences and return them in Monday→Sunday order.

    Parameters
    ----------
    days:
        Weekday names (e.g. ``"Monday"``).

    Returns
    -------
    list[tuple[str, int]]
    """
    counts: Dict[str, int] = Counter(d.strip() for d in days if d.strip())
    return [(day, counts.get(day, 0)) for day in WEEKDAY_ORDER]


# ── Plotting helpers ────────────────────────────


def plot_date_histogram(
    dates: Sequence[str],
    fmt: str = "%Y%m%d",
    *,
    title: str = "File Modifications by Date",
    save_path: Optional[str | Path] = None,
    figsize: Tuple[int, int] = (14, 6),
) -> plt.Figure:
    """Create a bar chart of date counts.

    Parameters
    ----------
    dates:
        Raw date strings.
    fmt:
        Date format.
    title:
        Chart title.
    save_path:
        If given, save the figure to this path.
    figsize:
        Matplotlib figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    data = count_dates(dates, fmt)
    if not data:
        raise ValueError("No valid dates provided")
    labels, counts = zip(*data)

    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(labels, counts, color="#4C72B0")
    ax.set_xlabel("Date")
    ax.set_ylabel("Count")
    ax.set_title(title)
    plt.xticks(rotation=45)
    fig.tight_layout()
    if save_path:
        fig.savefig(str(save_path))
    return fig


def plot_weekday_histogram(
    days: Sequence[str],
    *,
    title: str = "File Modifications by Weekday",
    save_path: Optional[str | Path] = None,
    figsize: Tuple[int, int] = (10, 6),
) -> plt.Figure:
    """Create a bar chart of weekday counts.

    Parameters
    ----------
    days:
        Weekday name strings.
    title:
        Chart title.
    save_path:
        If given, save the figure to this path.
    figsize:
        Matplotlib figure size.

    Returns
    -------
    matplotlib.figure.Figure
    """
    data = count_weekdays(days)
    labels, counts = zip(*data)

    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(labels, counts, color="#4C72B0")
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Count")
    ax.set_title(title)
    fig.tight_layout()
    if save_path:
        fig.savefig(str(save_path))
    return fig
