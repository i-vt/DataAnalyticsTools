"""Data-generation helpers: bootstrapping and parametric distributions."""

from __future__ import annotations

from typing import Optional

import numpy as np


def bootstrap(
    data: list | np.ndarray,
    n_samples: int = 1000,
    *,
    seed: Optional[int] = None,
) -> np.ndarray:
    """Generate new samples by resampling *data* with replacement.

    Parameters
    ----------
    data:
        Original observations.
    n_samples:
        Number of bootstrap samples to draw.
    seed:
        Optional RNG seed for reproducibility.

    Returns
    -------
    numpy.ndarray
        Array of length *n_samples*.

    Raises
    ------
    ValueError
        If *data* is empty or *n_samples* < 1.
    """
    arr = np.asarray(data)
    if arr.size == 0:
        raise ValueError("Cannot bootstrap from empty data")
    if n_samples < 1:
        raise ValueError("n_samples must be >= 1")
    rng = np.random.default_rng(seed)
    return rng.choice(arr, size=n_samples, replace=True)


def generate_normal(
    mean: float = 0.0,
    std: float = 1.0,
    n_samples: int = 1000,
    *,
    seed: Optional[int] = None,
) -> np.ndarray:
    """Draw samples from a normal distribution.

    Parameters
    ----------
    mean:
        Centre of the distribution.
    std:
        Standard deviation (must be > 0).
    n_samples:
        Number of points to generate.
    seed:
        Optional RNG seed.

    Returns
    -------
    numpy.ndarray

    Raises
    ------
    ValueError
        If *std* <= 0 or *n_samples* < 1.
    """
    if std <= 0:
        raise ValueError("std must be positive")
    if n_samples < 1:
        raise ValueError("n_samples must be >= 1")
    rng = np.random.default_rng(seed)
    return rng.normal(mean, std, n_samples)
