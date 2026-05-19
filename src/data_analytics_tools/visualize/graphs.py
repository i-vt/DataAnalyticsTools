"""Simple line/scatter chart from tabular data."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence, Tuple

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use("Agg")


def plot_from_csv(
    csv_path: str | Path,
    *,
    sep: str = " ",
    x_col: str = "x",
    y_col: str = "y",
    xlabel: str = "X",
    ylabel: str = "Y",
    title: str = "Graph",
    save_path: Optional[str | Path] = None,
    dpi: int = 150,
    figsize: Tuple[int, int] = (10, 6),
) -> plt.Figure:
    """Plot an X/Y line chart from a CSV file.

    Parameters
    ----------
    csv_path:
        Path to the CSV file.
    sep:
        Column separator.
    x_col, y_col:
        Column names (or positional names assigned when ``header=None``).
    xlabel, ylabel, title:
        Axis / chart labels.
    save_path:
        Optional path to save the figure.
    dpi:
        Resolution for saved image.
    figsize:
        Figure dimensions.

    Returns
    -------
    matplotlib.figure.Figure
    """
    df = pd.read_csv(csv_path, sep=sep, header=None, names=[x_col, y_col])
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.plot(df[x_col], df[y_col], marker="o", linewidth=1.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    if save_path:
        fig.savefig(str(save_path), dpi=dpi)
    return fig


def plot_xy(
    x: Sequence[float],
    y: Sequence[float],
    *,
    xlabel: str = "X",
    ylabel: str = "Y",
    title: str = "Graph",
    save_path: Optional[str | Path] = None,
    dpi: int = 150,
    figsize: Tuple[int, int] = (10, 6),
) -> plt.Figure:
    """Plot X/Y data from sequences (no file required).

    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.plot(x, y, marker="o", linewidth=1.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    if save_path:
        fig.savefig(str(save_path), dpi=dpi)
    return fig
