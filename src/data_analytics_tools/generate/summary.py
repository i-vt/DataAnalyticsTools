"""Statistical summary utilities inspired by R's ``summary()``."""

from __future__ import annotations

from typing import Dict, Tuple, Union

import numpy as np
import pandas as pd


def summary(data: Union[list, np.ndarray, pd.Series]) -> Dict[str, float]:
    """Return a six-number statistical summary (min, Q1, median, mean, Q3, max).

    Parameters
    ----------
    data:
        Numeric data as a list, NumPy array, or Pandas Series.

    Returns
    -------
    dict[str, float]
        Keys: ``min``, ``q1``, ``median``, ``mean``, ``q3``, ``max``.

    Raises
    ------
    ValueError
        If *data* is empty.
    """
    arr = np.asarray(data, dtype=float)
    if arr.size == 0:
        raise ValueError("Cannot summarise empty data")
    return {
        "min": float(np.min(arr)),
        "q1": float(np.percentile(arr, 25)),
        "median": float(np.median(arr)),
        "mean": float(np.mean(arr)),
        "q3": float(np.percentile(arr, 75)),
        "max": float(np.max(arr)),
    }


def summary_with_correlation(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return descriptive statistics and correlation matrix for a DataFrame.

    Parameters
    ----------
    df:
        DataFrame with numeric columns.

    Returns
    -------
    tuple[DataFrame, DataFrame]
        ``(summary_stats, correlation_matrix)``

    Raises
    ------
    TypeError
        If *df* is not a DataFrame.
    ValueError
        If *df* has no numeric columns.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        raise ValueError("DataFrame contains no numeric columns")

    stats = numeric_df.describe().T
    stats["mean"] = numeric_df.mean()
    stats["median"] = numeric_df.median()
    corr = numeric_df.corr()
    return stats, corr
